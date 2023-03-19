#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Carlos Ramos.

from abc import abstractmethod

from letrista.line import Line

class Section:
    """Represents a song/lyrics section within `Draft` object."""

    # Type constants.
    TYPE_UNASSIGNED = 'Unassigned'
    TYPE_TITLE      = 'Title'
    TYPE_VERSE      = 'Verse'
    TYPE_CHORUS     = 'Chorus'
    TYPE_BRIDGE     = 'Bridge'
    TYPE_PRECHORUS  = 'Pre-chorus'
    TYPE_POSTCHORUS = 'Post-chorus'
    TYPE_INTRO      = 'Intro'
    TYPE_OUTRO      = 'Outro'

    def __init__(self):
        """Initializes the _lines list."""

        self._lines = []
        self._type  = self.TYPE_UNASSIGNED
        self._pre_section_text  = ''
        self._post_section_text = ''

        # Inner text created with the Lines.
        self._inner_text = None
        # Section word count, created while the section text is created.
        self._word_count = -1

    def __str__(self):
        string = ''

        string += "Section [" + self._type + "]\n"

        for line in self.lines:
            string += line.__str__() + '\n'

        string += '\n'

        return string

    @property
    def text(self):
        """Return the content of the section as string."""

        # If the section has no content, then no need to print
        # the wrappers.
        inner_text = self._get_inner_text()
        if len(inner_text) == 0:
            return ''

        # We print the wrappers and the content (content is guranteed).
        string  = self._pre_section_text
        string += inner_text
        string += self._post_section_text
        string += '\n'

        return string

    @property
    def lines(self):
        """Returns the _lines."""

        return self._lines

    @property
    def type(self):
        """Returns the type set by the daughter classes."""

        return self._type

    @property
    def word_count(self):
        """Returns the word count of the section."""

        # Return the calculated value.
        if self._word_count > -1:
            return self._word_count

        self._word_count = 0
        # Sum the word count from each line object.
        for line in self._lines:
            self._word_count += line.word_count

        return self._word_count

    @property
    def line_count(self):
        """Get the number of printable lines in the draft."""

        self._line_count = 0

        for line in self.lines:
            if len(line.text) > 0:
                self._line_count += 1

        return self._line_count

    def add_line(self, line_obj):
        """Add a line object `Line` to the section."""

        self._lines.append(line_obj)

    def clone(self, target_section, draft_line_number = 0):
        """Clones the printable lines from the target section."""

        for line in target_section.lines:
            if line.is_printable:
                new_line = Line(line._original_text, draft_line_number = draft_line_number)
                self.add_line(new_line)

    def _get_inner_text(self):
        """Returns the string with the content of the section."""

        # Return the calculated text if available.
        if self._inner_text is not None:
            return self._inner_text

        self._inner_text = ""

        for line in self.lines:
            if len(line.text) > 0:
                self._inner_text += line.text + "\n"

        # Remove last training end of line.
        self._inner_text  = self._inner_text.strip()

        return self._inner_text
