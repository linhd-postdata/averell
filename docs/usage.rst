=====
Usage
=====

CLI
---

To show averell help::

    averell --help

To list all available corpora::

    averell list

Visualization example of one of the available corpora:

.. code-block:: text

      id  name              size      docs    words  granularity    license
    ----  ----------------  ------  ------  -------  -------------  ---------
       1  Disco V2          22M       4088   381539  stanza         CC-BY
                                                     line


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

Now we can combine and join these corpora through "granularity" selection::

    averell export 2 3 --granularity line --corpora-folder my_corpora

It produces an single JSON file with information about all the lines in
those corpora. Example of **two** random lines in the file :file:`mycorpora/corpus_2_3.json`:

.. code-block:: JSON

    {
        "line_number": "5",
        "line_text": "¿Has visto que en el mismo lugar donde",
        "metrical_pattern": "++---+--++-",
        "stanza_number": "2",
        "manually_checked": false,
        "poem_title": " - II - ",
        "author": "Mira de Amescua",
        "stanza_text": "¿Has visto que en el mismo lugar donde\nbordado estuvo el cristalino velo\nun bordado terliz de escarcha y hielo\nhace que el campo de verdor se monde?",
        "stanza_type": "cuarteto"
    }
    {
        "line_number": "10",
        "line_text": "el que a lo cierto no a lo incierto mira,",
        "metrical_pattern": "---+-+-+-+-",
        "stanza_number": "3",
        "manually_checked": false,
        "poem_title": "- VIII - Considerando un sepulcro y los que están en él ",
        "author": "Lope de Zarate",
        "stanza_text": "De aquí si que consigue el ser dichoso\nel que a lo cierto no a lo incierto mira,\npues le adorna lo eterno fastuoso;",
        "stanza_type": "terceto"
    }


In a project
------------

To use averell in a project::

	import averell

