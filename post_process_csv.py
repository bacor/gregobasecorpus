"""
To avoid certain issues, the MySQL dumps are exported to a CSV format with
non-standard delimiters (@). These files are then post-processed and turned
into normal csv files with appropriate headings etc. We also generate a
markdown file summarizing the structure of the database tables.
"""

import pandas as pd

"""Structure of the Gregobase MySQL database"""
database_structure = {
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
                'description': '? Values: 0 (152x), 1 (8985x), 2 (2x)'
            },
            {
                'name': 'office-part',
                'dtype': str,
                'description': 'Usage or office part. Values: an (3818x),\
                                hy (792x), al (706x), in (649x), co (640x),\
                                re (501x), of (495x), gr (361x), rb (228x),\
                                ky (220x), tr (203x), va (141x), or (105x),\
                                pr (75x), ps (35x), se (34x), ca (11x),\
                                im (6x)'
            },
            {
                'name': 'mode',
                'dtype': str,
                'description': 'Mode of the chant. Values: 1 (1897x), 8 (1761x),\
                                2 (1009x), 7 (927x), 4 (889x), 6 (685x), 3 (672x),\
                                5 (578x), p (7x), e (7x), d (6x), 0 (3x)'
            },
            {
                'name': 'mode_var',
                'dtype': str,
                'description': '??? This field appears under the usage in the PDF.\
                                Values: g (299x), a (217x), f (156x), d (131x), c (79x), \
                    G (62x), g2 (52x), VIII g (41x), e (40x), a2 (35x), d2 (28x), D (27x), \
                    * a (21x), A* (19x), b (17x), c2 (16x), et 5 (14x), E (14x), V a (8x), \
                    A (8x), I g (8x), * (8x), III (7x), VII c (7x), a* (6x), d* (6x), C (5x), \
                    Per. (5x), VII a (4x), G* (4x), d3 (3x), a3 (3x), g3 (3x), e* (3x), II d (3x), \
                    IV * (3x), F (3x), I a (3x), IV e (3x), II *d (2x), e2 (2x), VI f (2x), \
                    * f (2x), VIIC2 (2x), * c (2x), C2 (2x), et 2 (2x), * d (2x), *a (2x), \
                    VIII a (2x), VII c2 (2x), ? (2x), D2 (2x), I f (1x), a transpos (1x), \
                    a transpos. (1x), D 2 (1x), VIII c (1x), VIII C (1x), IV E (1x), \
                    VII g (1x), Re (1x), 1 (1x), g5 (1x), c 2 (1x), t. irreg (1x), IV (1x), \
                    VI (1x), * e (1x), E2 (1x), d transp (1x), A-star (1x), IV g (1x), et 3 (1x), \
                    II* d (1x), g 2 (1x), a transp. (1x), c transpos (1x), g 3 (1x), e * (1x), \
                    g4 (1x),   (1x), c Transpos (1x), G2 (1x), irreg. (1x), C transp. (1x), \
                    III  (1x)'
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

def post_process_tables(source_dir, target_dir, quotechar="@"):
    """Post-process the CSV files exported by MySQL. 
    
    That mostly means adding
    header rows and making sure the columns have the right datatypes

    Args:
        source_dir (str): The source directory with csv files generated by 
            exporting from MySQL.
        target_dir (str): The target directory where proper csv files will
            be generated in
        quotechar (str, optional): the character used to quote strings. This
            is usually a double quote, but weird errors during export led us 
            to use something else.
    """
    print(f'> Converting to proper CSV files in directory: {target_dir}')
    for table, structure in database_structure.items():
        columns = structure['columns']
        dtypes = { col['name']: col['dtype'] for col in columns }
        names = [ col['name'] for col in columns ]
        df = pd.read_csv(f'{source_dir}{table}.csv', 
                        names=names, 
                        dtype=dtypes,
                        sep=',', 
                        escapechar='\\', 
                        quotechar=quotechar,
                        na_values='N',
                        index_col=0,
                        engine='python')
        target_fn = f'{target_dir}{table}.csv'
        df.to_csv(target_fn)

def export_database_structure_to_markdown(filename):
    """Generate a markdown summary of the database structure
    
    Generate a markdown file summarizing the structure of the database: which
    tables it contains, what columns they have and what values they take. All 
    this is specified in the global variable `GREGOBASE_STRUCTURE` in thne file
    `post_processing.py`. 
    
    Note that it contains some statistics about value frequencies. These do 
    not reflect the current dataset, but were computed separately from an 
    earlier version. They are a good indication of value frequencie, however.
    
    Args:
        filename (str): the filename
    """
    print(f'> Generating markdown file with database structure: {filename}')

    with open(filename, 'w') as handle:
        # Header
        handle.write('Structure of GregoBase database\n')
        handle.write('===============================\n')
        handle.write('Below a summary of the relevant tables. This file is \n')
        handle.write('automatically generated in `post_process_sql_dump.py`.\n')
        handle.write('**Note**: value frequencies were computed on an older '
                    +'version of the dataset and may be inaccurate.\n\n')
        
        for table, structure in database_structure.items():
            title = f'Table `{table}`'
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
            
if __name__ == '__main__':
    post_process_tables(source_dir='_tmp_mysql_export/', target_dir='csv/')
    export_database_structure_to_markdown(filename='database_structure.md')