"""Generate gabc files for every chant in the `chants.csv` file.
"""
import pandas as pd
import json
import warnings
__version__ = '0.1.2'

def extract_gabc_body(chant):
    """Extract the gabc body of a chant from the chants table
    
    Args:
        chants (pd.DataFrame): The chants dataframe
        idx (int): the id of the chant
    
    Raises:
        Exception: when the chant does not have gabc
        Exception: when the encoding can't be converted to utf-8
    
    Returns:
        str: A gabc string
    """
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

def collect_metadata(idx, chants, chant_tags, chant_sources, sources, tags):
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
    chant = chants.loc[idx,:]
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
    source_ids = chant_sources.query(f'chant_id=={idx}')['source']
    if len(source_ids) > 0:
        metadata['_gregobase_sources'] = ",".join(str(i) for i in source_ids)
        for i, source_id in enumerate(source_ids):
            source = sources.loc[source_id, :]
            metadata[f'_gregobase_source_{i}_id'] = source_id
            metadata[f'_gregobase_source_{i}_title'] = source["title"]
            metadata[f'_gregobase_source_{i}_year'] = source["year"]

    # Add all tags associated to the chant
    tag_ids = chant_tags.query(f'chant_id=={idx}')['tag_id']
    if len(tag_ids) > 0:
        metadata['_gregobase_tags'] = ",".join(str(i) for i in tag_ids)
        for i, tag_id in enumerate(tag_ids):
            tag = tags.loc[tag_id, :]
            metadata[f'_gregobase_tag_{i}_id'] = tag_id
            metadata[f'_gregobase_tag_{i}_name'] = tag['tag']

    return metadata

def export_chants_to_gabc_files(chants, chant_tags, chant_sources, sources, tags,
    filepath='gabc/{idx:0>5}.gabc'):
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
    
    for idx, chant in chants.iterrows():
        body = extract_gabc_body(chant)
        if body is not False:
            metadata = collect_metadata(idx, chants, chant_tags, chant_sources, sources, tags)
            filename = filepath.format(idx=idx)

            with open(filename, 'w') as handle:
                for key, value in metadata.items():
                    attribute = f'{key}:{value};\n'
                    handle.write(attribute)        
                handle.write("%%\n")
                handle.write(body)

if __name__ == '__main__':
    chants = pd.read_csv('csv/chants.csv', index_col=0)
    chant_sources = pd.read_csv('csv/chant_sources.csv', index_col=0)
    chant_tags = pd.read_csv('csv/chant_tags.csv', index_col=0)
    sources = pd.read_csv('csv/sources.csv', index_col=0)
    tags = pd.read_csv('csv/tags.csv', index_col=0)
    
    export_chants_to_gabc_files(chants,
        chant_tags, chant_sources, sources, tags)
