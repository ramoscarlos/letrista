#!/usr/bin/env python3

"""Tests for `Title` class."""

import pytest

from letrista.line import Line
from letrista.title import Title

def test_title_is_unassigned():
    """Creates a Title with default 'Untitled' value."""

    section = Title()

    assert section.text == 'Untitled\n========\n'

def test_title_is_created_with_content():
    """Creates a Title."""

    section = Title()

    line1 = Line('[Title]')
    line2 = Line('A-This is not the title')
    line3 = Line('This is the title')
    line4 = Line('This is also not the title')

    section.add_line(line1)
    section.add_line(line2)
    section.add_line(line3)
    section.add_line(line4)

    assert section.TYPE_TITLE == section.type
    assert section.text == 'This is the title\n=================\n'
    assert isinstance(section.lines, list)
