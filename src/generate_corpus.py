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
import logging
from music21 import converter
import chant21

# GregoBase Corpus version
__version__ = '0.4'

# Directories
SRC_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(SRC_DIR, os.path.pardir))
DIST_DIR = os.path.join(ROOT_DIR, 'dist')
OUTPUT_DIR = os.path.join(DIST_DIR, f'gregobasecorpus-v{__version__}')
CSV_DIR = os.path.join(OUTPUT_DIR, 'csv')
GABC_DIR = os.path.join(OUTPUT_DIR, 'gabc')
HTML_DIR = os.path.join(OUTPUT_DIR, 'html')        

# Load database structure
db_structure_fn = os.path.join(SRC_DIR, 'db_structure.json')
with open(db_structure_fn, 'r') as handle:
    DB_STRUCTURE = json.load(handle)

##

def random_id(length=5):
    """Return a random alphanumeric string of a given length"""
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(chars) for _ in range(length))

def compress_corpus():
    """Compress the output directory, and put the archive inside it."""
    archive_fn = os.path.join(DIST_DIR, f'gregobasecorpus-v{__version__}')
    shutil.make_archive(archive_fn, 'zip', OUTPUT_DIR)
    source_fn = f'{archive_fn}.zip'
    target_fn = os.path.join(OUTPUT_DIR, f'gregobasecorpus-v{__version__}.zip')
    logging.info(f"Compressing the corpus: '{os.path.relpath(target_fn, start=OUTPUT_DIR)}")
    os.rename(source_fn, target_fn)

##

