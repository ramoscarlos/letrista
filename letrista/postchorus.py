#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Carlos Ramos.

from letrista.section import Section

class Postchorus(Section):
    """Represents a pre-chorus section within the `Draft` object."""

    def __init__(self):
        """Initializes the section as a post-chorus."""

        super().__init__()

        self._type = Section.TYPE_POSTCHORUS
        self._pre_section_text = '$$'
        self._post_section_text = '$$'
