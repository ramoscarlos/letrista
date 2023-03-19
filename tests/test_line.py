#!/usr/bin/env python

"""Tests for `line` in `letrista` package."""

import pytest

from letrista.line import Line


def test_line_fails_if_no_content():
    """Line instance fails if no text is provided."""

    with pytest.raises(TypeError) as e_info:
        line = Line()

    assert 'required positional argument' in str(e_info.value)

def test_line_is_created_without_line_number():
    """This creates a line object with the provided text."""

    line = Line('Gets created')

    assert 'Gets created' == line._original_text

###########################################################
##### Test of line TYPE                               #####
###########################################################

def test_line_is_type_end_of_lyric_with_five_stars():
    """This detects an end of lyric line with *****."""

    line = Line('*****')

    assert line.TYPE_END == line.type

def test_line_is_type_end_of_lyric_with_five_dashes():
    """This detects an end of lyric line with -----."""

    line = Line('-----')

    assert line.TYPE_END == line.type

def test_line_is_type_end_of_lyric_with_five_hashes():
    """This detects an end of lyric line with #####."""

    line = Line('#####')

    assert line.TYPE_END == line.type

def test_line_is_type_end_of_lyric_with_five_slashes():
    """This detects an end of lyric line with /////."""

    line = Line('/////')

    assert line.TYPE_END == line.type

def test_line_is_not_end_of_lyrics_if_whitespace_at_start():
    """There is no end if the separators do not start the line."""

    line = Line(' *****')

    assert line.TYPE_END != line.type

def test_line_is_not_type_end_of_lyric_with_four_stars():
    """If only four stars are provided, no end of lyrics is detected."""

    line = Line('****')

    assert line.TYPE_END != line.type

def test_line_is_ignored():
    """Test is ignored via constructor parameter."""

    line = Line('-----', eol_or_unassigned = True)

    assert line.TYPE_IGNORED == line.type

def test_line_is_empty():
    """Line is an empty line if there is no text."""

    line = Line('')

    assert line.TYPE_SKIP == line.type

def test_line_with_only_spaces_is_empty():
    """Line is an empty line if there is only spaces."""

    line = Line('                    ')

    assert line.TYPE_SKIP == line.type

def test_line_with_end_of_line_is_empty():
    """Line is empty if only is an end of line character."""

    line = Line('\n')

    assert line.TYPE_SKIP == line.type

def test_line_with_tabs_is_empty():
    """Line is empty if only has tabs characters."""

    line = Line('\t\t\t\t')

    assert line.TYPE_SKIP == line.type

def test_line_is_empty_if_only_whitespace_characters():
    """Line is empty if only has whitespace characters (spaces, tabs, eol)."""

    line = Line('          \t\n')

    assert line.TYPE_SKIP == line.type

def test_line_is_comment():
    """Line is comment if second position is a dash."""

    line = Line('A-00 Is comment')

    assert line.TYPE_COMMENT == line.type

def test_line_is_instruction():
    """Line is an instruction if it begins with brack '['."""

    line = Line('[This is an instruction]')

    assert line.TYPE_INSTRUCTION == line.type

def test_line_has_count():
    """The third and fourth characters as digit indicate count."""

    line = Line('X 00 This has a count')

    assert line.TYPE_COUNT == line.type

def test_line_has_undefined_count_with_xx():
    """The third and fourth characters as 'xx' indicate undefined count."""

    line = Line('X xx This has a count')

    assert line.TYPE_COUNT == line.type

def test_line_has_undefined_count_with_XX():
    """The third and fourth characters as 'XX' indicate undefined count."""

    line = Line('X XX This has a count')

    assert line.TYPE_COUNT == line.type

def test_line_has_undefined_count_with_underscores():
    """The third and fourth characters as '__' indicate undefined count."""

    line = Line('X __ This has a count')

    assert line.TYPE_COUNT == line.type

def test_line_has_schema():
    """Line has schema since is at least three characters long."""

    line = Line('X This has schema')

    assert line.TYPE_SCHEMA == line.type

def test_line_doesnt_have_schema():
    """Line should not be schema since it has only one character after strip."""
    line = Line('X ')

    assert line.TYPE_SCHEMA != line.type

def test_line_has_schema_with_plus():
    """Line has schema with a plus in second position."""

    line = Line('X+This has schema')

    assert line.TYPE_SCHEMA == line.type

def test_line_is_lyrics():
    """This is the last type. If nothing else, is just lyrics."""

    line = Line('This should be lyrics')

    assert line.TYPE_LYRICS == line.type

###########################################################
##### Test of line processed text                     #####
###########################################################

def test_ignored_line_returns_no_text():
    """Tests a line TYPE_IGNORED returns no text."""

    line = Line('This has text', eol_or_unassigned = True)

    assert line.TYPE_IGNORED == line.type
    assert '' == line.text

