=======================
Usage (the Python code)
=======================

The main object of the module is the ``Draft``::

    from letrista.draft import Draft

From there, you have three options, add text directly at creation time, as string or read a file.


Adding text for processing
--------------------------


From the constructor
********************

You can create a ``Draft`` and provide the full lyrics as string::

    draft = Draft('Full lyrics')


Adding a string
***************

The first way is to load a string into the object:

.. code-block:: python

    draft = Draft()
    draft.add_text("Here is one line")

The ``add_text`` method accumulates the text from succesive calls, and also takes several lines at a time, so one buffer with the full draft can be taken with just one function call.


From a file
***********

The function ``add_file`` expects the path to a file with read permissions and appends it to the current text in the draft::

    draft = Draft()
    draft.add_file('path_to_file.e37')


Generating the marke37 text
---------------------------


There are two ways to get the processed text from the draft. One is calling the ``process_lines`` function, then getting the text once its needed:

.. code-block:: python

    # Dump all the text into the object.
    draft = Draft(all_the_text)

    # Call this to process the given text.
    draft.process_lines()

    # Once you need to use it, just call the property
    # (after the process_lines has been called)
    draft.text

The other way to do this is to get the text from the direct call from the ``to_marke37`` function:

.. code-block:: python

    # Dump all the text into the object.
    draft = Draft(all_the_text)

    text = draft.to_marke37()


Properties
----------


There are not so many properties, but you may find a use for them:

==============  =================================
Property        Information
==============  =================================
``text``        The processed lyrics, in marke37
                format.
--------------  ---------------------------------
``word_count``  Word count of the printable lines
                of the draft.
==============  =================================

