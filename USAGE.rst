=====
Usage
=====


Command line interface
----------------------

To show averell help::

    averell --help


List
^^^^

To list all available corpora::

    averell list

Options:

--rst   Prints the corpora list in reStructuredText format

Visualization example of the available corpora:

.. code-block:: text

      id  name                     lang    size      docs     words  granularity    license
    ----  -----------------------  ------  ------  ------  --------  -------------  -----------
       1  Disco V2.1               es      22M       4088    381539  stanza         CC-BY
          (disco2_1)                                                 line
       2  Disco V3                 es      28M       4080    377978  stanza         CC-BY
          (disco3)                                                   line
       3  Sonetos Siglo            es      6.8M      5078    466012  stanza         CC-BY-NC
          de Oro                                                     line           4.0
          (adso)
       4  ADSO 100                 es      128K       100      9208  stanza         CC-BY-NC
          poems corpus                                               line           4.0
          (adso100)
       5  Poesía Lírica            es      3.8M       475    299402  stanza         CC-BY-NC
          Castellana Siglo                                           line           4.0
          de Oro                                                     word
          (plc)                                                      syllable
       6  Gongocorpus (gongo)      es      9.2M       481     99079  stanza         CC-BY-NC-ND
                                                                     line           3.0
                                                                     word           FR
                                                                     syllable
       7  Eighteenth Century       en      2400M     3084   2063668  stanza         CC
          Poetry Archive                                             line           BY-SA
          (ecpa)                                                     word           4.0
       8  For Better               en      39.5M      103     41749  stanza         Unknown
          For Verse                                                  line
          (4b4v)
       9  Métrique en              fr      183M      5081   1850222  stanza         Unknown
          Ligne (mel)                                                line
      10  Biblioteca Italiana      it      242M     25341   7121246  stanza         Unknown
          (bibit)                                                    line
                                                                     word
      11  Corpus of                cs      4100M    66428  12636867  stanza         CC-BY-SA
          Czech Verse                                                line
          (czverse)                                                  word
      12  Stichotheque Portuguese  pt      11.8M     1702    168411  stanza         Unkwown
          (stichopt)                                                 line


Download
^^^^^^^^

This option allows extracting all the poems from the selected corpora.
Each poem is translated to a JSON format file. Once the poems have been processed,
the researcher can use each poem individually.

Usage: `averell download [OPTIONS] [IDs]`

  Download the corpus with IDs. IDs can be numeric identifiers in the
  corpora list, corpus shortcodes (shown between parenthesis), the
  speciall literal "all" to download all corpora, or two-letter ISO language
  codes to download avaliable corpora in a specific language.

  For example, the command "averell download 1 bibit fr" will download DISCO
  V2.1, the Biblioteca Italiana poetry corpus, and all corpora tagged with
  the French languge tag.

Options:

--corpora-folder  Local folder where the corpora will be downloaded

Example:

Download desired corpora into :file:`mycorpora` folder::

    averell download 2 3 --corpora-folder my_corpora

Example of poem in TEI format obtained from one of the corpora:

