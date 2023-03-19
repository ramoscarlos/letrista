#!/usr/bin/env python

"""Tests for `EditableLine` in `letrista` package."""

import pytest

from letrista.editable_line import EditableLine as Line

###########################################################
##### Test of line TYPE can be commented              #####
###########################################################

def test_editable_line_type_lyrics_can_be_commented():
    line = Line('This is text')

    assert line.type == Line.TYPE_LYRICS
    assert line.text == 'This is text'
    assert line._original_text == 'This is text'

    line.comment()

    assert line.type == Line.TYPE_COMMENT
    assert line.text == ''
    assert line._original_text == '--This is text'

def test_editable_line_type_schema_can_be_commented():
    line = Line('A This is text')

    assert line.type == Line.TYPE_SCHEMA
    assert line.text == 'This is text'

    line.comment()

    assert line.type == Line.TYPE_COMMENT
    assert line._original_text == 'A-This is text'
    assert line.text == ''

def test_editable_line_type_count_can_be_commented():
    line = Line('A __ This is text')

    assert line.type == Line.TYPE_COUNT
    assert line.text == 'This is text'

    line.comment()

    assert line.type == Line.TYPE_COMMENT
    assert line._original_text == 'A-__ This is text'
    assert line.text == ''

def test_editable_line_type_skip_can_be_commented():
    line = Line('         ')

    assert line.type == Line.TYPE_SKIP
    assert line.text == ''

    line.comment()

    assert line.type == Line.TYPE_COMMENT
    assert line._original_text == '--         '
    assert line.text == ''

def test_editable_line_type_instruction_can_be_commented():
    line = Line('[Verse]')

    assert line.type == Line.TYPE_INSTRUCTION
    assert line._original_text == '[Verse]'

    line.comment()
    assert line._original_text == '--[Verse]'

def test_editable_line_type_ignored_cannot_be_commented():
    """Ignored lines should not be commented.

    Once a line is TYPE_IGNORED, it cannot go back as ignored: it cannot return
    to the TYPE_IGNORED status after being uncommented.

    Unless a new status is created, such as TYPE_IGNORED_COMMENTED, but that
    would be much more of a hassle for something that is not visible.
    """
    line = Line('Ignored line', eol_or_unassigned = True)

    assert line.type == Line.TYPE_IGNORED
    assert line.text == ''

    line.comment()

    assert line.type == Line.TYPE_IGNORED
    assert line._original_text == 'Ignored line'
    assert line.text == ''

def test_editable_line_type_comment_cannot_be_commented():
    """A commented line (type 1) will not be altered in any shape or form."""

    line = Line('--Commented line')

    assert line.type == Line.TYPE_COMMENT
    assert line.text == ''

    line.comment()

    assert line.type == Line.TYPE_COMMENT
    assert line._original_text == '--Commented line'
    assert line.text == ''

def test_editable_line_type_comment_schema_cannot_be_commented():
    """A commented line (type 2) will not be altered in any shape or form."""

    line = Line('A-Commented line')

    assert line.type == Line.TYPE_COMMENT
    assert line.text == ''

    line.comment()

    assert line.type == Line.TYPE_COMMENT
    assert line._original_text == 'A-Commented line'
    assert line.text == ''

def test_editable_line_type_end_can_be_commented():
    line = Line('*****')

    assert line.type == Line.TYPE_END
    assert line.text == ''

    line.comment()

    assert line.type == Line.TYPE_COMMENT
    assert line._original_text == '--*****'
    assert line.text == ''

###########################################################
##### Test of line TYPE can be un-commented           #####
###########################################################

def test_editable_line_type_lyrics_can_be_uncommented():
    line = Line('This is text')

    assert line.type == Line.TYPE_LYRICS
    assert line._original_text == 'This is text'
    line.comment()
    line.uncomment()
    assert line.type == Line.TYPE_LYRICS
    assert line._original_text == 'This is text'

def test_editable_line_type_schema_can_be_uncommented():
    line = Line('A This is text')

    assert line.type == Line.TYPE_SCHEMA
    assert line.text == 'This is text'
    line.comment()
    line.uncomment()
    assert line.type == Line.TYPE_SCHEMA
    assert line.text == 'This is text'

