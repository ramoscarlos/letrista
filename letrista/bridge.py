#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Carlos Ramos.

from letrista.section import Section

class Bridge(Section):
    """Represents a bridge within the `Draft` object."""

    def __init__(self):
        """Starts a bridge."""

        super().__init__()

        self._type = Section.TYPE_BRIDGE;
        self._pre_section_text = '_'
        self._post_section_text = '_'
