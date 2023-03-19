#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Carlos Ramos.

from letrista.section import Section

class Title(Section):
    """Represents the title of the `Draft` object."""

    def __init__(self):
        """Initializes the section as a title."""

        super().__init__()

        self._type = Section.TYPE_TITLE

    @property
    def line_count(self):
        """Lines in the title do not count."""

        return 0

    def _get_inner_text(self):
        """Return the first title available.

        If no title from all in the section, use 'Untitled'.
        """

        if self._inner_text is not None:
            return self._inner_text

        self._inner_text = ""

        for line in self.lines:
            if len(line.text) > 0:
                self._inner_text += line.text

                break

        if len(self._inner_text) == 0:
            self._inner_text = 'Untitled'

        ruler = '=' * len(self._inner_text)
        self._inner_text += '\n' + ruler

        return self._inner_text
