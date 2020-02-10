import pymysql
import random
import subprocess
import os
import pandas as pd
import shutil

__version__ = '0.1.1'

"""Structure of the Gregobase MySQL database"""
db_structure = {
    'chant_tags': {
        'description': 'Lists the tags associated to each chant. So a certain\
                        chant_id might occur multiple times, once for each of\
                        its tags.',
        'columns': [
            {
                'name': 'chant_id',
                'dtype': int,
                'description': 'ID of a chant'
            },
            {
                'name': 'tag_id',
                'dtype': int,
                'description': 'ID of a tag'
            }
        ]
    },

    'chants': {
        'description': 'Table of chants with all their properties.',
        'columns': [
            {
                'name': 'id',
                'dtype': int,
                'description': 'unique id of a chant'
            },
            { 
                'name': 'cantus_id',
                'dtype': str,
                'description': 'Cantus_id of the chant'
            },
            {
                'name': 'version',
                'dtype': str,
                'description': 'Which version of the chant, e.g. according to \
                                which source?'
            },
            {
                'name': 'incipit',
                'dtype': str,
                'description': 'Textual incipit'
            },
            {
                'name': 'initial',
                'dtype': int,
                'description': '?'
            },
            {
                'name': 'office-part',
                'dtype': str,
                'description': 'Usage or office part.'
            },
            {
                'name': 'mode',
                'dtype': str,
                'description': 'Mode of the chant.'
            },
            {
                'name': 'mode_var',
                'dtype': str,
                'description': 'Not sure; this field appears under the usage in the PDF.'
            },
            {
                'name': 'transcriber',
                'dtype': str,
                'description': 'Who transcribed the chant.'
            },
            {
            'name': 'commentary',
            'dtype': str,
            'description': 'Appears right above the chant in the PDF.'
            },
            {
                'name': 'gabc',
                'dtype': str,
                'description': 'The GABC code of the chant.'
            },
            {
                'name': 'gabc_verses',
                'dtype': str,
                'description': 'GABC of the other verses (same melody, different text)'
            },
            {
                'name': 'tex_verses',
                'dtype': str,
                'description': 'LaTeX code of the other verses, where the place of\
                                melodic inflections are indicated in by bold and\
                                italic syllables.'
            },
            {
                'name': 'remarks',
                'dtype': str,
                'description': 'Remarks about for example the transcription.'
            }
        ]
    },

    'tags': {
        'description': 'Tag names',
        'columns': [
            {
                'name': 'id',
                'dtype': int,
                'description': 'ID of the tag',
            },
            {
                'name': 'tag',
                'dtype': str,
                'description': 'Name of the tag'
            }
        ]
    },
  
    'sources': {
        'description': '',
        'columns': [
            {
                'name': 'id',
                'dtype': int,
                'description': 'ID of the source'
            },
            {
                'name': 'year',
                'dtype': int,
                'description': 'Year of publication (?) of the source'
            },
            {
                'name': 'editor',
                'dtype': str,
                'description': 'Editor of the source'
            },
            {
                'name': 'title',
                'dtype': str,
                'description': 'Title'
            },
            {
                'name': 'description',
                'dtype': str,
                'description': 'Description of the source'
            },
            {
                'name': 'caption',
                'dtype': str,
                'description': 'Caption (usually with credits) shown above the source images.'
            },
            {
                'name': 'pages',
                'dtype': str,
                'description': 'List of pages in the source'
            }
        ]
    },

    'chant_sources': {
        'description': 'Table links chants to sources',
        'columns': [
            {
                'name': 'chant_id',
                'dtype': int,
                'description': 'ID of the chant'
            },
            {
                'name': 'source',
                'dtype': int,
                'description': 'ID of the source'
            },
            {
                'name': 'page_id',
                'dtype': str,
                'description': 'Page id. Can be a page number or e.g. `[125], 125**`'
            },
            {
                'name': 'sequence',
                'dtype': int,
                'description': '???'
            },
            {
                'name': 'extent',
                'dtype': int,
                'description': 'The number of pages the chant spans.'
            }
        ]
    }
}

def randomId(length=5):
    """Return a random alphanumeric string of a given length"""
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(chars) for _ in range(length))

