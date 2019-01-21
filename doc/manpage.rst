====
ydpy
====

----------------------------------------------
CLI for Collins and Langenscheidt dictionaries
----------------------------------------------

:manual section: 1
:version: ydpy 0.4.1
:date: 2018-10-01

Synopsis
--------
**ydpy** [*option*...] [*regexp*]

Description
-----------

**ydpy** is a command‐line interface to the following dictionaries
distributed by Young Digital Planet:

* English‐Polish and Polish‐English Collins dictionary
* Polish‐German and German‐Polish Langenscheidt dictionary

If *regexp* is specified, **ydpy** prints only entries
with names matching the specified regular exprssion.
Otherwise, it prints all the dictionary entries.

Options
-------

-e, --en-pl
   Use the English‐Polish dictionary.
   This is the default.
-p, --pl-en
   Use the Polish‐English dictionary.
-g, --de-pl
   Use the German‐Polish dictionary.
-o, --pl-de
   Use the Polish‐German dictionary.
-f PATH, --path PATH
   Set dictionary data directory.
   The default is the path specified in ``/etc/ydpdict.conf``,
   or ``/usr/share/ydpdict``.
-h, --help
   Show help message and exit.
--version
   Show version information and exit.

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

https://docs.python.org/3/library/re.html#regular-expression-syntax

.. vim:ts=3 sts=3 sw=3