.. code-block:: XML

    <TEI xmlns="http://www.tei-c.org/ns/1.0">
        <teiHeader>
            <fileDesc>
                <titleStmt>
                    <title> Spanish Metrical Patterns Bank: Golden Age Sonnets.</title>
                    <principal>Borja Navarro Colorado</principal>
                    <respStmt>
                        <name>María Ribes Lafoz</name>
                        <name>Noelia Sánchez López</name>
                        <name>Borja Navarro Colorado</name>
                        <resp>Metrical patterns annotation</resp>
                    </respStmt>
                </titleStmt>
                <publicationStmt>
                    <publisher>Natural Language Processing Group. Department of Software and Computing Systems. University of Alicante (Spain)</publisher>
                </publicationStmt>
                <sourceDesc>
                    <bibl><title>Sonetos</title> de <author>Garcilaso de La Vega</author>. <publisher>Biblioteca Virtual Miguel de Cervantes</publisher>, edición de <editor role="editor">Ramón García González</editor>.</bibl>
                </sourceDesc>
            </fileDesc>
            <encodingDesc>
                <metDecl xml:id="bncolorado" type="met" pattern="((\+|\-)+)*">
                    <metSym value="+">stressed syllable</metSym>
                    <metSym value="-">unstressed syllable</metSym>
                </metDecl>
                <metDecl>
                    <p>All metrical patterns have been manually checked.</p>
                </metDecl>
            </encodingDesc>
        </teiHeader>
        <text>
            <body>
                <head>
                    <title>-XX-</title>
                </head>
                <lg type="cuarteto">
                    <l n="1" met="-++--++--+-">Con tal fuerza y vigor son concertados</l>
                    <l n="2" met="-----+-+-+-">para mi perdición los duros vientos,</l>
                    <l n="3" met="--+--+---+-">que cortaron mis tiernos pensamientos</l>
                    <l n="4" met="+----++--+-">luego que sobre mí fueron mostrados.</l>
                </lg>
                <lg type="terceto">
                    <l n="5" met="-++--+---+-">El mal es que me quedan los cuidados</l>
                    <l n="6" met="---+-----+-">en salvo de estos acontecimientos,</l>
                    <l n="7" met="-++--+---+-">que son duros, y tienen fundamentos</l>
                </lg>
            </body>
        </text>
    </TEI>

Generated example JSON file from input XML/TEI poem into
:file:`my_corpora/{corpus}/averell/parser/{author_name}/{poem_name}.json`

.. code-block:: JSON

    {
        "manually_checked": true,
        "poem_title": "-XX-",
        "author": "Garcilaso de La Vega",
        "stanzas": [
            {
                "stanza_number": "1",
                "stanza_type": "cuarteto",
                "lines": [
                    {
                        "line_number": "1",
                        "line_text": "Con tal fuerza y vigor son concertados",
                        "metrical_pattern": "-++--++--+-"
                    },
                    {
                        "line_number": "2",
                        "line_text": "para mi perdición los duros vientos,",
                        "metrical_pattern": "-----+-+-+-"
                    },
                    {
                        "line_number": "3",
                        "line_text": "que cortaron mis tiernos pensamientos",
                        "metrical_pattern": "--+--+---+-"
                    },
                    {
                        "line_number": "4",
                        "line_text": "luego que sobre mí fueron mostrados.",
                        "metrical_pattern": "+----++--+-"
                    }
                ],
                "stanza_text": "Con tal fuerza y vigor son concertados\npara mi perdición los duros vientos,\nque cortaron mis tiernos pensamientos\nluego que sobre mí fueron mostrados."
            },
            {
                "stanza_number": "2",
                "stanza_type": "terceto",
                "lines": [
                    {
                        "line_number": "5",
                        "line_text": "El mal es que me quedan los cuidados",
                        "metrical_pattern": "-++--+---+-"
                    },
                    {
                        "line_number": "6",
                        "line_text": "en salvo de estos acontecimientos,",
                        "metrical_pattern": "---+-----+-"
                    },
                    {
                        "line_number": "7",
                        "line_text": "que son duros, y tienen fundamentos",
                        "metrical_pattern": "-++--+---+-"
                    }
                ],
                "stanza_text": "El mal es que me quedan los cuidados\nen salvo de estos acontecimientos,\nque son duros, y tienen fundamentos"
            }
        ]
    }

Export
^^^^^^

This functionality allows to build a new corpus from the selected corpora and select the granularity.
The result will be new unique corpus in a JSON format file.
The new corpus will include all the information of the poem indexed by its granularity.

Usage: `averell export [OPTIONS] [IDs]`

  Parse the corpus with IDs with the GRANULARITY into CORPORA-FOLDER. IDS
  can be numeric identifiers in the "averell list" output, corpus shortcodes
  (shown between parenthesis), the speciall literal "all" to export all
  corpora, or two-letter ISO language codes to export avaliable corpora in a
  specific language.

  For example, the command "averell export 1 bibit fr" will export DISCO
  V2.1, the Biblioteca Italiana poetry corpus, and all corpora tagged with
  the French languge tag in a single file spliting poems line by line.


