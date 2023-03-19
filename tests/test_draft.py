#!/usr/bin/env python3

"""Tests for `draft` class."""

import os
import pytest

from letrista.draft import Draft
from letrista.line import Line

def get_expected_output(filename):
    # Gets the file from the testing path.
    file_path = os.path.dirname(__file__)+'/example_drafts/'+filename
    # Opens it for reading.
    f = open(file_path, "r")
    # Return all text.
    return f.read()

###########################################################
##### Draft plays well with strings                   #####
###########################################################

def test_draft_adds_one_line():
    """Test draft adds one line to the text."""

    draft = Draft()
    draft.add_text("Test line")

    assert draft._draft_lyrics == "Test line\n"
    assert draft.draft_line_count == 1

def test_draft_adds_two_lines_in_two_calls():
    """Test draft adds two lines to the text, using two calls."""

    draft = Draft()
    draft.add_text("Test line 1")
    draft.add_text("Test line 2")

    assert draft._draft_lyrics == "Test line 1\nTest line 2\n"
    assert draft.draft_line_count == 2

def test_draft_adds_two_lines_in_one_call():
    """Test draft adds two lines to the text, using one call."""

    draft = Draft()
    draft.add_text("Test line 1\nTest line 2")

    assert draft._draft_lyrics == "Test line 1\nTest line 2\n"
    assert draft.draft_line_count == 2

def test_line_count_cant_be_changed():
    """Test that the line count does not have a public setter."""

    draft = Draft()
    with pytest.raises(TypeError) as e_info:
        draft.draft_line_count(2)

    assert 'object is not callable' in str(e_info.value)

def test_draft_receives_initial_lines():
    """Test that the constructor receives two lines."""

    draft = Draft('Line 1\nLine 2\n')

    assert draft._draft_lyrics == "Line 1\nLine 2\n"
    assert draft.draft_line_count == 2

def test_draft_receives_initial_lines_adding_last_eol():
    """Test that the constructor receives two lines.

    The constructor will add the last \n, since the program
    requires that we always have a \n to break up the string
    into a list for further processing.
    """

    draft = Draft('Line 1\nLine 2')

    assert draft._draft_lyrics == "Line 1\nLine 2\n"
    assert draft.draft_line_count == 2

def test_draft_concatenates_initial_line_with_new_one():
    """Test that add_text concatenates with initial text."""

    draft = Draft('Line 1')
    draft.add_text('Line 2')

    assert draft._draft_lyrics == "Line 1\nLine 2\n"
    assert draft.draft_line_count == 2

def test_draft_creates_object_line():
    """The draft generates the line object."""

    draft = Draft('Line 1')

    assert len(draft.lines) == 1
    assert isinstance(draft.lines[0], Line)
    assert 'Line 1' == draft.lines[0].text

def test_draft_creates_two_object_lines():
    """The draft generates two line objects."""

    draft = Draft('Line 1\nLine 2')

    assert len(draft.lines) == 2
    assert isinstance(draft.lines[0], Line)
    assert isinstance(draft.lines[1], Line)
    assert 'Line 1' == draft.lines[0].text
    assert 'Line 2' == draft.lines[1].text

def test_draft_enumerates_object_lines():
    """The draft enumerates the lines properly."""

    draft = Draft('Line 1\nLine 2')

    assert 1 == draft.lines[0].draft_line_number
    assert 2 == draft.lines[1].draft_line_number

###########################################################
##### Draft creates sections with ids                 #####
###########################################################

def test_draft_creates_section():
    """Draft creates sections."""

    draft = Draft('[Verse]\nLine')

    draft.process_lines()

    assert 'Verse1' in draft._sections

def test_draft_creates_chorus_and_bridge():
    """Creates Chorus and Bridge from test text file."""

    draft = Draft()
    draft.add_file(os.path.dirname(__file__)+'/example_drafts/chorus_bridge.e37')

    sec = draft.process_lines()

    assert 'Chorus1' in draft._sections
    assert 'Bridge1' in draft._sections

def test_draft_creates_intro_and_verse():
    """Creates Intro and Verse from test text file."""

    draft = Draft()
    draft.add_file(os.path.dirname(__file__)+'/example_drafts/intro_verse.e37')

    sec = draft.process_lines()

    assert 'Intro1' in draft._sections
    assert 'Verse1' in draft._sections

def test_draft_creates_all_sections():
    """Correctly creates at least one section of each."""

    draft = Draft()
    draft.add_file(os.path.dirname(__file__)+'/example_drafts/all_sections.e37')
    draft.process_lines()

    assert draft.text == get_expected_output('all_sections.me37')

def test_draft_omits_empty_sections():
    draft = Draft()
    draft.add_file(os.path.dirname(__file__)+'/example_drafts/empty_sections.e37')
    draft.process_lines()

    assert draft.text == 'This is one line\n\nThis is the second line'


###########################################################
##### Draft repeats a section                         #####
###########################################################

def test_draft_repeats_a_chorus():
    """Repeats a chorus with the [ChorusR] instruction."""

    draft = Draft()
    draft.add_file(os.path.dirname(__file__)+'/example_drafts/chorus_r.e37')
    draft.process_lines()

    assert draft.text == get_expected_output('chorus_r.me37')

def test_draft_repeats_a_chorus2_not_present():
    """Repeats a chorus with the [Chorus2R] instruction (defaulting to Chorus1R)."""

    draft = Draft()
    draft.add_file(os.path.dirname(__file__)+'/example_drafts/chorus2r_not_present.e37')
    draft.process_lines()

    assert draft.text == get_expected_output('chorus_r.me37')

def test_draft_repeats_a_chorus3_not_present():
    """Repeats a chorus with the [Chorus3R] instruction (defaulting to Chorus1R)."""

    draft = Draft()
    draft.add_file(os.path.dirname(__file__)+'/example_drafts/chorus3r_not_present.e37')
    draft.process_lines()

    assert draft.text == get_expected_output('chorus_r.me37')

def test_draft_repeats_chorus_and_expands_it():
    """Repeats a chorus with the [ChorusR] instruction and expands the contents."""

    draft = Draft()
    draft.add_file(os.path.dirname(__file__)+'/example_drafts/chorusr_then_2r.e37')
    draft.process_lines()

    assert draft.text == get_expected_output('chorusr_then_2r.me37')

def test_draft_has_no_section_to_repeat():
    """Has a [ChorusR] instruction but no existing `Chorus` to copy."""

    draft = Draft()
    draft.add_file(os.path.dirname(__file__)+'/example_drafts/no_chorus_r.e37')
    draft.process_lines()

    assert draft.text == get_expected_output('no_chorus_r.me37')

def test_draft_word_count_of_intro_verse_is_correct():
    draft = Draft()
    draft.add_file(os.path.dirname(__file__)+'/example_drafts/intro_verse.e37')
    draft.process_lines()

    assert draft.word_count == 27

def test_draft_line_count_counts_printed_lines():
    """Get the line count."""

    draft = Draft()
    draft.add_file(os.path.dirname(__file__)+'/example_drafts/all_sections.e37')
    draft.process_lines()

    assert draft._sections['Title1'].line_count == 0
    assert draft._sections['Intro1'].line_count == 2
    assert draft._sections['Verse1'].line_count == 4
    assert draft._sections['Pre-chorus1'].line_count == 3
    assert draft._sections['Chorus1'].line_count == 4
    assert draft._sections['Post-chorus1'].line_count == 5
    assert draft._sections['Bridge1'].line_count == 2
    assert draft._sections['Verse2'].line_count == 3
    assert draft._sections['Outro1'].line_count == 3

    assert draft.line_count == 26