class SQLConverter(object):

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
        try:
            self.db = pymysql.connect(host=db_host, user=db_user, password=db_pass)
        except:
            raise Exception(
                'Could not connect to the mysql database. Are you sure mysql '
                'is running? You can check this by running `mysql -uroot` '
                'which opens mysql (close it using `exit`). If mysql is not '
                'running, start it using `mysql.server start`.'
            )

        self.cursor = self.db.cursor()

        # Set up directories
        self.tmp_dir = os.path.join(OUTPUT_DIR, 'tmp')
        for dir_path in [CSV_DIR, self.tmp_dir]:
            if not os.path.exists(dir_path):
                logging.info(f"Creating directory: '{os.path.relpath(dir_path, start=OUTPUT_DIR)}'")
                os.makedirs(dir_path)

        self.db_structure = db_structure

    def create_db(self):
        logging.info(f"Creating temporary database '{self.db_name}'")
        return self.cursor.execute(f'CREATE DATABASE {self.db_name};')

    def delete_db(self):
        logging.info(f"Deleting temporary database '{self.db_name}'")
        return self.cursor.execute(f'DROP DATABASE {self.db_name};')

    def import_sql(self, filepath):
        rel_path = os.path.relpath(filepath, start=OUTPUT_DIR)
        logging.info(f"Importing sql file into database: '{rel_path}'")
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
            tmp_fn = os.path.join(self.tmp_dir, f'{table_name}.csv')
            target_fn = os.path.join(CSV_DIR, f'{table_name}.csv')
            logging.info(f"Exporting table '{table_name}' to temporary file '{os.path.relpath(target_fn, start=OUTPUT_DIR)}'")
            statement = (
                "SELECT * from {db_prefix}{table_name} INTO OUTFILE '{filepath}' "
                "FIELDS OPTIONALLY ENCLOSED BY '{delimiter}' "
                "TERMINATED BY ',' "
                "LINES TERMINATED BY '\n'"
                ).format(filepath=tmp_fn, 
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
            df = pd.read_csv(tmp_fn,
                            names=names, 
                            dtype=dtypes,
                            sep=',', 
                            escapechar='\\', 
                            quotechar=self.field_delimiter,
                            na_values='N',
                            index_col=0,
                            engine='python')

            df.to_csv(target_fn)

        # Remove temporary directory
        rel_tmp_dir = os.path.relpath(self.tmp_dir, start=OUTPUT_DIR)
        logging.info(f"Removing temporary directory '{rel_tmp_dir}'")
        shutil.rmtree(self.tmp_dir)

    def convert_to_csv(self, filepath):
        """Convert a sql dump of GregoBase into a set of CSV files
        
        Args:
            filepath (str): a path to the .sql file
        """
        self.create_db()
        self.import_sql(filepath)
        try:
            self.export_tables()
        except pymysql.err.InternalError as e:
            if e.args[0] == 1290:
                raise Exception(
                    'Cannot export the MySQL tables because your MySQL server '
                    'is running with the --secure-file-priv option. A possible '
                    'solution is (temporarily) disabling the option in your '
                    '`~/.my.cnf` file and then restarting mysql. This is also '
                    'explained in the file `src/README.md` in the '
                    'GregoBaseCorpus repository.'
                )
            else:
                raise e
        self.delete_db()

##

class CSVConverter(object):
    def __init__(self, db_structure=DB_STRUCTURE):
        """"""
        self.db_structure = db_structure

        # Set up output directories
        if not os.path.exists(GABC_DIR):
            os.makedirs(GABC_DIR)
        if not os.path.exists(HTML_DIR):
            os.makedirs(HTML_DIR)
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
            logging.error(f'Cannot find GABC of chant {chant.name}; skipping...')
            return False

        # First encode to bytes, then decode, also the escaped unicode chars:
        try:
            gabc = gabc.encode('latin1').decode('unicode-escape')
        except:
            logging.error(f'Cannot convert GABC to utf-8 for chant {chant.name}; skipping...')
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
        
        chant = self.chants.loc[idx,:].fillna('')
        metadata = {
            'name': chant.get('incipit'),
            'office-part': chant.get('office_part'),
            'mode': chant.get('mode'),
            'transcriber': chant.get('transcriber'),
            'commentary': chant.get('commentary'),
            'user-notes': chant.get('remarks'),
            'gabc-copyright': 'CC0-1.0 <http://creativecommons.org/publicdomain/zero/1.0/>',
            '_gregobase_corpus_version': __version__,
            '_gregobase_id': idx,
            '_gregobase_url': f'https://gregobase.selapa.net/chant.php?id={idx}',
            '_gregobase_cantus_id': chant.get('cantus_id'),
            '_gregobase_mode_var': chant.get('mode_var')
        }

        # Delete empty fields
        keys = list(metadata.keys())
        for key in keys:
            if metadata[key] == '':
                del metadata[key]
        
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

    def convert_to_gabc(self):
        """Exports all chants to GABC files."""
        logging.info('Exporting chants to GABC files...')
        for idx, chant in self.chants.iterrows():
            body = self.extract_gabc_body(idx)
            if body is not False:
                metadata = self.collect_metadata(idx)
                gabc_path = os.path.join(GABC_DIR, f'{idx:0>5}.gabc')
                
                with open(gabc_path, 'w') as handle:
                    for key, value in metadata.items():
                        attribute = f'{key}:{value};\n'
                        handle.write(attribute)        
                    handle.write("%%\n")
                    handle.write(body)

class GABCConverter(object):
    def __init__(self):
        """"""
        # Set up output directories
        if not os.path.exists(GABC_DIR):
            raise Exception('GABC directory not found')
        if not os.path.exists(CSV_DIR):
            raise Exception('CSV directory not found')
        if not os.path.exists(HTML_DIR):
            os.makedirs(HTML_DIR)

        # Load all csv files
        chants_fn = os.path.join(CSV_DIR, 'chants.csv')
        self.chants = pd.read_csv(chants_fn, index_col=0)

    def convert_to_html(self):
        logging.info('Exporting chants to HTML files...')
        for idx, chant in self.chants.iterrows():
            gabc_path = os.path.join(GABC_DIR, f'{idx:0>5}.gabc')
            html_path = os.path.join(HTML_DIR, f'{idx:0>5}.html')

            if not os.path.exists(gabc_path):
                logging.error(f'GABC file not found: {os.path.relpath(gabc_path, start=OUTPUT_DIR)}')
                continue
            
            try:
                chant = converter.parse(gabc_path,
                    format='gabc', forceSource=True, storePickle=False)
            except Exception as e:
                logging.error(f"Chant {idx} could not be parsed: {e}")
                continue

            chant.toHTML(html_path)
        
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
        """Create a Markdown table describing the structure a database table:
        the columns, what values they take, and so on."""
        columns_to_report = []
        lines = []
        lines.append('| Column       | Type | Description                                        |')
        lines.append('|--------------|------|----------------------------------------------------|')
        for column in self.db_structure[table_name]:
            name = column['name']
            dtype = column['dtype']
            description = column['description']
            lines.append(f'| {name: <12} | {dtype: <4} | {description: <50} |')

        for column in self.db_structure[table_name]:
            if not 'report_value_counts' in column:
                continue
            table = getattr(self, table_name)
            column_name = column['name']
            value_counts = pd.value_counts(table[column_name])
            value_descriptions = column.get('value_descriptions', {})
            title = f'#### Values of `{table_name}.{column_name}`\n'
            if 'value_description_table' in column:
                value_descriptions = getattr(self, column['value_description_table'])
                title = f'#### Frequencies of `{table_name}.{column_name}` values\n'

            lines.append('')
            lines.append(title)
            lines.append('| Value        | Count | Perc. | Description                              |')
            lines.append('|--------------|------:|------:|------------------------------------------|')

            others_count = 0
            other_values = []
            min_freq = column.get('report_min_freq', 0)
            for value, count in value_counts.iteritems():
                perc = count / len(table) * 100

                if perc <= min_freq:
                    others_count += count
                    if 'value_description_table' in column:
                        template = column['value_description_template']
                        description = template.format(description=value_descriptions.loc[value, :])
                        other_values.append(f'`{description}`')
                    else:
                        other_values.append(f'`{value}`')
                    continue

                if 'value_description_table' in column:
                    template = column['value_description_template']
                    description = template.format(description=value_descriptions.loc[value, :])
                else:
                    description = value_descriptions.get(value, '')
                lines.append(f'| {value: <12} | {count: >5} | {perc: >4.0f}% | {description: <40} |')
            
            if others_count > 0:
                perc = others_count / len(table) * 100
                values = ", ".join(other_values)
                lines.append(f'| *others*     | {others_count: >5} | {perc: >4.0f}% | {values} |')


        return '\n'.join(lines)

    def get_changelog(self):
        """Export the changes in changelog.csv as a markdown list"""
        changelog = pd.read_csv(os.path.join(SRC_DIR, 'changelog.csv'))
        new_changes = changelog.query(f'version=={__version__}')
        lines = []
        for i, (version, change) in new_changes.iterrows():
            line = f'- {change}'
            lines.append(line)
        return '\n'.join(lines)

    def write_readme(self, gregobase_export_date="?"):
        """Write the README for a release of the GregoBase Corpus using the 
        template file `readme_template.md`."""
        logging.info('Writing README file...')
        now = datetime.datetime.now()
        corpus_date = now.strftime("%d %B %Y")
        num_gabc_files = len([f for f in os.listdir(GABC_DIR) 
            if os.path.isfile(os.path.join(GABC_DIR,f))])
        num_html_files = len([f for f in os.listdir(HTML_DIR) 
            if os.path.isfile(os.path.join(HTML_DIR,f))])

        template_kws = {
            'version': __version__,
            'chants_structure': self.table_structure('chants'),
            'chant_sources_structure': self.table_structure('chant_sources'),
            'chant_tags_structure': self.table_structure('chant_tags'),
            'tags_structure': self.table_structure('tags'),
            'sources_structure': self.table_structure('sources'),
            'gregobase_export_date': gregobase_export_date,
            'num_gabc_files': num_gabc_files,
            'num_html_files': num_html_files,
            'num_chants': len(self.chants),
            'num_unconvertable': len(self.chants) - num_html_files,
            'num_sources': len(self.sources),
            'num_tags': len(self.tags),
            'corpus_date': corpus_date,
            'changelog': self.get_changelog()
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
    parser.add_argument('--sql', type=str, required=True,
                        help='path the gregobase database dump')
    parser.add_argument('--date', type=str, required=True,
                        help='the date on which gregobase was exported (you can find this in the sql file)')   
    args = parser.parse_args()

    # Clear output_dir before starting logging to that directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Set up logging
    log_fn = os.path.join(OUTPUT_DIR, 'corpus-generation.log')
    logging.basicConfig(filename=log_fn,
                        filemode='w',
                        format='%(levelname)s %(asctime)s %(message)s',
                        datefmt='%d-%m-%y %H:%M:%S',
                        level=logging.INFO)
    logging.info(f'Start generating GregoBase Corpus v{__version__}')
    logging.info(f"> Output directory: '{os.path.relpath(OUTPUT_DIR, start=ROOT_DIR)}'")

    # Go!
    sql = SQLConverter()
    sql.convert_to_csv(filepath=args.sql)

    csv = CSVConverter()
    csv.convert_to_gabc()
    
    gabc = GABCConverter()
    gabc.convert_to_html()

    writer = ReadmeWriter()
    writer.write_readme(gregobase_export_date=args.date)

    compress_corpus()

if __name__ == '__main__':
    # main()

    # sql = SQLConverter()
    # sql.convert_to_csv(filepath='gregobase_dumps/gregobase_20191024.sql')

    # csv = CSVConverter()
    # csv.convert_to_gabc()
    
    # gabc = GABCConverter()
    # gabc.convert_to_html()

    writer = ReadmeWriter()
    writer.write_readme(gregobase_export_date='24 October 2019')
    # compress_corpus()

    