Writing lyrics with Letrista (the markup)
=========================================

There are three main concepts to take into consideration while writing a draft of lyrics with the Letrista markup:

* **Lines** represent the minimal unit, and the can contain rhyme scheme, syllable count, be comments, instructions, whitespace, or just be plain ignored.
* **Sections** are groups of lines separated by instructions, and belong to a part of the song (title, verse, chorus, bridge, etcetera).
* **Instructions** are lines that begin with a square bracket, ``[``, and determine the type of section.

How do we begin?
----------------

So, how do we start? Just by writing? Nope. Well, yes, and no. By default, all text before an instruction is ignored. That is, the following text:

.. code-block:: text

	I am making my lyrics here
	And I am not even rhyming
	But this is my verse
	And no one can stop me

amounts to nothing at the output. This means one thing:

	All text prior to the first section (which pretty much will be ``[Title]``), is ignored.

That is, you can start jotting down ideas, words, paragraphs, quotes, and it will not be taken into consideration for your lyrics. You won't even need a name for the song, just start typing and all is ignored.


So, how is a section created?
-----------------------------

Once you feel like something can go into the lyrics, you start the section with brackets, like:

.. code-block:: text

	[Verse]
	I am making my lyrics here
	And I am not even rhyming
	But this is my verse
	And no one can stop me

The ``[Verse]`` line makes all the difference: now everything under it is visible.

The following sections are valid:

* Title
* Verse
* Chorus
* Bridge
* Pre-chorus
* Post-chorus
* Intro
* Outro

Therefore, to create a new chorus, you just start the section with:

.. code-block:: text

	[Chorus]

And all the lines under it, until the next instruction is reached, will be parsed as part of the chorus.

As an example, here is a lyric with two sections:

.. code-block:: text

	[Verse]
	A generic line in a verse
	As boring as this line can be

	[Chorus]
	Now this is the chorus
	Yeah, yeah, yeah

The transformation of this to the format **marke37** yields the following:

.. code-block:: markdown

	A generic line in a verse
	As boring as this line can be

	**Now this is the chorus
	Yeah, yeah, yeah**


Commenting lines
----------------

But writing drafts would be not useful in markup if we could not remove lines from output in an easy way. Here is where comments come in: any line that has a dash (``-``) at the second position is a comment. Hence, a verse like the following one:

.. code-block:: text

	[Verse]
	A generic line in a verse
	-- This is an ignored line
	As boring as this line can be
	-- As well as this one

yields the same output as before:

.. code-block:: markdown

	A generic line in a verse
	As boring as this line can be

Speaking of which, why the dash at the second position? Because we can have rhyme scheme and syllable count.


Rhyme scheme and syllable count
-------------------------------

There are three possible interpretations for a printed line:

* A line that has the rhyme scheme at the first character.
* A line that has the rhyme scheme followed by the syllable count.
* A regular lyric line, with no annotations.


Lyric line with rhyme scheme
****************************

A line with a rhyme scheme satisfies the following conditions:

* The first character of the line is a capitalized letter.
* The second character is not alphanumeric.

This way, annotations like this can happen (lyrics from `The Black Market <https://genius.com/Rise-against-the-black-market-lyrics>`_):

.. code-block:: text

	[Verse]
	X A currency of heartache and sorrow
	A The air we breathe is stale with mold
	X To shadows we are slaves, digging deeper every day
	A But emptiness is growing so old

That is, lines 1 and 3 from the verse do not rhyme, but 2 and 4 do (and we assign the rhyme A). As that is only a writer aid, the output of the markup is:

.. code-block:: markdown

	A currency of heartache and sorrow
	The air we breathe is stale with mold
	To shadows we are slaves, digging deeper every day
	But emptiness is growing so old

That is, the first character, when capitalized, serves as the rhyme scheme of the line. That way, a draft can be started as:

.. code-block:: text

	[Verse]
	X
	A
	X
	A

where the content is yet to be delivered, but the structure is already in place (lines 2 and 4 should rhyme, while we care not for 1 and 3).


Lyric line with rhyme scheme and syllable count
***********************************************

Other useful piece of information while writing is the syllable count. For this, positions 3 and 4 are reserved (speaking in human-reading a line positions). Such that a default line with both scheme and count look like this:

.. code-block:: text

	┏━━ First character is for rhyme scheme
	┃
	┃ ┏━━ Three and four make for two-digit count
	┃ ┃
	X __ This is the lyrics
	 ┃   ┃
	 ┃   ┗━━ Six and beyond are lyrics
	 ┃
	 ┗━━ Second character, if dash, makes a comment

Going back to the prior verse, we can enhance it with syllable count:

.. code-block:: text

	[Verse]
	X 10 A currency of heartache and sorrow
	A 08 The air we breathe is stale with mold
	X 13 To shadows we are slaves, digging deeper every day
	A 10 But emptiness is growing so old

So for the second verse, we can start the scaffold as:

.. code-block:: text

	[Verse]
	X 10
	A 08
	X 13
	A 10

And that is an approximation for what we need to write, without even putting a word yet!

As a note: the syllable count is manual. This is because, even if syllables were counted by the dictionary definition, the syllable count should be counted by sound grouping. As an example, take the third line:

.. code-block:: text

	To shadows we are slaves, digging deeper every day

If you `listen to the song <https://www.youtube.com/watch?v=-sUgp5vjiwA&ab_channel=RiseAgainst-Topic>`_, is " we are" one syllable or two? I am going with "one", but we can differ (this possible lack of agreement makes it manual).

Two underscores serve as placeholder for syllable count in these two positions.


Plain lyric line
****************

A lyrics line is a line that is to be printed that does not fall in the two prior categories. Something like:

.. code-block:: text

	This is a text line

However, be aware that the "I" and "A" lines are going to be interpreted as schema lines. That is:

.. code-block:: text

	[Verse]
	I think this is a good line
	A good line indeed

will yield:

.. code-block:: markdown

	think this is a good line
	good line indeed

because the two lines fulfill the requirements:

* They begin with a capital letter
* There is a space at the second position

To correct this behavior, the default schema is always suggested:

.. code-block:: text

	[Verse]
	X I think this is a good line
	X A good line indeed


End-of-line comments
--------------------

Besides the full-line comments (any line with a dash at the second position), a comment can be added at the end of any line with two dashes:

.. code-block:: text

	[Verse]
	X I think this is a good line -- is it, tho?
	X A good line indeed

where the text after the dashes is ignored, yielding:

.. code-block:: text

	I think this is a good line
	A good line indeed

But, what about the whitespace before the dashes? Is it printed? Good question.


Whitespace
----------

You can have all the whitespace you want before and after the lines, and between sections. For instance, this line:

.. code-block:: text

	[Verse]
	X     So much space         -- right?

gets reduced to:

.. code-block:: markdown

	So much space

The same applies to empty lines, between lines and between sections. For instance, the following text:

.. code-block:: text

	[Verse]
	X             This has a lot of whitespace         -- also at the end
	X The    space   between words stays


	-- This gets deleted


	-- More empty space

	[Chorus]

	Here is the first line



	And the fourth line

.. code-block:: markdown

	This has a lot of whitespace
	The    space   between words stays

	**Here is the first line
	And the fourth line**


Repeating sections
------------------

A chorus is rarely done only once. No need to copy the lines, so there is a special repeat section, trailing with an ``R``.

For instance, to repeat a chorus, the repeat is ``[ChorusR]``. For a bridge, the instruction would be ``[BridgeR]``.

Furthermore, every section gets a secuential id. That is, the first verse is ``Verse1``, the second verse is ``Verse2``. Under this logic, the second verse can be repeated as ``[Verse2R]``:

.. code-block:: text

	[Verse]
	Text 1
	Text 2
	Text 3
	Text 4

	[Verse]
	Text 5
	Text 6
	Text 7
	Text 8

	[Chorus]
	Chorus 1
	Chorus 2
	Chorus 3

	[Verse2R]

	[ChorusR]

With those two repeat sections, the text is:

.. code-block:: text

	Text 1
	Text 2
	Text 3
	Text 4

	Text 5
	Text 6
	Text 7
	Text 8

	**Chorus 1
	Chorus 2
	Chorus 3**

	Text 5
	Text 6
	Text 7
	Text 8

	**Chorus 1
	Chorus 2
	Chorus 3**


End of document
---------------

When the lyrics are done, a ruler can be set to ignore everything after it:

.. code-block:: text

	[Verse]
	And this is the last verse

	[Outro]
	And the outro finishes all!

	**************

	And this shall be ignored
	Regardless if its a comment or not

The lines after the ruler are ignored. All of them:

.. code-block:: text

	And this is the last verse

	**_And the outro finishes all!_**

