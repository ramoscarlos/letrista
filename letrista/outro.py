#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Carlos Ramos.

from letrista.section import Section

class Outro(Section):
    """Represents the outro section within the `Draft` object."""

    def __init__(self):
        """Initializes the section as outro."""

        super().__init__()

        self._type = Section.TYPE_OUTRO
        self._pre_section_text = '**_'
        self._post_section_text = '_**'
