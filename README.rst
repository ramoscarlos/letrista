====================================================
Letrista |pipy-version| |build-status| |docs-status|
====================================================


Letrista is a markup syntax and parser system for lyrics writing, written in `Python 3 <https://www.python.org/>`_. It allows the use of comments and useful notes for lyrics drafts, such as rhyme scheme and syllable count.

The output of this parser is in `marke37 <https://github.com/ramoscarlos/marke37>`_ format, which is a modified version of the Markdown syntax. This output can be processed further if needed into a more common and visual format (mainly HTML).

The primary goal of this package is to aid the lyricists/songwriters (mainly myself) to concentrate on the actual content that will remain on the lyrics, while also leaving the options available within the same file (for if those are needed to compare or restore).

The ideal usage of this package is with a real-time editing tool, like within the Sublime Text editor, with the `Letrista Sublime <https://github.com/ramoscarlos/letrista_sublime>`_ plugin, but the module is provided for inclusion in other projects.

A demo editor is provided at `quick-draft.letrista.app <https://quick-draft.letrista.app/>`_, with an already populated `example in English <https://quick-draft.letrista.app/example>`_ and `one in Spanish <https://quick-draft.letrista.app/ejemplo>`_.

The module is released under the MIT license, so you can pretty much what you want with it. For the full documentation, visit `Read The Docs <https://letrista.readthedocs.io>`_.


.. ###
.. Substitutions
.. ################

.. |pipy-version| image:: https://img.shields.io/pypi/v/letrista.svg
   :target: https://pypi.python.org/pypi/letrista
   :alt: PiPy Version

.. |build-status| image:: https://img.shields.io/travis/ramoscarlos/letrista.svg
   :target: https://travis-ci.com/ramoscarlos/letrista
   :alt: Build Status

.. |docs-status| image:: https://readthedocs.org/projects/letrista/badge/?version=latest
   :target: https://letrista.readthedocs.io/en/latest/?version=latest
   :alt: Documentation Status
