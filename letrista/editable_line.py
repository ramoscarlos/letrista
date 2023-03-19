#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Carlos Ramos.

from letrista.line import Line

class EditableLine(Line):
    """Line class that adds methods to edit a line with markup.


    Pretty much, the methods here yield no difference over the output
    (that is, if you are not in editing mode).

    There is no use for a count of words if you are not going to display
    it anywhere (hence, all the metadata about the lyrics is reserved to this
    "super-class" of line).

    This class adds the following methods to the `Line` class:
        comment()
        uncomment()
        toggle_comment()
        add_syllable_count()
    """

    def comment(self):
        """Comments the current line.

        A comment is any line with a '-' in the second character of any given line.
        The exclusion to this is the end of line made up of dashes.

        If line is commented, this has no effect. If line is uncommented,
        it gets commented.
        """

        # Do nothing with commented or ignored lines.
        if self.type in (Line.TYPE_COMMENT, Line.TYPE_IGNORED):
            return

        if (self.type in (Line.TYPE_SCHEMA, Line.TYPE_COUNT)
            and self._original_text[1] == ' '):
            # If the line is has schema or count, we define what to do based on our second position.
            self._original_text = self._original_text[0] + '-' + self._original_text[2:]
        else:
            # For everything else, we just append two dashes at the beginning.
            self._original_text = '--' + self._original_text;

        # Reset the type (for if this happens to be a TYPE_END line).
        self._type = self.TYPE_UNSET

    def uncomment(self):
        """Removes the comment symbol from a given line."""

        # Do nothing to non-comment lines.
        if self.type is not Line.TYPE_COMMENT:
            return

        if self._original_text.startswith('--'):
            self._original_text = self._original_text[2:]
        else:
            self._original_text = self._original_text[0] + ' ' + self._original_text[2:]

        # Reset the type.
        self._type = self.TYPE_UNSET

    def toggle_comment(self):
        """Comments an uncommented line. Uncomments a commented one."""

        if self.type == Line.TYPE_COMMENT:
            self.uncomment()
        else:
            self.comment()

    def add_syllable_count(self):
        """Adds the syllable count to a line that qualifies.

        The line that qualify are the next ones:
          - Lines of type TYPE_LYRICS
          - Lines of type TYPE_SCHEMA
          - Lines of type TYPE_SKIP

        The instructions, end of lyrics, and the ones already have count
        do not qualify.
        """

        if self.type not in (Line.TYPE_LYRICS, Line.TYPE_SCHEMA, Line.TYPE_SKIP):
            return

        # Add the default count if has schema. Schema and count otherwise.
        if self.type == Line.TYPE_SCHEMA:
            self._original_text = self._original_text[0] + ' __ ' + self._original_text[2:]
        else:
            self._original_text = 'X __ ' + self._original_text
        # New type is TYPE_COUNT.
        self._type = self.TYPE_COUNT