class GregoBaseConverter(object):

    field_delimiter = '@'
    """str: delimiter used in the temporary csv file"""
    
    def __init__(self, db_host='localhost', db_user='root', db_pass='',
        db_prefix='gregobase_', db_structure=db_structure):
        
        # Initialize database
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_prefix = db_prefix
        self.db_name = f'tmp_db_gregocorpus_{randomId()}'
        self.db = pymysql.connect(host=db_host, user=db_user, password=db_pass)
        self.cursor = self.db.cursor()

        # Set up directories
        output_dir = os.path.join('dist', f'gregobasecorpus-v{__version__}')
        self.output_dir = os.path.abspath(output_dir)
        self.csv_dir = os.path.join(self.output_dir, 'csv')
        self.tmp_dir = os.path.join(self.output_dir, 'tmp')

        # Clear 
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        for dir_path in [self.csv_dir, self.tmp_dir]:
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
            structure = self.db_structure[table_name]
            columns = structure['columns']
            dtypes = { col['name']: col['dtype'] for col in columns }
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

            target_fn = os.path.join(self.csv_dir, f'{table_name}.csv')
            df.to_csv(target_fn)

        # Remove temporary directory
        shutil.rmtree(self.tmp_dir)

    def export_db_structure(self, filename='database_structure.md'):
        """Generate a markdown summary of the database structure
        
        Generate a markdown file summarizing the structure of the database: which
        tables it contains, what columns they have and what values they take. All 
        this is specified in the variable `db_structure`.
        
        Args:
            filename (str): the filename
        """
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w') as handle:
            # Header
            header = (
                "Structure of GregoBase Corpus v{version}\n"
                "====================================\n"
                "\n"
                "*Note: This file is automatically generated.*\n\n")
            handle.write(header.format(version=__version__))
            
            for table, structure in self.db_structure.items():
                title = f'Table `{table}.csv`'
                handle.write(f'{title}\n')
                handle.write('-' * len(title) + '\n')
                handle.write(f'{structure["description"]}\n\n')

                handle.write('| Column | Type | Description |\n')
                handle.write('|--|--|--|--|\n')
                for column in structure['columns']:
                    name = column['name']
                    dtype = 'int' if column['dtype'] == int else 'str'
                    desc = column['description']
                    handle.write(f'| {name} | {dtype} | {desc} |\n')

                handle.write('\n\n')

    def convert(self, filepath):
        """Convert a sql dump of GregoBase into a set of CSV files
        
        Args:
            filepath (str): a path to the .sql file
        """
        self.create_db()
        self.import_sql(filepath)
        self.export_tables()
        self.delete_db()
        self.export_db_structure()

class GABCConverter(object):
    def __init__(self, db_structure=db_structure):
        """"""
        self.db_structure = db_structure

        # Set up output directories
        output_dir = os.path.join('dist', f'gregobasecorpus-v{__version__}')
        self.output_dir = os.path.abspath(output_dir)
        self.gabc_dir = os.path.join(self.output_dir, 'gabc')
        if not os.path.exists(self.gabc_dir):
            os.makedirs(self.gabc_dir)

        self.csv_dir = os.path.join(self.output_dir, 'csv')
        if not os.path.exists(self.csv_dir):
            raise Exception('CSV directory not found')

        # Load all csv files
        chants_fn = os.path.join(self.csv_dir, 'chants.csv')
        self.chants = pd.read_csv(chants_fn, index_col=0) 
        chant_sources_fn = os.path.join(self.csv_dir, 'chant_sources.csv')
        self.chant_sources = pd.read_csv(chant_sources_fn, index_col=0)
        chant_tags_fn = os.path.join(self.csv_dir, 'chant_tags.csv')
        self.chant_tags = pd.read_csv(chant_tags_fn, index_col=0)
        sources_fn = os.path.join(self.csv_dir, 'sources.csv')
        self.sources = pd.read_csv(sources_fn, index_col=0)
        tags_fn = os.path.join(self.csv_dir, 'tags.csv')
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
        - ``office-part``
        - ``mode``
        - ``transcriber``
        - ``license`` (non-standard; always CC0 for GregoBase)

        Besides this, we collect all sources and tags associated with a chant. 
        Those gregobase-specific meta-fields all start with the `_gregobase` prefix:

        - ``_gregobase_id``: the id of the chant
        - ``_gregobase_url``: the gregobase webpage for the chant
        - ``_gregocorpus_version`: version of the converter
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
            'office-part': chant['office-part'],
            'mode': chant['mode'],
            'transcriber': chant['transcriber'],
            'licence': 'CC0',
            '_gregobase_url': f'https://gregobase.selapa.net/chant.php?id={idx}',
            '_gregobase_id': idx,
            '_gregobase_corpus_version': __version__,
        }
        if not pd.isnull(chant['commentary']):
            metadata['commentary'] = chant['commentary']

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
        
        for idx, chant in self.chants.head(5).iterrows():
            print(idx)
            body = self.extract_gabc_body(idx)
            if body is not False:
                metadata = self.collect_metadata(idx)
                filepath = os.path.join(self.gabc_dir, filename.format(idx=idx))

                with open(filepath, 'w') as handle:
                    for key, value in metadata.items():
                        attribute = f'{key}:{value};\n'
                        handle.write(attribute)        
                    handle.write("%%\n")
                    handle.write(body)

if __name__ == '__main__':
    converter = GregoBaseConverter()
    # converter.write_db_structure()
    converter.convert('gregobase_online.sql')

    # gabc = GABCConverter()
    
    # gabcConv.convert()

    