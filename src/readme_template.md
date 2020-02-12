GregoBase Corpus v{version}
===========================

The GregoBase Corpus is a corpus of Gregorian chant for computational musicology.
It is a research-friendly version of [GregoBase](gregobase.selapa.net/), a
large database of chant transcriptions in the
[GABC format](https://gregorio-project.github.io/gabc/index.html).
This format can be loaded into [music21](https://web.mit.edu/music21/), a Python
toolkit for computational musicology, using the library `chant21`.

| Summary                          |                      |
|----------------------------------|----------------------|
| GregoBase Corpus version         | {version: <20} |
| Corpus generated on              | {corpus_date: <20} |
| GregoBase exported on            | {gregobase_export_date: <20} |
| Number of chants in `chants.csv` | {num_chants: <20} |
| Number of GABC files             | {num_gabc_files: <20} |
| Number of unconverted chants     | {num_unconverted: <20}|
| Number of sources                | {num_sources: <20} |
| Number of tags                   | {num_tags: <20} |

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
The GABC files contain standard header fields (name, mode, office-part, etc.),
but also some non-standard fields, all starting with an underscore.
Note that only non-empty fields are included. Fields that are always present in
this corpus are indicated with an asterisk (*).

| Header field                  | * | Description                                        |
|-------------------------------|---|----------------------------------------------------|
| `name`                        |   |The incipit of the chant (somewhat confusingly)     |
| `office-part`                 |   |The office part: the liturgical genre of the chant. |
| `mode `                       |   |Mode of the chant; see below.                       |
| `transcriber`                 |   | Who transcribed the chant                          |
| `commentary`                  |   | Commentary shown above the chant (often the text source) |
| `user-notes`                  |   | Remarks by the transcriber                         |
| `gabc-copyright`              | * | License: CC0 for chants in the GregoBase Corpus    |
| `_gregobasecorpus_version`    | * | version of the GregoBase Corpus (`{version}`)      |
| `_gregobase_id`               | * | the id of the chant                                |
| `_gregobase_url`              | * | url to the gregobase webpage for the chant         |
| `_gregobase_cantus_id`        |   | the cantus ID                                      |
| `_gregobase_mode_var`         |   | This field contains more mode information; presumably the ending, as the GregoBase site writes: 'the “ending” field is used to put the ending according to Solesmes classification'. |
| `_gregobase_sources`          |   | a comma-separated list of source ids for sources the chant appears in |
| `_gregobase_source_[i]_id`    |   | the id of the i-th source                          |
| `_gregobase_source_[i]_title` |   | the title of the i-th source                       |
| `_gregobase_source_[i]_year`  |   | the year of the i-th source                        |
| `_gregobase_tags`             |   | a comma-separated list of tag ids                  |
| `_gregobase_tag_[i]_id`       |   | the id of the i-th tag                             |
| `_gregobase_tag_[i]_name`     |   | the name of the i-th tag                           |

Tables
------

### Table `chants.csv`

Table of chants with all their properties (see also [these desriptions of the fields](https://gregobase.selapa.net/?page_id=18)).

{chants_structure}

### Table `chant_sources.csv`

{chant_sources_structure}

### Table `chant_tags.csv`

This table lists the tags associated to every chant. If a chant has
multiple tags, there will be multiple rows in this table with the same `chant_id` (and of course different `tag_id`s).

{chant_tags_structure}

### Table `tags.csv`

Tag names

{tags_structure}

### Table `sources.csv`

{sources_structure}

Changelog v{version}
-------------------

{changelog}
