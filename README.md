GregoBaseCorpus
===============

The GregoBaseCorpus is a corpus of Gregorian chant for computational musicology.
It is a research-friendly version of [GregoBase](gregobase.selapa.net/), a
large database of chant transcriptions in the
[GABC format](https://gregorio-project.github.io/gabc/index.html).
This format can be loaded into [`music21`](https://web.mit.edu/music21/), a Python
toolkit for computational musicology, using the library 
[`chant21`](https://github.com/bacor/chant21/).

[**> Download the latest release of the GregoBaseCorpus**](https://github.com/bacor/gregobasecorpus/releases/latest)

[> Read more about the corpus](https://github.com/bacor/gregobasecorpus/tree/master/docs)

> Check out [chant21](https://github.com/bacor/chant21/) and the
[CantusCorpus](https://github.com/bacor/cantuscorpus/), a related plainchant corpus.

Licence
-------

The GregoBaseCorpus (the collection of `.gabc` and `.csv` files)
is released under a [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/)
license, just like [GregoBase itself](https://gregobase.selapa.net/?page_id=2]).
The Python code used to generate the corpus (that is, the code in the `src/`
directory) is released under an MIT license.

Generating the corpus
---------------------

The GregoBase Corpus is created automatically from database dumps of GregoBase.
If you just want to use the corpus, you don't have to regenerate it yourself:
simply download [the latest release](https://github.com/bacor/gregobasecorpus/releases/latest) and you're good to go. But if you want to regenerate the corpus yourself, 
you can of course do so: [read on...](https://github.com/bacor/gregobasecorpus/tree/master/src).