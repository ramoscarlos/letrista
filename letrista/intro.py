#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Carlos Ramos.

from letrista.section import Section

class Intro(Section):
    """Represents the intro section within the `Draft` object."""

    def __init__(self):
        """Initializes the section as intro."""

        super().__init__()

        self._type = Section.TYPE_INTRO
        self._pre_section_text = '_**'
        self._post_section_text = '**_'
