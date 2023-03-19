#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Carlos Ramos.

from letrista.section import Section

class UnassignedSection(Section):
    """Represents a song/lyrics section within `Draft` object."""

    def __init__(self):
        """Starts as an unassigned section."""

        super().__init__()

        self._type = Section.TYPE_UNASSIGNED;

    @property
    def text(self):
        """The unassigned section just returns... nothing."""

        return ''

    @property
    def word_count(self):
        """The unassigned section lines do not count towards the word total."""

        return 0

    @property
    def line_count(self):
        """Lines in the unassigned section do not count."""

        return 0
