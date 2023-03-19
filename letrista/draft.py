#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Carlos Ramos.

# Used because Sublime Text has Python 3.3,
# which has unordered dictionaries.
from collections import OrderedDict

from letrista.line import Line
from letrista.section import Section
from letrista.unassigned_section import UnassignedSection
from letrista.instruction import Instruction

class Draft:
    """Contains and clasifies all lines in the draft.

    This class receives all the lines within the draft
    and formats them to generate lyrics in the marke37
    markdown format, for its transformation using said
    package into a common friendly format.

    It uses the following internal variables to keep tabs:

    _draft_lyrics:
        A string with all the text of the draft.
    string_list:
        Takes [_draft_lyrics] and explodes them.
    """

    def __init__(self, draft_lyrics = ''):
        """Generates the draft from the initial string."""

        self._draft_lyrics = draft_lyrics

        self._section_count = {
            # This value of unassigned is hardcoded since is only one.
            Section.TYPE_UNASSIGNED: 1,
            Section.TYPE_TITLE: 0,
            Section.TYPE_INTRO: 0,
            Section.TYPE_VERSE: 0,
            Section.TYPE_PRECHORUS: 0,
            Section.TYPE_CHORUS: 0,
            Section.TYPE_POSTCHORUS: 0,
            Section.TYPE_BRIDGE: 0,
            Section.TYPE_OUTRO: 0,
        }

        # Make sure the last line has end of line.
        if len(draft_lyrics) > 0 and draft_lyrics[-1] != '\n':
            self._draft_lyrics = self._draft_lyrics + '\n'

        # Draft word count.
        self._word_count = -1

    @property
    def string_list(self):
        """Returns the draft lyrics as a list (an item per line)."""

        # Split the string into a list for processing.
        self._string_list = self._draft_lyrics.splitlines()

        return self._string_list

    @property
    def draft_line_count(self):
        """Returns the [unprocessed] number of lines the draft has.

        Returns the total number of lines the draft has. That is, line you
        write, line that gets counted. This is the total prior to any
        processing, and is used to pass the original line number to the line
        object, in case a problem in processing occurs, we know the original
        number within the draft (or draft_line_number).
        """

        return len(self.string_list)

    @property
    def lines(self):
        """Lines in the draft (as Line objects)."""

        self._lines = []

        for index, line_str in enumerate(self.string_list):
            self._lines.append(Line(line_str, draft_line_number = (index + 1)))

        return self._lines

    @property
    def text(self):
        """Return the processed text."""

        text = ''

        for section in self._sections.values():
            # Make sure the section has content.
            if section.word_count > 0:
                text += section.text
                text += '\n'

        text = text.strip()

        self._text = text

        return self._text

    @property
    def word_count(self):
        """Returns the word count of the printable lines."""

        # Return the calculated value.
        if self._word_count > -1:
            return self._word_count

        self._word_count = 0
        # Sum the word count from each section.
        for section in self._sections:
            wc = self._sections[section].word_count
            self._word_count += wc

        return self._word_count

    @property
    def line_count(self):
        """Line count in the draft."""

        self._line_count = 0

        for section in self._sections.values():
            if section.line_count > 0:
                self._line_count += section.line_count

        return self._line_count

    def add_text(self, new_lines):
        """Adds lines (as text) to the draft.

        Adds an arbitrary amount of new lines (including one) to the current
        draft lyrics, ensuring it has the end of line character at the end.
        """

        self._draft_lyrics = self._draft_lyrics + new_lines

        if len(new_lines) > 0 and new_lines[-1] != '\n':
            self._draft_lyrics = self._draft_lyrics + '\n'

        return self._draft_lyrics

    def add_file(self, file_path):
        """Adds the content of a file as string."""

        f = open(file_path, "r")

        # Call the function that adds text.
        self.add_text(f.read())

    def to_marke37(self):
        """Generates the marke37 lyrics markup from the draft."""

        self.process_lines()

        return self.text

    def process_lines(self):
        """Processes the lines `Line` in the list, to create the sections."""

        self._sections = OrderedDict()

        # Create an unassigned section, where everything will fall until
        # another section is created (hopefully the [Title]).
        self._sections['Unassigned1'] = self.__create_unassigned_section()

        # The current section will be the unassigned section.
        current_section = self._sections['Unassigned1']
        # Loop thru each object line to find which are instructions.
        for line in self.lines:
            if line.is_instruction:
                current_section = self.__parse_instruction(line)
            elif line.is_end_of_lyrics:
                break
            else:
                # If no instruction or end of lyrics, add line to section.
                current_section.add_line(line)

        return self._sections

    def __create_unassigned_section(self):
        """Creates the UnassignedSection"""

        unassigned_section = UnassignedSection()

        return unassigned_section

    def __parse_instruction(self, line):
        """Receives the instruction line to create a new section."""

        ins = Instruction(line.instruction_text)
        # Creates the id of the new section.
        self._section_count[ins.section_type] += 1
        new_section_id = ins.section_type + str(self._section_count[ins.section_type])

        self._sections[new_section_id] = ins.create_section()

        # Add the instruction line as first line.
        self._sections[new_section_id].add_line(line)

        # If instruction is a repeat instruction, clone lines.
        self.__parse_repeat_instruction(ins, self._sections[new_section_id])

        return self._sections[new_section_id]

    def __parse_repeat_instruction(self, instruction, current_section):
        """Copies the lines from another section into the new one."""

        # If instruction is not repeat, nothing to do here.
        if not instruction.is_repeat:
            return

        # If instruction type has nothing to be able to clone, we bail.
        if self._section_count[instruction.section_type] < 2:
            return

        # If target section is current section.
        current_section_id = current_section.type + str(self._section_count[instruction.section_type])
        if current_section_id == instruction.section_to_repeat:
            # If the ids are the same, we try to copy the first section in the draft.
            section_to_repeat = instruction.section_type + '1'
        else:
            # If not current section, we try to search for the given section number.
            section_to_repeat = instruction.section_to_repeat

        target_section = None
        # Look for the wanted section in the dictionary (as long as is not itself)
        if section_to_repeat in self._sections:
            target_section = self._sections[section_to_repeat]

        # If the id is not present, we assume the id is wrong, so we
        # default to the 'Section1'.
        if target_section is None:
            section_to_repeat = instruction.section_type + '1'
            if section_to_repeat in self._sections:
                target_section = self._sections[section_to_repeat]

        # Here, we already have the target section to clone.
        line_no = current_section.lines[0].draft_line_number
        current_section.clone(target_section, line_no)
