#!/usr/bin/env python3

"""Tests for `unassigned_section` class."""

import pytest

from letrista.section import Section
from letrista.line import Line

def test_section_is_created():
    """Creates a Section."""

    section = Section()

    assert section.type == Section.TYPE_UNASSIGNED

def test_section_as_str():
    """Test the __str__ property of the section."""

    section = Section()

    l1 = Line('Line 1')
    l2 = Line('Line 2')

    section.add_line(l1)
    section.add_line(l2)

    assert str(section) == 'Section ['+Section.TYPE_UNASSIGNED+']\n000 Line 1\n000 Line 2\n\n'

def test_section_has_right_word_count():
    """Test section has the right word count."""

    section = Section()

    l1 = Line('Line 1')
    l2 = Line('Line 2')

    section.add_line(l1)
    section.add_line(l2)

    assert section.word_count == 4
