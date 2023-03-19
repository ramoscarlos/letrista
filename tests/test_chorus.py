#!/usr/bin/env python3

"""Tests for `Chorus` class."""

import pytest

from letrista.section import Section
from letrista.line import Line
from letrista.chorus import Chorus

def test_chorus_is_created():
    """Creates a `Chorus`."""

    section = Chorus()

    assert section.type == Section.TYPE_CHORUS

def test_chorus_prints_nothing_if_empty():
    """`Chorus` prints nothing if empty."""

    section = Chorus()

    assert section.text == ''

def test_chorus_as_str():
    """Test the __str__ property of the chorus."""

    section = Chorus()

    section.add_line(Line('Line 1'))
    section.add_line(Line('Line 2'))

    assert str(section) == 'Section ['+Section.TYPE_CHORUS+']\n000 Line 1\n000 Line 2\n\n'