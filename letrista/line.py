#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Carlos Ramos.


class Line:
    """Represents a line within the draft.


    This class is used to represent a line within the draft (i.e. a line that
    belong to the lyrics, not to special instructions or aids during the writing
    or editing phase).

    A line within the draft may include the following characters:
      - An initial letter indicating the rhyme scheme.
      - A dash (-) at the second position, which makes a line a comment.
      - The syllable count at positions 3 and 4 (a two-digit padded number).
      - The rest of the text from position 5 and onwards.
      - Hats (^) can indicate a rhyme within the line.
      - Furthermore, a line can be within one of the following categories:
          + An instruction line.
          + Whitespace between lines (which does not trigger a change of section)
          + End of lyrics divider.

    The properties this class uses are:
      - _draft_line_number:
          to know the original number the line of text held in the draft.
      - _original_text:
          is the unprocessed text, as was received for the string list. As such,
          is the line of text without the end of line.
    """

    # Constants for line type.
    TYPE_UNSET       = 0  # The type of the line has not been yet determined
    TYPE_COUNT       = 1  # "X ## lyrics"  -- Includes rhyme scheme and syllable count
    TYPE_SCHEMA      = 2  # "X lyrics"     -- Includes only the rhyme scheme
    TYPE_SKIP        = 3  # "\n"           -- Just a line skip
    TYPE_LYRICS      = 4  # "lyrics"       -- Just lyrics, no indicators
    TYPE_INSTRUCTION = 5  # "["            -- Line that begins with "["
    TYPE_COMMENT     = 6  # "A-## lyrics"  -- Any line with "-" in second position
    TYPE_END         = 7  # "********"     -- End of lyrics (5 or more same char)
    TYPE_IGNORED     = 8  # Any line after the TYPE_END line.

    # Symbols used to mark the end of document or end of lyrics.
    SYMBOLS_FOR_EOD = ('*', '-', '#', '/')

    def __init__(self, text, draft_line_number = 0, eol_or_unassigned = False):
        """Creates the object with the text and original draft number.

        If the draft line number is not provided, is defaulted to zero.

        The type of the line is set here. Since the end of lyrics is reached
        at another line above, a bigger object is in charge of informing
        the current line that is no longer relevant. Therefore, we have the
        indicator `eol_or_unassigned` (end of lyrics reached, or still unassigned)
        to select the default type: is is either TYPE_UNSET or TYPE_IGNORED.
        """

        self._original_text = text
        self._draft_line_number = draft_line_number

        if eol_or_unassigned is True:
            self._type = self.TYPE_IGNORED
        else:
            self._type = self.TYPE_UNSET

    def __str__(self):
        """Returns the draft line number and original text."""

        string  = str(self._draft_line_number).zfill(3)
        string += " "
        string += self._original_text

        return string

    @property
    def type(self):
        """Returns the type of line we receive per markup.

        Checks for the presence of 'letrista' or 'e37' symbols that make
        up the lyrics, and decide which type (for more information on format,
        see the TYPE constants above).

        By default, the type chosen is `TYPE_UNSET`, which is pretty much a
        status prior to the calculations. This is done from the constructor.

        The TYPE_IGNORE also comes in only for the constructor (via flag).

        The priority of search is this:
          - TYPE_IGNORED:
              Check if that is the value, as it could have gotten here from the
              constructor (and by no other means).
          - TYPE_SKIP:
              A line with no text is an empty line (plus we validate the length).
          - TYPE_END:
              Since '-----' can be confused with a comment due to the second
              position, we look for the end of lyrics first.
          - TYPE_COMMENT:
              Since if the line is a comment, we do not care anymore, this is the
              second thing we look for.
          - TYPE_INSTRUCTION:
              Then, we check for the presence of the '[' that signals an instruction.
          - TYPE_COUNT:
              IF all else fails, then we look for actual lyrics. Here, we look at
              positions 3 and 4 (2 and 3 in programming) for digits, underscores, or xx.
              If any of that is true, we have a line with syllable count.
          - TYPE_SCHEMA:
              If it does not have a count, we check if we have at least two characters,
              excluding whitespace, and if the first one is uppercase, then we have the
              schema indicator in this line.
          - TYPE_LYRICS:
              If we do not have anything else special in the line, this is just lyrics.
        """

        text = self._original_text.strip()

        # First check: TYPE_UNSET or TYPE_IGNORED
        # This will return the TYPE_IGNORED if set in the constructor, or the
        # already calculated type from a prior run of this function.
        if self._type != self.TYPE_UNSET:
            return self._type

        # Second check: TYPE_SKIP
        if len(text) == 0:
            self._type = self.TYPE_SKIP

            # If we found a match, we return.
            return self._type

        # Third check: TYPE_END
        for symbol in self.SYMBOLS_FOR_EOD:
            # This test is performed with original text rather than the trimmed
            # version, since we want to ensure the ruler is at the beginning of
            # the line only.
            if self._original_text.startswith(symbol * 5):
                self._type = self.TYPE_END

                # If we found a match, we return.
                return self._type

        # Fourth check: TYPE_COMMENT
        if len(text) > 1 and text[1] == '-':
            self._type = self.TYPE_COMMENT

            # If we found a match, we return.
            return self._type

        # Fifth check: TYPE_INSTRUCTION
        if text.startswith('['):
            self._type = self.TYPE_INSTRUCTION

            # If we found a match, we return.
            return self._type

        # Sixth check: TYPE_COUNT
        if len(text) >= 4 and self.__line_has_count_indicator():
            self._type = self.TYPE_COUNT

            # If we found a match, we return.
            return self._type

        # Seventh check: TYPE_SCHEMA
        if len(text) >= 2 and self.__line_has_schema_indicator():
            self._type = self.TYPE_SCHEMA

            # If we found a match, we return.
            return self._type

        # Last check: TYPE_LYRICS (the only reason we should have reached this place)
        self._type = self.TYPE_LYRICS

        return self._type

    @property
    def text(self):
        """Returns the processed text of the line, depending on type"""

        empty_types = (
            self.TYPE_UNSET,       # Any unset line.
            self.TYPE_SKIP,        # Any empty line.
            self.TYPE_COMMENT,     # Any line that is a comment.
            self.TYPE_IGNORED,     # Any line after the end of lyrics.
            self.TYPE_INSTRUCTION, # Instructions do not print text.
            self.TYPE_END          # The end of lyrics also yields no text.
        )

        if self.type in empty_types:
            self._text = ''

            return self._text

        # With that, six of the nine types are done (and the processing starts).
        text = self._original_text.strip()

        # If TYPE_COUNT, remove the first five characters; if TYPE_SCHEMA, remove two.
        if self.type == self.TYPE_COUNT:
            text = text[5:]
        elif self.type == self.TYPE_SCHEMA:
            text = text[2:]

        # Find and strip the inline comments.
        text = self.__remove_inline_comments_from_text(text)
        # Find and strip the inner rhyme scheme.
        text = self.__remove_hat_inner_rhyme_scheme(text)

        # Assign the processed text to the output.
        self._text = text

        return self._text

    @property
    def draft_line_number(self):
        """Line number set at the constructor."""

        return self._draft_line_number

    @property
    def is_instruction(self):
        """Returns whether the current line is instruction or not."""

        return self.type == self.TYPE_INSTRUCTION

    @property
    def is_end_of_lyrics(self):
        """Returns whether the current line is end of lyrics or not."""

        return self.type == self.TYPE_END

    @property
    def instruction_text(self):
        """Returns the original text if we have an instruction line."""

        if self.is_instruction:
            self._instruction_text = self._original_text
        else:
            self.text

        return self._instruction_text

    @property
    def is_printable(self):
        """Determines if a line has content to print."""

        if len(self.text) > 0:
            return True

        return False

    @property
    def word_count(self):
        """Count the number of words in the printable text."""

        return len(self.text.split())

    def __line_has_count_indicator(self):
        """Determines if a line has the syllable count indicator.

        This functions looks at positions 3 and 4 (2 and 3 in programming)
        for the following patterns:
            [digit][digit]: Is the count of syllables.
            __: Two underscores used as an undetermined amount.
            xx: Used also as undetermined amount, wether caps or not.
        """

        text = self._original_text.lower()

        # There is a count indicator if those two positions are digits.
        if text[2].isdigit() and text[3].isdigit():
            return True

        # Or if the those two positions are '__':
        if text[2] == '_' and text[3] == '_':
            return True

        # Or if the those two positions are 'xx' (since this was lowered):
        if text[2] == 'x' and text[3] == 'x':
            return True

        return False

    def __line_has_schema_indicator(self):
        """Determines if a line of text has teh schema indicator.

        This really does not need a function of itself, unless one wants to
        add ignored syllables, such as 'A' (very common in English) and 'Y'
        (which is very common in Spanish).

        Since these are edge cases, I decided not to ignore them, as the line
        can be converted from:
          "A sunny day"
        to:
          "A A sunny day"
        being the first 'A' part of the rhyme scheme (therefore overriding the
        bad identification of the lyrics 'A').
        """

        text = self._original_text.strip()

        if text[0].isupper() and not text[1].isalnum():
            return True

        return False

    def __remove_inline_comments_from_text(self, text):
        """Finds and strips the inner comment, started with --, from the line."""
        comment_pos = text.find('--')
        if comment_pos > -1:
            text = text[:comment_pos].strip()

        return text

    def __remove_hat_inner_rhyme_scheme(self, text):
        """Removes the inner rhyme scheme, denoted by the ^A or ^00."""

        new_string = ''
        hat_flag = False

        for i in range(len(text)):
            if text[i] == '^':
                hat_flag = True
            elif hat_flag is True:
                if text[i].isupper():
                    # Hat flag is false, we skip this char but not the next.
                    hat_flag = False
                elif text[i].isdigit():
                    # Hat flag keeps on being True, to remove all digits.
                    hat_flag = True
                else:
                    new_string += text[i]
            else:
                # If no special condition, we just paste the character as is.
                new_string += text[i]

        return new_string
