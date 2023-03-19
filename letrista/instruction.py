#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Carlos Ramos.

from letrista.section import Section
from letrista.title import Title
from letrista.intro import Intro
from letrista.verse import Verse
from letrista.prechorus import Prechorus
from letrista.chorus import Chorus
from letrista.postchorus import Postchorus
from letrista.bridge import Bridge
from letrista.outro import Outro

class Instruction:
    """Represents an instruction to be parsed by the `Draft` object."""

    # Allowed identifiers for sections.
    SECTION_IDENTIFIERS = {
        Section.TYPE_TITLE: {
            'Title',  # English
            'Título', # Spanish
            'Titulo', # Spanish
        },
        Section.TYPE_VERSE: (
            'Verse', # English
            'Verso', # Spanish
        ),
        Section.TYPE_CHORUS: (
            'Chorus', # English
            'Coro',   # Spanish
        ),
        Section.TYPE_PRECHORUS: (
            'Pre-chorus', # English
            'Prechorus',  # English
            'Pre-coro',   # Spanish
            'Precoro',    # Spanish
        ),
        Section.TYPE_POSTCHORUS: (
            'Post-chorus', # English
            'Postchorus',  # English
            'Post-coro',   # Spanish
            'Postcoro',    # Spanish
        ),
        Section.TYPE_BRIDGE: (
            'Bridge', # English
            'Puente'  # Spanish
        ),
        Section.TYPE_INTRO: (
            'Intro', # English/Spanish
        ),
        Section.TYPE_OUTRO: (
            'Outro', # English/Spanish
        ),
    }

    def __init__(self, text):
        """Receives the instruction text (all the "[..." text)."""

        self._section_type = None
        self._instruction_text = text

    @property
    def is_repeat(self):
        """Determines if the instruction is to repeat an existing section."""

        self._is_repeat = False

        if self._instruction_text.find("R]") > 0:
            self._is_repeat = True

        return self._is_repeat

    @property
    def section_to_repeat(self):
        """Gets the id of the section to be repeated."""

        # If no indicator to repeat, we do not repeat.
        if not self.is_repeat:
            return ''

        # The id is given by the Section.TYPE constant, regardless of the
        # language used (i.e. 'Chorus' or 'Coro')
        # Therefore, is useless to trim the section type, hence why there
        # is a blind search for digits.
        # This is based on https://stackoverflow.com/a/36434101
        number_id = int('0' + ''.join(filter(str.isdigit, self._instruction_text)))

        if number_id <= 0:
            number_id = '1'

        self._section_to_repeat = self.section_type + str(number_id)

        return self._section_to_repeat

    @property
    def section_type(self):
        """Determines the type of section to be created."""

        if self._section_type is not None:
            return self._section_type

        # Check the types of section based on the priority above.
        for section_type in self.SECTION_IDENTIFIERS:
            # Check each identifier within the entry.
            for identifier in self.SECTION_IDENTIFIERS[section_type]:
                # If there is a match, set section type.
                if self._instruction_text.startswith('[' + identifier):
                    self._section_type = section_type

                    break

        # In order to be forgiving, if we have not found a match,
        # we will generate a 'Verse' section.
        if self._section_type is None:
            self._section_type = Section.TYPE_VERSE

        return self._section_type

    def create_section(self):
        """Creates the `Section` object based on type."""

        if self.section_type == Section.TYPE_TITLE:
            return Title()
        if self.section_type == Section.TYPE_CHORUS:
            return Chorus()
        elif self.section_type == Section.TYPE_BRIDGE:
            return Bridge()
        elif self.section_type == Section.TYPE_POSTCHORUS:
            return Postchorus()
        elif self.section_type == Section.TYPE_PRECHORUS:
            return Prechorus()
        elif self.section_type == Section.TYPE_INTRO:
            return Intro()
        elif self.section_type == Section.TYPE_OUTRO:
            return Outro()
        else:
            return Verse()
