Generating the corpus
=====================

To generate the corpus, pass the mysql dump to ``generate_corpus.sh``::

    bash generate_corpus.sh gregobase_online.sql >> generation.log


Requirements
------------

* **GregoBase mysql dump** 
    A dump of the GregoBase database: ``gregobase_online.sql``.
    More recent versions can (perhaps) be downloaded from
    from GitHub: https://github.com/gregorio-project/GregoBase

* **MySQL.** 
    Make sure you have a ``mysql`` installation with root access.
    (On MacOS, you could use ``brew`` to install it: ``brew install mysql``).
    You can check this by running ``mysql -uroot`` which opens mysql. You
    can close it using ``exit``. If you get an error 
    `Can't connect to local MySQL server through socket`, your server is 
    probably not running. Start it using ``mysql.server start``.

* **Python with Pandas**
    The postprocessing of the csv files is done using Pandas. 
    You can install it using `pip install pandas`. 


1. Converting MySQL to CSV
--------------------------

The mysql database dump is converted to intermediate CSV files (using
weird delimiters to avoid certain issues). The script 
``generate_corpus.sh`` creates a temporary mysql database, imports the
database dump, exports all tables, and removes the database again.
This script also runs step 2 and 3, since it has to clean up the temporary
directories afterwards.


2. Post-processing CSV files
----------------------------

.. automodule:: post_process_csv
   :members:

3. Exporting chants to GABC
---------------------------

.. automodule:: generate_gabc_files
   :members:

