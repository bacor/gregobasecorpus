Generating the corpus
=====================

Below you find instructions for generating the corpus.
If you just want to use the corpus, simply download one of the releases:
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

* **Python.**
    The corpus is generated using a Python script. You can find the Python 
    version used in `.python-version` and the dependencies in 
    `requirements.txt`. If you use `pyenv` and `venv` to manage 
    python versions and virtual environments:

    ```bash
    # Install the right python version
    pyenv install | cat .python-version

    # Create a virtual environment
    python -m venv env

    # Activate the environment
    source env/bin/activate

    # Install dependencies
    pip install -r requirements.txt
    ```

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

Possible issues
---------------

The way the MySQL database is used can give rise to some issues. In particular, 
the tables cannot be exported when the MySQL server is running with the 
`--secure-file-priv` option enabled. You can check whether this is enabled
by running `mysql> SHOW VARIABLES LIKE "securefilepriv";`. 
You can (temporarily) disable the option in your configuration file: add

```
[mysqld]

secure_file_priv = ''
```

to `~/.my.cnf`, restart mysql using `$ mysql.server restart`, and try agian.
(See also [here](https://medium.com/@andrewpongco/solving-the-mysql-server-is-running-with-the-secure-file-priv-option-so-it-cannot-execute-this-d319de864285) or [here](https://dba.stackexchange.com/questions/123290/error-secure-file-priv-option-when-save-selection-to-csv).)

License
-------

The code for generating the corpus is released under an MIT license; see `src/LICENCE`.
Note that the GregoBase Corpus itself (that is, the collection of `.gabc` and `.csv` 
files) is released under a different license (CC0).