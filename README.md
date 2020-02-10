GregoBase Corpus
================

The GregoBase Corpus is a corpus of Gregorian chant for computational musicology.
It is a research-friendly version of [GregoBase](gregobase.selapa.net/), a
large database of chant transcriptions in the
[GABC format](https://gregorio-project.github.io/gabc/index.html).
This format can be loaded into [music21](https://web.mit.edu/music21/), a Python
toolkit for computational musicology, using the library `chant21`.

**Usage.**
TODO: example of using the corpus with chant21

**Versions.**
Since new transcriptions are regularly added to GregoBase, we plan to release
new versions of the corpus as well. All releases can be downloaded from GitHub
and can be referenced using Zenodo DOI.

**Licence.**
The GregoBase Corpus (that is, the `.gabc` and `.csv` files) is released under a
[CC0](https://creativecommons.org/publicdomain/zero/1.0/) license (just like
[GregoBase itself](https://gregobase.selapa.net/?page_id=2])).
The Python code used to generate the corpus is released under an MIT license.

**Generating the corpus.**
We generate releases automatically from database dumps of GregoBase. These are
downloaded from the [GregoBase GitHub](https://github.com/gregorio-project/GregoBase/blob/master/gregobase_online.sql) and included in this repository in the directory `gregobase_dumps`. If you wish to generate the corpus yourself, all code and
further instructions can found in the `src` directory.