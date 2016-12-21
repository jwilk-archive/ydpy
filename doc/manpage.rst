====
ydpy
====

----------------------------------------------
CLI for Collins and Langenscheidt dictionaries
----------------------------------------------

:manual section: 1
:version: ydpy 0.4.1
:date: 2016-12-21

Synopsis
--------
**ydpy** [*option*...] [*search-term*]

Description
-----------

**ydpy** is a command-line interface to the Collins
English-Polish/Polish-English and Langenscheidt German-Polish/Polish-German
dictionaries distributed by Young Digital Planet.

Options
-------

-e, --en-pl
   Use the English-Polish dictionary.
   This is the default.
-p, --pl-en
   Use the Polish-English dictionary.
-g, --de-pl
   Use the German-Polish dictionary.
-o, --pl-de
   Use the Polish-German dictionary.
-f PATH, --path PATH
   Set dictionary data directory.
   The default is the path specified in ``/etc/ydpdict.conf``,
   or ``/usr/share/ydpdict``.
-h, --help
   Show the help message and exit.
--version
   Show the program's version information and exit.

Example
-------

::

   $ ydpy --pl-en '^słownik$'
   słowni|k (-ka -ki) (instr sg  -kiem)
   m
   (książka) dictionary
   (słownictwo) vocabulary
   słownik polsko-angielski a Polish-English dictionary

See also
--------

**ydpdict**\ (1)

.. vim:ts=3 sts=3 sw=3