def test_comment_line_returns_no_text():
    """Tests a line TYPE_COMMENT returns no text."""

    line = Line('A-This is a comment')

    assert line.TYPE_COMMENT == line.type
    assert '' == line.text

def test_end_of_line_char_returns_no_text():
    """Tests a line TYPE_SKIP returns no text."""

    line = Line('\n')

    assert line.TYPE_SKIP == line.type
    assert '' == line.text

def test_empty_line_returns_no_text():
    """Tests a line TYPE_SKIP returns no text."""

    line = Line('')

    assert line.TYPE_SKIP == line.type
    assert '' == line.text

def test_instruction_line_returns_no_text():
    """Tests a line TYPE_INSTRUCTION returns no text."""

    line = Line('[')

    assert line.TYPE_INSTRUCTION == line.type
    assert '' == line.text

def test_type_count_eliminates_first_five_characters():
    """Tests that the first five characters are ignored from output text."""

    line = Line('A 00 This is the text')

    assert 'This is the text' == line.text

def test_type_schema_eliminates_first_three_characters():
    """Tests that the first two characters are ignored from output text."""

    line = Line('A This is the text')

    assert 'This is the text' == line.text

def test_line_removes_I_from_line():
    """Tests that the 'I ' is trimmed from output text."""

    line = Line('I am getting tired of these examples')

    assert 'am getting tired of these examples' == line.text

def test_line_removes_leading_and_trailing_whitespace():
    """Test that the space between rhyme and text, and text and comment, is removed"""

    line = Line('X     So much space         -- right?')

    assert 'So much space' == line.text

###########################################################
##### Test of other simple line properties            #####
###########################################################

def test_str_property_of_line():

    line = Line('This is the text', draft_line_number = 50)

    assert line.__str__() == '050 This is the text'

def test_line_sets_is_instruction_true():
    """Tests if the line determines correctly if it is instruction."""

    line = Line('[')

    assert line.is_instruction is True

def test_line_sets_is_instruction_false():
    """Tests if the line determines correctly if it is instruction."""

    line = Line('-[')

    assert line.is_instruction is False

def test_line_yields_correct_word_count_with_regular_words():
    """Tests the word count is right with just alpha-numeric characters."""

    line = Line('This has five words only')

    assert line.word_count == 5

def test_line_yields_correct_word_count_with_lots_of_spaces():
    """Tests the word count is right with lots of spaces between words."""

    line = Line('This         has      five      words    only')

    assert line.word_count == 5

def test_line_counts_numbers_as_a_word():
    """Tests the word count is right with numbers."""

    line = Line('My house has 100 square meters')

    assert line.word_count == 6

###########################################################
##### Test further symbol processing in a lyrics line #####
###########################################################

def test_inline_comments_are_erased_with_space_between():
    """Tests the inline comments are not shown (with space between)."""

    line = Line('This is a lyrics line -- with comments')

    assert line.text == 'This is a lyrics line'

def test_inline_comments_are_erased_with_no_space_between():
    """Tests the inline comments are not shown (with no space between text)."""

    line = Line('This is a lyrics line--with comments')

    assert line.text == 'This is a lyrics line'

def test_hat_capitalized_letters_are_erased():
    """Test that the ^A, or inside-line rhymes are eliminated."""

    line = Line('This is an inner^A rhyme')

    assert line.text == 'This is an inner rhyme'

def test_hat_digit_is_erased():
    """Test that the ^9, or inside-line rhymes are eliminated."""

    line = Line('This is an inner^9 rhyme')

    assert line.text == 'This is an inner rhyme'

def test_hat_digits_are_erased():
    """Test that the ^00, or inside-line rhymes are eliminated."""

    line = Line('This is an inner^00 rhyme')

    assert line.text == 'This is an inner rhyme'

def test_hat_noncapitalized_letters_are_kept():
    """Test that the ^a are erased.

    If a hat needs to be on the lyrics, possibly they will need to be escaped.
    """

    line = Line('This is an inner^a rhyme')

    assert line.text == 'This is an innera rhyme'

def test_two_hat_capitalized_letters_are_erased():
    """Test that the ^A, or inside-line rhymes are eliminated."""

    line = Line('This is an inner^A rhyme, here^B again')

    assert line.text == 'This is an inner rhyme, here again'

def test_two_hats_with_caps_and_numbers_are_removed():
    """Test that the ^Z and ^89 inside-line rhymes are eliminated."""

    line = Line('This is an inner^Z rhyme, here^89 again')

    assert line.text == 'This is an inner rhyme, here again'

def test_consecutive_hats_are_removed():
    """Test that the ^^^^^^^^^^ are all removed."""

    line = Line('This is an inner^^^^^^^^^^ rhyme')

    assert line.text == 'This is an inner rhyme'

def test_last_cap_of_consecutive_hats_is_removed():
    """Test that the ^^^^^^^^^^A are all removed."""

    line = Line('This is an inner^^^^^^^^^^A rhyme')

    assert line.text == 'This is an inner rhyme'