def test_editable_line_type_count_can_be_uncommented():
    line = Line('A __ This is text')

    assert line.type == Line.TYPE_COUNT
    assert line.text == 'This is text'
    line.comment()
    line.uncomment()
    assert line.type == Line.TYPE_COUNT
    assert line.text == 'This is text'

def test_editable_line_type_skip_can_be_uncommented():
    line = Line('         ')

    assert line.type == Line.TYPE_SKIP
    assert line.text == ''
    line.comment()
    line.uncomment()
    assert line.type == Line.TYPE_SKIP
    assert line.text == ''

def test_editable_line_type_instruction_can_be_uncommented():
    line = Line('[Verse]')

    assert line.type == Line.TYPE_INSTRUCTION
    assert line._original_text == '[Verse]'
    line.comment()
    line.uncomment()
    assert line.type == Line.TYPE_INSTRUCTION
    assert line._original_text == '[Verse]'

def test_editable_line_type_ignored_cannot_be_uncommented():
    """Ignored lines should not be uncommented."""

    line = Line('Ignored line', eol_or_unassigned = True)

    assert line.type == Line.TYPE_IGNORED
    assert line.text == ''
    line.uncomment()
    assert line.type == Line.TYPE_IGNORED
    assert line._original_text == 'Ignored line'

def test_editable_line_type_comment_can_be_uncommented():
    line = Line('--Commented line')

    assert line.type == Line.TYPE_COMMENT
    assert line.text == ''
    line.uncomment()
    assert line.type == Line.TYPE_LYRICS
    assert line._original_text == 'Commented line'

def test_editable_line_type_comment_schema_can_be_uncommented():
    line = Line('A-Commented line')

    assert line.type == Line.TYPE_COMMENT
    assert line.text == ''
    line.uncomment()
    assert line.type == Line.TYPE_SCHEMA
    assert line._original_text == 'A Commented line'

def test_editable_line_type_end_can_be_uncommented():
    line = Line('*****')

    assert line.type == Line.TYPE_END
    line.comment()
    line.uncomment()
    assert line.type == Line.TYPE_END
    assert line._original_text == '*****'

###########################################################
##### Test of toggle_comment() function               #####
###########################################################

def test_editable_line_type_lyrics_toogles_comment_state():
    line = Line('Lyrics line')

    assert line.type == Line.TYPE_LYRICS
    assert line._original_text == 'Lyrics line'
    line.toggle_comment()
    assert line.type == Line.TYPE_COMMENT
    assert line._original_text == '--Lyrics line'
    line.toggle_comment()
    assert line.type == Line.TYPE_LYRICS
    assert line._original_text == 'Lyrics line'
    line.toggle_comment()
    assert line.type == Line.TYPE_COMMENT
    assert line._original_text == '--Lyrics line'

###########################################################
##### Test of logic for adding schema and count       #####
###########################################################

def test_editable_line_adds_syllable_count_to_lyrics():
    line = Line('Lyrics line')
    assert line.type == Line.TYPE_LYRICS

    line.add_syllable_count()
    assert line._original_text == 'X __ Lyrics line'

def test_editable_line_adds_syllable_count_to_schema():
    line = Line('X Lyrics line')
    assert line.type == Line.TYPE_SCHEMA

    line.add_syllable_count()
    assert line._original_text == 'X __ Lyrics line'

def test_editable_line_adds_syllable_count_to_schema_2():
    line = Line('A simple line')
    assert line.type == Line.TYPE_SCHEMA

    line.add_syllable_count()
    assert line._original_text == 'A __ simple line'

def test_editable_line_adds_syllable_count_to_skip():
    line = Line('       ')
    assert line.type == Line.TYPE_SKIP

    line.add_syllable_count()
    assert line._original_text == 'X __        '

def test_editable_line_does_not_add_count_to_instruction():
    line = Line('[Verse]')
    assert line.type == Line.TYPE_INSTRUCTION

    line.add_syllable_count()
    assert line._original_text == '[Verse]'
