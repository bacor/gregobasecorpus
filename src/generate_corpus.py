###
# Author: Bas Cornelissen
# Date: February 2020

###
"""
Generate the GregoBase Corpus.
"""
import pymysql
import random
import os
import pandas as pd
import shutil
import json
import datetime

# GregoBase Corpus version
__version__ = '0.4'

# Directories
SRC_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(SRC_DIR, os.path.pardir))
DIST_DIR = os.path.join(ROOT_DIR, 'dist')
OUTPUT_DIR = os.path.join(DIST_DIR, f'gregobasecorpus-v{__version__}')
CSV_DIR = os.path.join(OUTPUT_DIR, 'csv')
GABC_DIR = os.path.join(OUTPUT_DIR, 'gabc')

# Load database structure
db_structure_fn = os.path.join(SRC_DIR, 'db_structure.json')
with open(db_structure_fn, 'r') as handle:
    DB_STRUCTURE = json.load(handle)

##

def random_id(length=5):
    """Return a random alphanumeric string of a given length"""
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(chars) for _ in range(length))

def compress_distribution(remove_dir=False):
    archive_fn = os.path.join(DIST_DIR, f'gregobasecorpus-v{__version__}')
    shutil.make_archive(archive_fn, 'zip', OUTPUT_DIR)
    if remove_dir:
        shutil.rmtree(OUTPUT_DIR)

##

