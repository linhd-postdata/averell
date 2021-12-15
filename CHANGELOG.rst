
Changelog
=========

1.2.3 (2021-12-15)
------------------

* Enhanced documentation

1.2.2 (2021-11-13)
------------------

* Added metadata for Zenodo

1.2.1 (2021-07-14)
------------------

* Added two new readers:
    * `Stichotheque Portuguese corpus <https://gitlab.com/stichotheque/stichotheque-pt>`_
    * `Corpus of Czech Verse <https://github.com/versotym/corpusCzechVerse/>`_
* `export_filename` is also returned as an output of `export_corpora`
* Fix writing function so as not to duplicate information
* Change `name` key to `corpus` for clarity
* Fix path split on Windows systems
* Add corpus name to averell output files

1.1.0 (2020-09-18)
------------------

* Added **Biblioteca Italiana (bibit)** reader
* Added Archivio Metrico Italiano info to Biblioteca Italiana reader
* Reduced fixtures file size
* Adding a tmp file to git ignore
* Adding languages and some other cosmetic changes
* Fixing an error with the expected output of the ``averell list`` command
* Adding slugs, langs, and 'all' to ``download`` and ``export``
* Fixing coverage
* Adding documentation and fixing a test

1.0.3 (2020-09-03)
------------------

* Added ``export --filename`` option
* Added two new readers:

  * **For better for verse**

  * **Métrique en ligne**

1.0.2 (2020-06-23)
------------------

* Added two new readers:

  * **ECPA corpus**

  * **Gongocorpus**

* Minor bug fixes

1.0.1 (2020-05-18)
------------------

* Setting up bumbpversion
* Integration with Zenodo

1.0.0 (2020-04-29)
------------------

* Remove commits-since code block
* Adding automated deployments to PyPI on tag releases
* Added menu
* Remove comments and cleaner code fixes
* Fix sorted output of tests
* Added proper documentation and coverage tests
* Added tests for ``export`` function
* Added ``export`` function
* Added ``TEI_NAMESPACE`` as a constant
* Fixed docs. Fixed loads with ``Path``. Fixed logging errors
* Added tests

0.0.1 (2020-01-08)
------------------

* First release on PyPI.
