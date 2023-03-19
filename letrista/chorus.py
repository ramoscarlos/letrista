#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Carlos Ramos.

from letrista.section import Section

class Chorus(Section):
    """Represents a chorus section within the `Draft` object."""

    def __init__(self):
        """Initializes the section as a chorus."""

        super().__init__()

        self._type = Section.TYPE_CHORUS
        self._pre_section_text = '**'
        self._post_section_text = '**'
