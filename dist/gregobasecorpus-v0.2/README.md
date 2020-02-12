GregoBase Corpus v0.2
===========================

The GregoBase Corpus is a corpus of Gregorian chant for computational musicology.
It is a research-friendly version of [GregoBase](gregobase.selapa.net/), a
large database of chant transcriptions in the
[GABC format](https://gregorio-project.github.io/gabc/index.html).
This format can be loaded into [music21](https://web.mit.edu/music21/), a Python
toolkit for computational musicology, using the library `chant21`.

| Summary                          |                      |
|----------------------------------|----------------------|
| GregoBase Corpus version         | 0.2                  |
| Corpus generated on              | 12 February 2020     |
| GregoBase exported on            | 24 October 2019      |
| Number of chants in `chants.csv` | 9139                 |
| Number of GABC files             | 9130                 |
| Number of unconverted chants     | 9                   |
| Number of sources                | 31                   |
| Number of tags                   | 168                  |

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
| `_gregobasecorpus_version`    | * | version of the GregoBase Corpus (`0.2`)      |
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

| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | int  | unique id of a chant (also used in naming the gabc files) |
| cantus_id    | str  | Cantus_id of the chant                             |
| version      | str  | Sometimes a chant exists in different versions. The versions currently used are “Vatican” and “Solesmes” according to the presence of rhythmic signs |
| incipit      | str  | Textual incipit                                    |
| initial      | int  | Whether to have a 1 or 2 lines initial or no initial at all |
| office_part  | str  | Usage or office part, using a two-letter abbreviation (see values) |
| mode         | str  | Mode of the chant. Should be a number or “p” for the “Tonus Peregrinus” (see values). |
| mode_var     | str  | This field contains more mode information; presumably the ending, as the GregoBase site writes: 'the “ending” field is used to put the ending according to Solesmes classification.' |
| transcriber  | str  | Who transcribed the chant.                         |
| commentary   | str  | Commentary that will be placed right above the chant in the PDF. |
| gabc         | str  | The GABC code of the chant.                        |
| gabc_verses  | str  | GABC of the other verses (same melody, different text) |
| tex_verses   | str  | LaTeX code of the other verses, where the place of melodic inflections are indicated in by bold and italic syllables. |
| remarks      | str  | Remarks about for example the transcription.       |

#### Values of `chants.office_part`

| Value        | Count | Perc. | Description                              |
|--------------|------:|------:|------------------------------------------|
| an           |  3818 |   42% | antiphona                                |
| hy           |   792 |    9% | hymnus                                   |
| al           |   706 |    8% | alleluia                                 |
| in           |   649 |    7% | introitus                                |
| co           |   640 |    7% | communio                                 |
| re           |   501 |    5% | responsorium                             |
| of           |   495 |    5% | offertorium                              |
| gr           |   361 |    4% | graduale                                 |
| rb           |   228 |    2% | responsorium brevis                      |
| ky           |   220 |    2% | kyriale                                  |
| tr           |   203 |    2% | tractus                                  |
| va           |   141 |    2% | varia                                    |
| or           |   105 |    1% | toni communes                            |
| pr           |    75 |    1% | praefationes                             |
| ps           |    35 |    0% | psalmus                                  |
| se           |    34 |    0% | sequentia                                |
| ca           |    11 |    0% | canticum                                 |
| im           |     6 |    0% | improperia                               |

#### Values of `chants.mode`

| Value        | Count | Perc. | Description                              |
|--------------|------:|------:|------------------------------------------|
| 1            |  1897 |   21% | dorian authentic                         |
| 8            |  1761 |   19% | mixolydian plagal or hypomixolydian      |
| 2            |  1009 |   11% | dorian plagal or hypodorian              |
| 7            |   927 |   10% | mixolydian authentic                     |
| 4            |   889 |   10% | phrygian plagal or hypophrygian          |
| 6            |   685 |    7% | lydian plagal or hypolydian              |
| 3            |   672 |    7% | phrygian authentic                       |
| 5            |   578 |    6% | lydian authentic                         |
| e            |     7 |    0% |                                          |
| p            |     7 |    0% | tonus peregrinus                         |
| d            |     6 |    0% |                                          |
| 0            |     3 |    0% |                                          |

#### Values of `chants.mode_var`

| Value        | Count | Perc. | Description                              |
|--------------|------:|------:|------------------------------------------|
| g            |   299 |    3% |                                          |
| a            |   217 |    2% |                                          |
| f            |   156 |    2% |                                          |
| d            |   131 |    1% |                                          |
| c            |    79 |    1% |                                          |
| G            |    62 |    1% |                                          |
| g2           |    52 |    1% |                                          |
| *others*     |   437 |    5% | `VIII g`, `e`, `a2`, `d2`, `D`, `* a`, `A*`, `b`, `c2`, `E`, `et 5`, `A`, `*`, `I g`, `V a`, `III`, `VII c`, `a*`, `d*`, `Per.`, `C`, `G*`, `VII a`, `d3`, `g3`, `a3`, `e*`, `I a`, `IV *`, `F`, `II d`, `IV e`, `?`, `C2`, `VIII a`, `* d`, `VIIC2`, `* c`, `et 2`, `VII c2`, `e2`, `VI f`, `*a`, `* f`, `II *d`, `D2`, `c 2`, `D 2`, `C transp.`, `* e`, `c Transpos`, `II* d`, `VIII C`, ` `, `a transpos.`, `g5`, `IV g`, `VI`, `VII g`, `a transpos`, `c transpos`, `E2`, `G2`, `g 2`, `III `, `e *`, `g 3`, `A-star`, `t. irreg`, `d transp`, `1`, `I f`, `g4`, `IV E`, `et 3`, `a transp.`, `irreg.`, `IV`, `Re`, `VIII c` |

### Table `chant_sources.csv`

| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| chant_id     | int  | ID of the chant                                    |
| source       | int  | ID of the source                                   |
| page_id      | str  | Page id. Can be a page number or e.g. `[125], 125**` |
| sequence     | int  | Order on the page                                  |
| extent       | int  | The number of pages the chant spans.               |

#### Frequencies of `chant_sources.source` values

| Value        | Count | Perc. | Description                              |
|--------------|------:|------:|------------------------------------------|
| 3            |  2156 |   22% | The Liber Usualis (1961)                 |
| 11           |  1816 |   18% | Antiphonarium O.P. (Gillet) (1933)       |
| 2            |  1529 |   15% | Graduale Romanum (1961)                  |
| 1            |  1083 |   11% | Graduale Romanum (1908)                  |
| 7            |   943 |   10% | Antiphonale Monasticum (1934)            |
| 14           |   930 |    9% | Graduale O.P. (Suarez) (1950)            |
| 17           |   252 |    3% | Antiphonale monasticum I (2005)          |
| 6            |   210 |    2% | Antiphonale Romanum II (2009)            |
| *others*     |  1004 |   10% | `Cantus selecti (1957)`, `Chants of the Church (1956)`, `Liber Hymnarius (1983)`, `Graduale Romanum (1974)`, `Antiphonale Romanum (1912)`, `Cantus varii romano-seraphici (1902)`, `Nocturnale Romanum (2002)`, `Antiphonale monasticum III (2007)`, `Graduale simplex (1975)`, `Hymnarium Cisterciense (1909)`, `Psalterium Monasticum (1981)`, `Gregorian Missal (1990)`, `Completorium O.P. (Suarez) (1949)`, `Officium Hebdomadæ Sanctæ O.P. (Fernandez) (1965)`, `Processionarium O.P. (Cormier) (1913)`, `Graduale Cisterciense (1934)`, `Antiphonale monasticum II (2006)`, `Matutinum O.P. (Gillet) (1936)`, `Antiphonarium Cisterciense (1947)`, `Les Heures Grégoriennes III (2008)`, `In nocte nativitatis Domini (1963)` |

### Table `chant_tags.csv`

This table lists the tags associated to every chant. If a chant has
multiple tags, there will be multiple rows in this table with the same `chant_id` (and of course different `tag_id`s).

| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| chant_id     | str  | ID of a chant                                      |
| tag_id       | str  | ID of a tag                                        |

#### Frequencies of `chant_tags.tag_id` values

| Value        | Count | Perc. | Description                              |
|--------------|------:|------:|------------------------------------------|
| 6            |   134 |   28% | Tempus Adventus                          |
| 14           |    22 |    5% | Completorium                             |
| 157          |    17 |    4% | Lingua Polonica                          |
| 135          |    15 |    3% | Tonus sollemnis                          |
| 117          |    14 |    3% | Caecilia Nocturnale Romanum              |
| 42           |    12 |    3% | In honorem SS. Sacramenti                |
| 55           |    11 |    2% | PRÆPARATIO ad Festum Nativitatis D. N. J. C. |
| 37           |     9 |    2% | Ad vesperas                              |
| 29           |     8 |    2% | Quadragesima                             |
| 9            |     7 |    1% | Trinity Sunday                           |
| 154          |     7 |    1% | In honorem SS. Cordis Jesu               |
| 10           |     6 |    1% | Pentecost                                |
| 111          |     6 |    1% | missa regia henrico du mont              |
| 103          |     6 |    1% | Ad Vigilias                              |
| 122          |     6 |    1% | Missa Regia                              |
| 104          |     6 |    1% | Ad Laudes                                |
| 56           |     5 |    1% | In Honorem Nativitatis D. N. J. C.       |
| 53           |     5 |    1% | In Honorem B. M. V. Immaculatæ.          |
| 70           |     5 |    1% | IN HONOREM S. COLETÆ.                    |
| 51           |     5 |    1% | In dedicatione S. Michaelis Archangeli   |
| 81           |     5 |    1% | IN HONOREM S. BERNARDINI SENENSIS.       |
| 120          |     5 |    1% | Saint Hildegard                          |
| 138          |     5 |    1% | In I Vesperis                            |
| *others*     |   157 |   33% | `Sabbato sancto, in vigilia paschæ`, `Ad Tertiam`, `Ad Sextam`, `Ad Nonam`, `In Ascensione Domini`, `In Nativitate Domini`, `Ad benedictionem Ss. Sacramenti`, `Tempore Paschali`, `Feria III ad vesperas`, `IN EPIPHANIA D. N. J. C.`, `In Feriis extra Tempus Paschale`, `IN HONOREM SS. CRUCIS D. N. J. C.`, `IN HONOREM SS. V. PROTOMARTYRUM ORDINIS.`, `IN HONOREM SANCTÆ AGNETIS.`, `IN HONOREM S. AUGUSTINI.`, `IN HONOREM SS. NOMINIS JESU.`, `invitatorium`, `IN HONOREM S. JOANNIS EVANGEL.`, `In Festo SS. Innocentium`, `Per Annum`, `IN HONOREM S. CATHARINÆ BONON.`, `Tempore Paschali in Feriis et Semiduplicibus et infra`, `Ad ritum initialis`, `In honorem B. Mariae V.`, `In Festo Duplici.`, `In Dominicis Adventus et Quadragesimæ`, `Tonus orationis`, `Tonus simplex`, `In II Vesperis`, `Paschaltide`, `In Festis I et II classis B. Mariæ V. et in die Oct. solemni ejusdem.`, `ORDO EXSEQUIARUM`, `IN HONOREM S. STEPHANI.`, `Die 4 Aug. - S. P. Dominici Conf.`, `Feria IV ad vesperas`, `In Vigilia Epiphaniæ.`, `B. M. V. Omnium Gratiarum Mediat.`, `IN HONOREM S. MICHAELIS ARCHANGELI.`, `IN CONVERSIONE S. PAULI.`, `in dominicis et festis`, `IN HONOREM S. MARGARITÆ DE CORTONA.`, `In Festo Toto Duplici`, `In Festis II classis adhibetur sequens`, `(Per Annum)`, `præterquam Tempore Paschali, et infra Octavas Solemnes et supra`, `In Festo Semiduplici et infra.`, `Dominica ad I vesperas`, `ritual`, `IN HONOREM S. THOMÆ.`, `Sabbato ad vesperas`, `In festivitate omnium sanctorum`, `In festo D.N. Jesu Christi Regis`, `Feria VI ad vesperas`, `Sequentia`, `In Assumptione B. Mariæ Virginis`, `IN FERIIS VI. QUADRAGESIMÆ.`, `Feria II ad vesperas`, `Christmas Matins Invitatory`, `Ad invitatorium`, `B. V. MARIA ET SS. CRUX D. N. J. C.`, `In Praesentatione Domini`, `Commune Apostolorum`, `Missa pro pace`, `In Epiphania Domini`, `Ad Missam vigiliae paschalis`, `Feria V in Cena Domini`, `Veni Creator`, `Dominica prima quadragesime`, `BMV Claromontanæ Częstochoviensis`, `Annuntiatione Dómini`, `Dominica tertia quadragesime`, `In Honorem S. Antonii`, `Ad benedictionem`, `In Honorem S. Petri de Alcantara`, `Mariae Magdalenae`, `Reproaches`, `Credidi`, ` Inclinavit Dominus`, `Nos qui vivimus`, `Sæpe expungaverunt me`, `Sana animam`, `Ecce quam bonum`, `S. MATTHÆI, APOSTOLI ET EVANGELISTÆ`, `Ad benedictionem sollemnem`, `Tonus Evangelii`, `IN HONOREM SS. RESURRECTIONIS D. N. J. C.`, `Most solemn tone`, `In resurrectione Christi.`, `AD HONOREM B. M. V.`, `IN RESURRECTIONE D. N. J. C.`, `IN FESTIS SS. CRUCIS D. N. J. C.`, `IN HONOREM S. PASCHALIS BAYLON.`, `IN HONOREM TRANSLATIONIS S. P. N. FRANCISCI.`, `IN HONOREM SS. TRINITATIS.`, `Compline, Short Responsory`, `Tractus`, `Sabbato ad Laudes`, `Adventus`, `In Purificatione B. Mariae Virginis (2. Febr.)`, `DE VIGILIA PRO DEFUNCTO`, `Introitus, Lent`, `Hebdomada Sancta`, `Tempore Natalis Domini`, `Ad I Vesperas`, `in sollemnitatibus`, `Cisterciensis`, `Responsorium breve`, `Feria II ad primam`, `Litaniae`, `Tempore Paschali In Honorem BMV` |

### Table `tags.csv`

Tag names

| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | int  | ID of the tag                                      |
| tag          | str  | Name of the tag                                    |

### Table `sources.csv`

| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | int  | ID of the source                                   |
| year         | int  | Year of publication (?) of the source              |
| editor       | str  | Editor of the source                               |
| title        | str  | Title                                              |
| description  | str  | Description of the source                          |
| caption      | str  | Caption (usually with credits) shown above the source images. |
| pages        | str  | List of pages in the source                        |

Changelog v0.2
-------------------

- Added value-frequencies for certain fields (office-part, mode, sources, tags) to README.
- Improve GABC headers: only include non-empty metadata fields
- Add changelog to README
