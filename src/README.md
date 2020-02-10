Generating the corpus
=====================

Below you find instructions for generating the corpus.
If you only want to use the corpus, just download one of the releases:
you don't have to regenerate it yourself.

Requirements
------------

* **GregoBase mysql dump**
    A dump of the GregoBase database from the `gregobase_dumps` directory.
    More recent versions can (perhaps) be downloaded from
    from [GitHub](https://github.com/gregorio-project/GregoBase). Look for
    the file `gregobase_online.sql`.

* **MySQL.**
    Make sure you have a ``mysql`` installation with root access.
    (On MacOS, you could use ``brew`` to install it: ``brew install mysql``).
    You can check this by running ``mysql -uroot`` which opens mysql. You
    can close it using ``exit``. If you get an error
    `Can't connect to local MySQL server through socket`, your server is
    probably not running. Start it using ``mysql.server start``.

* **Python with pandas**
    The postprocessing of the csv files is done using Pandas.
    You can install it using `pip install pandas`.

Overview
--------

The script `generate_corpus.py` first imports the MySQL dump into a temporary
mysql database. Then it exports it to temporary CSV files, which are cleant up
and converted to the final CSV files. Next, the chants in `chants.csv` stored as
separate GABC files with relevant metadata stored in their headers. Finally,
a README file is generated, and the corpus is compressed. During generation, the
script creates a directory like `dist/gregobasecorpus-v1.0` in which all data is 
stored. This is the directory that is compressed and released.

Usage
-----

To generate the corpus, run for example:

```bash
$ cd src/
$ python generate_corpus.py \
    --sql=../gregobase_dumps/gregobase_20191024.sql \
    --date='24 October 2019'
```

The `--date` argument is the date at which the SQL dump was generated. This can be
found in the SQL file. (We could also extract it automatically, but this is easier).