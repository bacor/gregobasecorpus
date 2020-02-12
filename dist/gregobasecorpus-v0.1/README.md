GregoBase Corpus v0.1
===========================

The GregoBase Corpus is a corpus of Gregorian chant for computational musicology.
It is a research-friendly version of [GregoBase](gregobase.selapa.net/), a
large database of chant transcriptions in the
[GABC format](https://gregorio-project.github.io/gabc/index.html).
This format can be loaded into [music21](https://web.mit.edu/music21/), a Python
toolkit for computational musicology, using the library `chant21`.

| Summary                         |                      |
|---------------------------------|----------------------|
| GregoBase Corpus version        | 0.1                  |
| Corpus generated on             | 10 February 2020     |
| GregoBase exported on           | 24 October 2019      |
| Number of GABC files            | 9130                 |
| Number of chants (`chants.csv`) | 9139                 |
| Number of sources               | 31                   |
| Number of tags                  | 168                  |

License
-------

The GregoBase Corpus is released under a
[CC0](https://creativecommons.org/publicdomain/zero/1.0/) license.

GregoBase is
[also released under this license](https://gregobase.selapa.net/?page_id=2]).
The copyright of chant has been discussed extensively, and (citing 
[the author](https://gregobase.selapa.net/?page_id=18) of GregoBase): "the general consensus is that the books are copyrighted, but not the melodies, except for newly composed ones but there aren’t many of them." 
Please refer to 
[the Gregorio project](https://gregorio-project.github.io/legalissues.html) 
for a more elaborate discussion of the legal issues.


GABC files
----------

All chants are stored as GABC files in the `gabc` directory, named by their id.
The GABC files contain standard header fields (name, mode, office-part, etc.), but also some non-standard fields, starting with an underscore.

| Header field     | Description                                            |
|------------------|--------------------------------------------------------|
| `name`           | The incipit of the chant (somewhat confusingly)        |
| `office-part`    | The office part: the liturgical genre of the chant.    |
| `mode `          | Mode of the chant; see below.                          |
| `transcriber`    | Who transcribed the chant                              |
| `gabc-copyright` | always CC0 for chants in the GregoBase Corpus          |
| `_gregobase_id`  | the id of the chant                                    |
| `_gregobase_url` | url to the gregobase webpage for the chant             |
| `_gregobasecorpus_version` | version of the GregoBase Corpus (should be `0.1`) |

The following fields are only included in the header if their 
values are present in GregoBase:

| Optional header fields        | Description                       |
|-------------------------------|-----------------------------------|
| `commentary`                  | Commentary shown right above the chant (usually source of the words)  |
| `_gregobase_cantus_id`        | The cantus ID                     |
| `_gregobase_mode_var`         | This field contains more mode information; presumably the ending, as the GregoBase site writes: 'the “ending” field is used to put the ending according to Solesmes classification'.        |
| `_gregobase_sources`          | A comma-separated list of source ids for sources the chant appears in |
| `_gregobase_source_[i]_id`    | the id of the i-th source         |
| `_gregobase_source_[i]_title` | the title of the i-th source      |
| `_gregobase_source_[i]_year`  | the year of the i-th source       |
| `_gregobase_tags`             | a comma-separated list of tag ids |
| `_gregobase_tag_[i]_id`       | the id of the i-th tag            |
| `_gregobase_tag_[i]_name`     | the name of the i-th tag          |

Tables
------

### `chants.csv`

Table of chants with all their properties (see also [these desriptions of the fields](https://gregobase.selapa.net/?page_id=18)).

| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | int  | unique id of a chant (also used in naming the gabc files) |
| cantus_id    | str  | Cantus_id of the chant                             |
| version      | str  | Sometimes a chant exists in different versions. The versions currently used are “Vatican” and “Solesmes” according to the presence of rhythmic signs |
| incipit      | str  | Textual incipit                                    |
| initial      | int  | Whether to have a 1 or 2 lines initial or no initial at all |
| office_part  | str  | Usage; also called office part.                    |
| mode         | str  | Mode of the chant. Should be a number or “p” for the “Tonus Peregrinus”. |
| mode_var     | str  | This field contains more mode information; presumably the ending, as the GregoBase site writes: 'the “ending” field is used to put the ending according to Solesmes classification.' |
| transcriber  | str  | Who transcribed the chant.                         |
| commentary   | str  | Commentary that will be placed right above the chant in the PDF. |
| gabc         | str  | The GABC code of the chant.                        |
| gabc_verses  | str  | GABC of the other verses (same melody, different text) |
| tex_verses   | str  | LaTeX code of the other verses, where the place of melodic inflections are indicated in by bold and italic syllables. |
| remarks      | str  | Remarks about for example the transcription.       |

### `chant_sources.csv`

| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| chant_id     | int  | ID of the chant                                    |
| source       | int  | ID of the source                                   |
| page_id      | str  | Page id. Can be a page number or e.g. `[125], 125**` |
| sequence     | int  | Order on the page                                  |
| extent       | int  | The number of pages the chant spans.               |

### `chant_tags.csv`

This table lists the tags associated to every chant. If a chant has
multiple tags, there will be multiple rows in this table with the same `chant_id` (and of course different `tag_id`s).

| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| chant_id     | str  | ID of a chant                                      |
| tag_id       | str  | ID of a tag                                        |

### `tags.csv`

Tag names

| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | int  | ID of the tag                                      |
| tag          | str  | Name of the tag                                    |

### `sources.csv`

| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | int  | ID of the source                                   |
| year         | int  | Year of publication (?) of the source              |
| editor       | str  | Editor of the source                               |
| title        | str  | Title                                              |
| description  | str  | Description of the source                          |
| caption      | str  | Caption (usually with credits) shown above the source images. |
| pages        | str  | List of pages in the source                        |