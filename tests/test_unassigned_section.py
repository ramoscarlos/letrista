#!/usr/bin/env python3

"""Tests for `unassigned_section` class."""

import pytest

from letrista.line import Line
from letrista.unassigned_section import UnassignedSection

def test_unassigned_section_is_created():
    """Creates an UnassignedSection."""

    section = UnassignedSection()

    assert section.TYPE_UNASSIGNED == section.type
    assert isinstance(section.lines, list)

def test_unassigned_section_has_two_lines():
    section = UnassignedSection()

    line1 = Line('First line')
    line2 = Line('Second line')

    section.add_line(line1)
    section.add_line(line2)

    assert len(section.lines) == 2

def test_unassigned_section_prints_nothing():
    section = UnassignedSection()

    line1 = Line('First line')
    line2 = Line('Second line')

    section.add_line(line1)
    section.add_line(line2)

    assert section.text == ''

def test_unassigned_section_returns_word_count_zero():
    section = UnassignedSection()

    line1 = Line('First line')

    section.add_line(line1)

    assert section.word_count == 0