Options:

--granularity      Refers to the granularity of the corpus: stanza , line, word or syllable
--corpora-folder   Local folder where the corpora are located
--filename         Name of the generated corpus file

Line
++++

Now we can combine and join these corpora through "granularity" selection::

    averell export 2 3 --granularity line --corpora-folder my_corpora --filename export_lines

It produces an single JSON file with information about all the lines in
those corpora. Example of the first lines in the file :file:`export_lines.json`:

.. code-block:: JSON

        {
            "line_number": "1",
            "line_text": "Mira, Zaide, que te aviso",
            "metrical_pattern": "+-+---+-",
            "stanza_number": "1",
            "manually_checked": false,
            "poem_title": "-Mira, Zaide, que te aviso ",
            "author": "Lope de Vega",
            "stanza_text": "Mira, Zaide, que te aviso\nque no pases por mi calle\nni...",
            "stanza_type": "Romance",
            "corpus": "plc"
        }
        {
            "line_number": "2",
            "line_text": "que no pases por mi calle",
            "metrical_pattern": "-+---+-",
            "stanza_number": "1",
            "manually_checked": false,
            "poem_title": "-Mira, Zaide, que te aviso ",
            "author": "Lope de Vega",
            "stanza_text": "...\nque no pases por mi calle\nni hables con mis mujeres,\nni con mis cautivos trates...",
            "stanza_type": "Romance",
            "corpus": "plc"
        }

Stanza
++++++

Example of first stanzas in the file :file:`export_stanzas.json` from the command::

   averell export 5 6 --granularity stanzas --corpora-folder my_corpora --filename export_stanzas

.. code-block:: JSON

    {
        "stanza_number": "1",
        "manually_checked": false,
        "poem_title": "-Mira, Zaide, que te aviso ",
        "author": "Lope de Vega",
        "stanza_text": "Mira, Zaide, que te aviso\nque no pases por mi calle\nni hables con mis mujeres,\nni con mis cautivos trates,\nni preguntes en qué entiendo\nni quién viene a visitarme,\nqué fiestas me dan contento\no qué colores me aplacen;\nbasta que son por tu causa\nlas que en el rostro me salen,\ncorrida de haber mirado\nmoro que tan poco sabe.\nConfieso que eres valiente,\nque hiendes, rajas y partes\ny que has muerto más cristianos\nque tienes gotas de sangre;\nque eres gallardo jinete,\nque danzas, cantas y tañes,\ngentil hombre, bien criado\ncuanto puede imaginarse;\nblanco, rubio por extremo,\nseñalado por linaje,\nel gallo de las bravatas,\nla nata de los donaires,\ny pierdo mucho en perderte\ny gano mucho en amarte,\ny que si nacieras mudo\nfuera posible adorarte;\ny por este inconveniente\ndetermino de dejarte,\nque eres pródigo de lengua\ny amargan tus libertades\ny habrá menester ponerte\nquien quisiere sustentarte\nun alcázar en el pecho\ny en los labios un alcaide.\nMucho pueden con las damas\nlos galanes de tus partes,\nporque los quieren briosos,\nque rompan y que desgarren;\nmas tras esto, Zaide amigo,\nsi algún convite te hacen,\nal plato de sus favores\nquieren que comas y calles.\nCostoso fue el que te hice;\nventuroso fueras, Zaide,\nsi conservarme supieras\ncomo supisme obligarme.\nApenas fuiste salido\nde los jardines de Tarfe\ncuando hiciste de la tuya\ny de mi desdicha alarde.\nA un morito mal nacido\nme dicen que le enseñaste\nla trenza de los cabellos\nque te puse en el turbante.\nNo quiero que me la vuelvas\nni quiero que me la guardes,\nmas quiero que entiendas, moro,\nque en mi desgracia la traes.\nTambién me certificaron\ncómo le desafiaste\npor las verdades que dijo,\nque nunca fueran verdades.\nDe mala gana me río;\n¡qué donoso disparate!\nNo guardas tú tu secreto\n¿y quieres que otro le guarde?\nNo quiero admitir disculpa;\notra vez vuelvo a avisarte\nque ésta será la postrera\nque me hables y te hable.\nDijo la discreta Zaida\na un altivo bencerraje\ny al despedirle repite:\nQuien tal hace, que tal pague.",
        "stanza_type": "Romance",
        "corpus": "plc"
    }
    {
        "stanza_number": "1",
        "manually_checked": false,
        "poem_title": "A San Juan de Alfarache ",
        "author": "Lope de Vega",
        "stanza_text": "A San Juan de Alfarache\nva la morena\na trocar con la flota\nplata por perlas.",
        "stanza_type": "Seguidilla",
        "corpus": "plc"
    }