class GregoBaseConverter(object):

    field_delimiter = '@'
    """str: delimiter used in the temporary csv file"""
    
    def __init__(self, db_host='localhost', db_user='root', db_pass='',
        db_prefix='gregobase_', db_structure=DB_STRUCTURE):
        
        # Initialize database
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_prefix = db_prefix
        self.db_name = f'tmp_db_gregocorpus_{random_id()}'
        self.db = pymysql.connect(host=db_host, user=db_user, password=db_pass)
        self.cursor = self.db.cursor()

        # Set up directories
        self.tmp_dir = os.path.join(OUTPUT_DIR, 'tmp')

        # Clear 
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        for dir_path in [CSV_DIR, self.tmp_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        self.db_structure = db_structure

    def create_db(self):
        return self.cursor.execute(f'CREATE DATABASE {self.db_name};')

    def delete_db(self):
        return self.cursor.execute(f'DROP DATABASE {self.db_name};')

    def import_sql(self, filepath):
        mysql = f'mysql --host={self.db_host} --user={self.db_user} --password={self.db_pass}'
        command = f'{mysql} {self.db_name} < {filepath}'
        os.system(command)

    def export_tables(self):
        """Export the database tables to CSV files. 
        
        This is done in two steps. The database tables are first exported to
        an intermediate CSV format using funny delimiters (stored in a temporary)
        directory. Second, these are converted to the final, ordinary CSV files."""
        self.cursor.execute(f'USE {self.db_name};')
        for table_name in self.db_structure.keys():
            # Export db table to temporary csv file
            tmp_filepath = os.path.join(self.tmp_dir, f'{table_name}.csv')
            statement = (
                "SELECT * from {db_prefix}{table_name} INTO OUTFILE '{filepath}' "
                "FIELDS OPTIONALLY ENCLOSED BY '{delimiter}' "
                "TERMINATED BY ',' "
                "LINES TERMINATED BY '\n'"
                ).format(filepath=tmp_filepath, 
                         table_name=table_name, 
                         delimiter=self.field_delimiter,
                         db_prefix=self.db_prefix)
            self.cursor.execute(statement)
            
            # Post process and convert to final csv file
            columns = self.db_structure[table_name]
            dtypes = {}
            dtype_map = { 'str': str, 'int': int }
            dtypes = { col['name']: dtype_map[col['dtype']] for col in columns }
            names = [ col['name'] for col in columns ]
            df = pd.read_csv(tmp_filepath,
                            names=names, 
                            dtype=dtypes,
                            sep=',', 
                            escapechar='\\', 
                            quotechar=self.field_delimiter,
                            na_values='N',
                            index_col=0,
                            engine='python')

            target_fn = os.path.join(CSV_DIR, f'{table_name}.csv')
            df.to_csv(target_fn)

        # Remove temporary directory
        shutil.rmtree(self.tmp_dir)

    def convert(self, filepath):
        """Convert a sql dump of GregoBase into a set of CSV files
        
        Args:
            filepath (str): a path to the .sql file
        """
        self.create_db()
        self.import_sql(filepath)
        self.export_tables()
        self.delete_db()

##

class GABCConverter(object):
    def __init__(self, db_structure=DB_STRUCTURE):
        """"""
        self.db_structure = db_structure

        # Set up output directories
        if not os.path.exists(GABC_DIR):
            os.makedirs(GABC_DIR)
        if not os.path.exists(CSV_DIR):
            raise Exception('CSV directory not found')

        # Load all csv files
        chants_fn = os.path.join(CSV_DIR, 'chants.csv')
        self.chants = pd.read_csv(chants_fn, index_col=0) 
        chant_sources_fn = os.path.join(CSV_DIR, 'chant_sources.csv')
        self.chant_sources = pd.read_csv(chant_sources_fn, index_col=0)
        chant_tags_fn = os.path.join(CSV_DIR, 'chant_tags.csv')
        self.chant_tags = pd.read_csv(chant_tags_fn, index_col=0)
        sources_fn = os.path.join(CSV_DIR, 'sources.csv')
        self.sources = pd.read_csv(sources_fn, index_col=0)
        tags_fn = os.path.join(CSV_DIR, 'tags.csv')
        self.tags = pd.read_csv(tags_fn, index_col=0)

    def extract_gabc_body(self, idx):
        """Extract the gabc body of a chant from the chants table
        
        Args:
            idx (int): The id of a chant
        
        Raises:
            Exception: when the chant does not have gabc
            Exception: when the encoding can't be converted to utf-8
        
        Returns:
            str: A gabc string
        """
        chant = self.chants.loc[idx, :]

        if type(chant.gabc) != str:
            return ""

        # The chant is a list of tex/gabc strings; extract only the gabc
        elif not chant.gabc.startswith('"'):
            parts = json.loads(chant.gabc)
            gabc = ""
            for format, contents, _ in parts:
                if format == 'gabc':
                    gabc += contents
                elif format == 'tex':
                    gabc += f' <v>{contents}</v>() '

        # All other cases: remove the quotes around the gabc
        elif chant.gabc.startswith('"') and chant.gabc.endswith('"'):
            gabc = chant.gabc[1:len(chant.gabc)-1]
        else:
            print(f'Skipping {chant.name}: cannot find gabc')
            return False

        # First encode to bytes, then decode, also the escaped unicode chars:
        try:
            gabc = gabc.encode('latin1').decode('unicode-escape')
        except:
            print(f'Skipping {chant.name}: cannot be converted to utf-8')
            return False

        if not pd.isnull(chant['gabc_verses']):
            gabc += chant['gabc_verses']

        return gabc

    def collect_metadata(self, idx):
        """Collect all metadata for a given chant from the various tables in the 
        GregoBase database. 
        
        The standard GABC fields are:

        - ``name``
        - ``office_part``
        - ``mode``
        - ``transcriber``
        - ``license`` (non-standard; always CC0 for GregoBase)

        Besides this, we collect all sources and tags associated with a chant. 
        Those gregobase-specific meta-fields all start with the `_gregobase` prefix:

        - ``_gregobase_id``: the id of the chant
        - ``_gregobase_url``: the gregobase webpage for the chant
        - ``_gregobase_corpus_version`: version of the converter
        - ``_gregobase_sources``: a comma-separated list of source ids for sources 
            the chant appears in.
        - ``_gregobase_source_{i}_id``: the id of the i-th source
        - ``_gregobase_source_{i}_title``: the title of the i-th source
        - ``_gregobase_source_{i}_year``: the year of the i-th source
        - ``_gregobase_tags``: a comma-separated list of tag ids
        - ``_gregobase_tag_{i}_id``: the id of the i-th tag
        - ``_gregobase_tag_{i}_name``: the name of the i-th tag
        """
        
        chant = self.chants.loc[idx,:]
        metadata = {
            'name': chant['incipit'],
            'office_part': chant['office_part'],
            'mode': chant['mode'],
            'transcriber': chant['transcriber'],
            'commentary': chant['commentary'],
            'user-notes': chant['remarks'],
            'gabc-copyright': 'CC0-1.0 <http://creativecommons.org/publicdomain/zero/1.0/>',
            '_gregobase_url': f'https://gregobase.selapa.net/chant.php?id={idx}',
            '_gregobase_id': idx,
            '_gregobase_corpus_version': __version__,
        }
        
        if not pd.isnull(chant['commentary']):
            metadata['commentary'] = chant['commentary']
        
        if not pd.isnull(chant['cantus_id']):
            metadata['_gregobase_cantus_id'] = chant['cantus_id']
        
        if not pd.isnull(chant['mode_var']):
            metadata['_gregobase_mode_var'] = chant['mode_var']

        # Add data about all sources the chant is found in
        source_ids = self.chant_sources.query(f'chant_id=={idx}')['source']
        if len(source_ids) > 0:
            metadata['_gregobase_sources'] = ",".join(str(i) for i in source_ids)
            for i, source_id in enumerate(source_ids):
                source = self.sources.loc[source_id, :]
                metadata[f'_gregobase_source_{i}_id'] = source_id
                metadata[f'_gregobase_source_{i}_title'] = source["title"]
                metadata[f'_gregobase_source_{i}_year'] = source["year"]

        # Add all tags associated to the chant
        tag_ids = self.chant_tags.query(f'chant_id=={idx}')['tag_id']
        if len(tag_ids) > 0:
            metadata['_gregobase_tags'] = ",".join(str(i) for i in tag_ids)
            for i, tag_id in enumerate(tag_ids):
                tag = self.tags.loc[tag_id, :]
                metadata[f'_gregobase_tag_{i}_id'] = tag_id
                metadata[f'_gregobase_tag_{i}_name'] = tag['tag']

        return metadata

    def convert(self, filename='{idx:0>5}.gabc'):
        """Exports all chants to GABC files.

        The header of the gabc file contains a lot of metadata, see 
        :func:`collect_metadata` for details.
        
        Args:
            chants (pd.DataFrame): The chants table
            chant_tags (pd.DataFrame): The chant_tags table (chant_tags.csv)
            chant_sources (pd.DataFrame): The chant_sources table (chant_sources.csv)
            sources (pd.DataFrame): The sources table (sources.csv)
            tags (pd.DataFrame): The tags table (tags.csv)
            filepath (str, optional): A formattable string for the gabc files to output.
                Defaults to 'gabc/{idx:0>5}.gabc'.
        """
        
        for idx, chant in self.chants.iterrows():
            body = self.extract_gabc_body(idx)
            if body is not False:
                metadata = self.collect_metadata(idx)
                filepath = os.path.join(GABC_DIR, filename.format(idx=idx))

                with open(filepath, 'w') as handle:
                    for key, value in metadata.items():
                        attribute = f'{key}:{value};\n'
                        handle.write(attribute)        
                    handle.write("%%\n")
                    handle.write(body)

##

class ReadmeWriter(object):

    def __init__(self, db_structure=DB_STRUCTURE):
        """"""
        self.db_structure = db_structure

        # Set up output directories
        OUTPUT_DIR = os.path.join(DIST_DIR, f'gregobasecorpus-v{__version__}')
        GABC_DIR = os.path.join(OUTPUT_DIR, 'gabc')
        if not os.path.exists(GABC_DIR):
            os.makedirs(GABC_DIR)

        CSV_DIR = os.path.join(OUTPUT_DIR, 'csv')
        if not os.path.exists(CSV_DIR):
            raise Exception('CSV directory not found')

        # Load all csv files
        chants_fn = os.path.join(CSV_DIR, 'chants.csv')
        self.chants = pd.read_csv(chants_fn, index_col=0) 
        chant_sources_fn = os.path.join(CSV_DIR, 'chant_sources.csv')
        self.chant_sources = pd.read_csv(chant_sources_fn, index_col=0)
        chant_tags_fn = os.path.join(CSV_DIR, 'chant_tags.csv')
        self.chant_tags = pd.read_csv(chant_tags_fn, index_col=0)
        sources_fn = os.path.join(CSV_DIR, 'sources.csv')
        self.sources = pd.read_csv(sources_fn, index_col=0)
        tags_fn = os.path.join(CSV_DIR, 'tags.csv')
        self.tags = pd.read_csv(tags_fn, index_col=0)

    def table_structure(self, table_name):
        lines = []
        lines.append('| Column       | Type | Description                                        |')
        lines.append('|--------------|------|----------------------------------------------------|')
        for column in self.db_structure[table_name]:
            name = column['name']
            dtype = column['dtype']
            description = column['description']
            lines.append(f'| {name: <12} | {dtype: <4} | {description: <50} |')
        return '\n'.join(lines)

    def write_readme(self, gregobase_export_date="?"):
        now = datetime.datetime.now()
        corpus_date = now.strftime("%d %B %Y")
        num_gabc_files = len([f for f in os.listdir(GABC_DIR) 
            if os.path.isfile(os.path.join(GABC_DIR,f))])

        template_kws = {
            'version': __version__,
            'chants_structure': self.table_structure('chants'),
            'chant_sources_structure': self.table_structure('chant_sources'),
            'chant_tags_structure': self.table_structure('chant_tags'),
            'tags_structure': self.table_structure('tags'),
            'sources_structure': self.table_structure('sources'),
            'gregobase_export_date': gregobase_export_date,
            'num_gabc_files': num_gabc_files,
            'num_chants': len(self.chants),
            'num_sources': len(self.sources),
            'num_tags': len(self.tags),
            'corpus_date': corpus_date
        }

        with open(os.path.join(SRC_DIR, 'readme_template.md'), 'r') as handle:
            template = handle.read()
            readme = template.format(**template_kws)
        
        readme_fn = os.path.join(OUTPUT_DIR, 'README.md')
        with open(readme_fn, 'w') as handle:
            handle.write(readme)

##

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate the GregoBase Corpus.')
    parser.add_argument('--sql', type=str,
                        help='path the gregobase database dump')
    parser.add_argument('--date', type=str,
                        help='the date on which gregobase was exported (you can find this in the sql file)')   
    args = parser.parse_args()



    # Go!
    converter = GregoBaseConverter()
    converter.convert(filepath=args.sql)
    gabc = GABCConverter()
    gabc.convert()
    writer = ReadmeWriter()
    writer.write_readme(gregobase_export_date=args.date)
    compress_distribution()

if __name__ == '__main__':
    main()
    
    # converter = GregoBaseConverter()
    # converter.convert('../gregobase_dumps/gregobase_20191024.sql')

    # gabc = GABCConverter()
    # gabc.convert()

    # writer = ReadmeWriter()
    # writer.write_readme()

    