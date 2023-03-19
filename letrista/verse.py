#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Carlos Ramos.

from letrista.section import Section

class Verse(Section):
    """Represents verse within the `Draft` object."""

    def __init__(self):
        """Starts a verse."""

        super().__init__()

        self._type = Section.TYPE_VERSE;