Word
++++

Example of first words in the file :file:`export_words.json` from the command::

   averell export 6 10 --granularity word --corpora-folder my_corpora --filename export_words

.. code-block:: JSON

    {
        "word_text": "A",
        "line_number": 1,
        "line_text": "A este que admiramos en luciente,",
        "metrical_pattern": "+---+---+-",
        "stanza_number": 1,
        "manually_checked": false,
        "poem_title": "A este que admiramos en luciente,",
        "author": "Góngora, Luis de",
        "stanza_type": "",
        "corpus": "gongo"
    }
    {
        "word_text": "este",
        "line_number": 1,
        "line_text": "A este que admiramos en luciente,",
        "metrical_pattern": "+---+---+-",
        "stanza_number": 1,
        "manually_checked": false,
        "poem_title": "A este que admiramos en luciente,",
        "author": "Góngora, Luis de",
        "stanza_type": "",
        "corpus": "gongo"
    }
    {
        "word_text": "que",
        "line_number": 1,
        "line_text": "A este que admiramos en luciente,",
        "metrical_pattern": "+---+---+-",
        "stanza_number": 1,
        "manually_checked": false,
        "poem_title": "A este que admiramos en luciente,",
        "author": "Góngora, Luis de",
        "stanza_type": "",
        "corpus": "gongo"
    }

Syllable
++++++++

Example of syllables in the file :file:`export_syllables.json` from the command::

   averell export 6 --granularity syllable --corpora-folder my_corpora --filename export_syllables

.. code-block:: JSON

   {
        "syllable": "A",
        "line_number": 1,
        "word_text": "A",
        "line_text": "A este que admiramos en luciente,",
        "metrical_pattern": "+---+---+-",
        "stanza_number": 1,
        "manually_checked": false,
        "poem_title": "A este que admiramos en luciente,",
        "author": "Góngora, Luis de",
        "stanza_type": "",
        "corpus": "gongo"
    }
    {
        "syllable": "es",
        "line_number": 1,
        "word_text": "este",
        "line_text": "A este que admiramos en luciente,",
        "metrical_pattern": "+---+---+-",
        "stanza_number": 1,
        "manually_checked": false,
        "poem_title": "A este que admiramos en luciente,",
        "author": "Góngora, Luis de",
        "stanza_type": "",
        "corpus": "gongo"
    }
    {
        "syllable": "te",
        "line_number": 1,
        "word_text": "este",
        "line_text": "A este que admiramos en luciente,",
        "metrical_pattern": "+---+---+-",
        "stanza_number": 1,
        "manually_checked": false,
        "poem_title": "A este que admiramos en luciente,",
        "author": "Góngora, Luis de",
        "stanza_type": "",
        "corpus": "gongo"
    }
    {
        "syllable": "que",
        "line_number": 1,
        "word_text": "que",
        "line_text": "A este que admiramos en luciente,",
        "metrical_pattern": "+---+---+-",
        "stanza_number": 1,
        "manually_checked": false,
        "poem_title": "A este que admiramos en luciente,",
        "author": "Góngora, Luis de",
        "stanza_type": "",
        "corpus": "gongo"
    }



In a Python project
-------------------

To use averell in a project::

   import averell

Exported corpora can be easily loaded into Pandas

.. code-block:: bash

   averell export adso100 --granularity line --filename adso100.json

.. code-block:: python

    import pandas as pd

    adso100 = pd.read_json(open("adso100.json"))

