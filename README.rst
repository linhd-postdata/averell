=======
Averell
=======

.. start-badges

.. image:: https://img.shields.io/pypi/v/averell.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/averell

.. image:: https://api.travis-ci.org/linhd-postdata/averell.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/linhd-postdata/averell

.. image:: https://readthedocs.org/projects/averell/badge/?version=latest
    :target: https://averell.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://zenodo.org/badge/232539126.svg
    :target: https://zenodo.org/badge/latestdoi/232539126
    :alt: Zenodo DOI

.. end-badges

Averell, the python library and command line interface that facilitates working
with existing repositories of annotated poetry. \
Averell is able to download an annotated corpus and reconcile different
TEI entities to provide a unified JSON output at the desired granularity.
That is, for their investigations some researchers
might need the entire poem, poems split line by line,
or even word by word if that is available. Averell allows to specify the
granularity of the final generated dataset, which is a combined JSON with all
the entities in the selected corpora.
Each corpus in the catalog must specify the parser to produce the expected data format.

* Free software: Apache Software License 2.0


Available corpora (version 1.1.0)
=================================

====  ===================  ======  ======  ======  ========  =============  ===========
  id  name                 lang    size      docs     words  granularity    license
====  ===================  ======  ======  ======  ========  =============  ===========
   1  Disco V2.1           es      22M       4088    381539  stanza         CC-BY
      (disco2_1)                                             line
   2  Disco V3             es      28M       4080    377978  stanza         CC-BY
      (disco3)                                               line
   3  Sonetos Siglo        es      6.8M      5078    466012  stanza         CC-BY-NC
      de Oro                                                 line           4.0
      (adso)
   4  ADSO 100             es      128K       100      9208  stanza         CC-BY-NC
      poems corpus                                           line           4.0
      (adso100)
   5  Poesía Lírica        es      3.8M       475    299402  stanza         CC-BY-NC
      Castellana Siglo                                       line           4.0
      de Oro                                                 word
      (plc)                                                  syllable
   6  Gongocorpus (gongo)  es      9.2M       481     99079  stanza         CC-BY-NC-ND
                                                             line           3.0
                                                             word           FR
                                                             syllable
   7  Eighteenth Century   en      2400M     3084   2063668  stanza         CC
      Poetry Archive                                         line           BY-SA
      (ecpa)                                                 word           4.0
   8  For Better           en      39.5M      103     41749  stanza         Unknown
      For Verse                                              line
      (4b4v)
   9  Métrique en          fr      183M      5081   1850222  stanza         Unknown
      Ligne (mel)                                            line
  10  Biblioteca Italiana  it      242M     25341   7121246  stanza         Unknown
      (bibit)                                                line
                                                             word
  11  Corpus of            cs      4100M    66428  12636867  stanza         CC-BY-SA
      Czech Verse                                            line
      (czverse)                                              word
  12  Stichotheque         pt      11.8M     1702    168411  stanza         Unkwown
      (stichopt)                                             line
====  ===================  ======  ======  ======  ========  =============  ===========


Documentation
=============

https://averell.readthedocs.io/

Installation
============

To install averell, run this command in your terminal::

    pip install averell

This is the preferred method to install averell, as it will always install
the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Usage
=====

Check `usage page <https://averell.readthedocs.io/en/latest/usage.html>`_
