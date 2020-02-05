Structure of GregoBase database
===============================
Below a summary of the relevant tables. This file is 
automatically generated in `post_process_sql_dump.py`.
**Note**: value frequencies were computed on an older version of the dataset and may be inaccurate.

Table `chant_tags`
------------------
Lists the tags associated to each chant. So a certain                        chant_id might occur multiple times, once for each of                        its tags.

| Column | Type | Description |
|--|--|--|--|
| chant_id | int | ID of a chant |
| tag_id | int | ID of a tag |


Table `chants`
--------------
Table of chants with all their properties.

| Column | Type | Description |
|--|--|--|--|
| id | int | unique id of a chant |
| cantus_id | str | Cantus_id of the chant |
| version | str | Which version of the chant, e.g. according to                                 which source? |
| incipit | str | Textual incipit |
| initial | int | ? Values: 0 (152x), 1 (8985x), 2 (2x) |
| office-part | str | Usage or office part. Values: an (3818x),                                hy (792x), al (706x), in (649x), co (640x),                                re (501x), of (495x), gr (361x), rb (228x),                                ky (220x), tr (203x), va (141x), or (105x),                                pr (75x), ps (35x), se (34x), ca (11x),                                im (6x) |
| mode | str | Mode of the chant. Values: 1 (1897x), 8 (1761x),                                2 (1009x), 7 (927x), 4 (889x), 6 (685x), 3 (672x),                                5 (578x), p (7x), e (7x), d (6x), 0 (3x) |
| mode_var | str | ??? This field appears under the usage in the PDF.                                Values: g (299x), a (217x), f (156x), d (131x), c (79x),                     G (62x), g2 (52x), VIII g (41x), e (40x), a2 (35x), d2 (28x), D (27x),                     * a (21x), A* (19x), b (17x), c2 (16x), et 5 (14x), E (14x), V a (8x),                     A (8x), I g (8x), * (8x), III (7x), VII c (7x), a* (6x), d* (6x), C (5x),                     Per. (5x), VII a (4x), G* (4x), d3 (3x), a3 (3x), g3 (3x), e* (3x), II d (3x),                     IV * (3x), F (3x), I a (3x), IV e (3x), II *d (2x), e2 (2x), VI f (2x),                     * f (2x), VIIC2 (2x), * c (2x), C2 (2x), et 2 (2x), * d (2x), *a (2x),                     VIII a (2x), VII c2 (2x), ? (2x), D2 (2x), I f (1x), a transpos (1x),                     a transpos. (1x), D 2 (1x), VIII c (1x), VIII C (1x), IV E (1x),                     VII g (1x), Re (1x), 1 (1x), g5 (1x), c 2 (1x), t. irreg (1x), IV (1x),                     VI (1x), * e (1x), E2 (1x), d transp (1x), A-star (1x), IV g (1x), et 3 (1x),                     II* d (1x), g 2 (1x), a transp. (1x), c transpos (1x), g 3 (1x), e * (1x),                     g4 (1x),   (1x), c Transpos (1x), G2 (1x), irreg. (1x), C transp. (1x),                     III  (1x) |
| transcriber | str | Who transcribed the chant. |
| commentary | str | Appears right above the chant in the PDF. |
| gabc | str | The GABC code of the chant. |
| gabc_verses | str | GABC of the other verses (same melody, different text) |
| tex_verses | str | LaTeX code of the other verses, where the place of                                melodic inflections are indicated in by bold and                                italic syllables. |
| remarks | str | Remarks about for example the transcription. |


Table `tags`
------------
Tag names

| Column | Type | Description |
|--|--|--|--|
| id | int | ID of the tag |
| tag | str | Name of the tag |


Table `sources`
---------------


| Column | Type | Description |
|--|--|--|--|
| id | int | ID of the source |
| year | int | Year of publication (?) of the source |
| editor | str | Editor of the source |
| title | str | Title |
| description | str | Description of the source |
| caption | str | Caption (usually with credits) shown above the source images. |
| pages | str | List of pages in the source |


Table `chant_sources`
---------------------
Table links chants to sources

| Column | Type | Description |
|--|--|--|--|
| chant_id | int | ID of the chant |
| source | int | ID of the source |
| page_id | str | Page id. Can be a page number or e.g. `[125], 125**` |
| sequence | int | ??? |
| extent | int | The number of pages the chant spans. |


