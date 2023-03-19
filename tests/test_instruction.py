#!/usr/bin/env python3

"""Tests for `unassigned_section` class."""

import pytest

from letrista.instruction import Instruction
from letrista.section import Section
from letrista.verse import Verse
from letrista.chorus import Chorus
from letrista.prechorus import Prechorus
from letrista.postchorus import Postchorus
from letrista.bridge import Bridge
from letrista.intro import Intro
from letrista.outro import Outro
from letrista.title import Title

def test_instruction_fails_if_no_text_provided():
    """Creates an Instruction."""

    with pytest.raises(TypeError) as e_info:
        ins = Instruction()

    assert 'required positional argument' in str(e_info.value)

def test_instruction_is_created():
    """Creates an Instruction."""

    ins = Instruction('[Pewpew]')

###########################################################
##### Test that instruction detects section correctly #####
###########################################################

def test_instruction_type_is_verse():
    """Creates an Instruction with type 'Verse' from 'Verse'."""

    ins = Instruction('[Verse]')

    assert 'Verse' == ins.section_type

def test_instruction_type_is_verse_from_verso():
    """Creates an Instruction with type 'Verse' from 'Verso'."""

    ins = Instruction('[Verso]')

    assert 'Verse' == ins.section_type

def test_instruction_type_is_chorus():
    """Creates an Instruction with type 'Chorus' from 'Chorus'."""

    ins = Instruction('[Chorus]')

    assert 'Chorus' == ins.section_type

def test_instruction_type_is_chorus_from_coro():
    """Creates an Instruction with type 'Chorus' from 'Coro'."""

    ins = Instruction('[Coro]')

    assert 'Chorus' == ins.section_type

def test_instruction_type_is_prechorus():
    """Creates an Instruction with type 'Pre-chorus' from 'Pre-chorus'."""

    ins = Instruction('[Pre-chorus]')

    assert 'Pre-chorus' == ins.section_type

def test_instruction_type_is_prechorus_with_no_dash():
    """Creates an Instruction with type 'Pre-chorus' from 'Prechorus'."""

    ins = Instruction('[Prechorus]')

    assert 'Pre-chorus' == ins.section_type

def test_instruction_type_is_prechorus():
    """Creates an Instruction with type 'Pre-chorus' from 'Pre-coro'."""

    ins = Instruction('[Pre-coro]')

    assert 'Pre-chorus' == ins.section_type

def test_instruction_type_is_prechorus():
    """Creates an Instruction with type 'Pre-chorus' from 'Precoro'."""

    ins = Instruction('[Precoro]')

    assert 'Pre-chorus' == ins.section_type

def test_instruction_type_is_postchorus():
    """Creates an Instruction with type 'Post-chorus' from 'Post-chorus'."""

    ins = Instruction('[Post-chorus]')

    assert 'Post-chorus' == ins.section_type

def test_instruction_type_is_postchorus_with_no_dash():
    """Creates an Instruction with type 'Post-chorus' from 'Postchorus'."""

    ins = Instruction('[Postchorus]')

    assert 'Post-chorus' == ins.section_type

def test_instruction_type_is_postchorus():
    """Creates an Instruction with type 'Post-chorus' from 'Post-coro'."""

    ins = Instruction('[Post-coro]')

    assert 'Post-chorus' == ins.section_type

def test_instruction_type_is_postchorus():
    """Creates an Instruction with type 'Post-chorus' from 'Postcoro'."""

    ins = Instruction('[Postcoro]')

    assert 'Post-chorus' == ins.section_type

def test_instruction_type_is_intro_from_intro():
    """Creates an Instruction with type 'Intro' from 'Intro'."""

    ins = Instruction('[Intro]')

    assert 'Intro' == ins.section_type

def test_instruction_type_is_intro_from_introduccion():
    """Creates an Instruction with type 'Intro' from 'Introduccion'."""

    ins = Instruction('[Introduccion]')

    assert 'Intro' == ins.section_type

def test_instruction_type_is_intro_from_introduccioon():
    """Creates an Instruction with type 'Intro' from 'Introducción'."""

    ins = Instruction('[Introducción]')

    assert 'Intro' == ins.section_type

def test_instruction_type_is_outro_from_outro():
    """Creates an Instruction with type 'Intro' from 'Intro'."""

    ins = Instruction('[Outro]')

    assert 'Outro' == ins.section_type

def test_instruction_type_is_verse_from_garbage():
    """Creates an Instruction with type 'Verse' from 'PewPew'."""

    ins = Instruction('[PewPew]')

    assert 'Verse' == ins.section_type

###########################################################
##### Test the correct section objects are created    #####
###########################################################

def test_verse_is_created_from_instruction():
    """Instruction returns a `Verse`."""

    ins = Instruction('[Verse]')

    assert isinstance(ins.create_section(), Verse)

def test_chorus_is_created_from_instruction():
    """Instruction returns a `Chorus`."""

    ins = Instruction('[Chorus]')

    assert isinstance(ins.create_section(), Chorus)

def test_prechorus_is_created_from_instruction():
    """Instruction returns a `Prechorus`."""

    ins = Instruction('[Prechorus]')

    assert isinstance(ins.create_section(), Prechorus)

def test_postchorus_is_created_from_instruction():
    """Instruction returns a `Postchorus`."""

    ins = Instruction('[Postchorus]')

    assert isinstance(ins.create_section(), Postchorus)

def test_bridge_is_created_from_instruction():
    """Instruction returns a `Bridge`."""

    ins = Instruction('[Bridge]')

    assert isinstance(ins.create_section(), Bridge)

def test_intro_is_created_from_instruction():
    """Instruction returns a `Intro`."""

    ins = Instruction('[Intro]')

    assert isinstance(ins.create_section(), Intro)

def test_outro_is_created_from_instruction():
    """Instruction returns a `Outro`."""

    ins = Instruction('[Outro]')

    assert isinstance(ins.create_section(), Outro)

def test_title_is_created_from_instruction():
    """Instruction returns a `Title`."""

    ins = Instruction('[Title]')

    assert isinstance(ins.create_section(), Title)

###########################################################
##### Test repeat instructions work                   #####
###########################################################

def test_section_to_repeat_is_empty_if_no_indicator():
    """Test that the section to repeat is empty if no "R]" is found."""

    ins = Instruction('[Chorus]')

    assert ins.section_to_repeat == ''

def test_repeat_indicator_is_detected():
    """Test if the trailing "R]" gets picked as indicator."""

    ins = Instruction('[ChorusR]')

    assert ins.is_repeat is True
    assert ins.section_type == Section.TYPE_CHORUS

def test_repeat_indicator_is_detected_with_spanish_coro():
    """Test if the trailing "R]" gets picked as indicator."""

    ins = Instruction('[CoroR]')

    assert ins.is_repeat is True
    assert ins.section_type == Section.TYPE_CHORUS

def test_section_id_to_be_repeated_is_correct_without_number():
    """Test if the id of section to be repeated is correct (without number)."""

    ins = Instruction('[ChorusR]')

    assert ins.section_to_repeat == 'Chorus1'

def test_section_id_to_be_repeated_is_correct_with_spanish_coro_without_number():
    """Test if the id of section to be repeated is correct, using Spanish 'Coro' (no number)."""

    ins = Instruction('[CoroR]')

    assert ins.section_to_repeat == 'Chorus1'

def test_section_id_to_be_repeated_is_correct_with_number_2():
    """Test if the id of section to be repeated is correct (using number 2)."""

    ins = Instruction('[Chorus2R]')

    assert ins.section_to_repeat == 'Chorus2'

def test_section_id_to_be_repeated_is_correct_with_spanish_coro_with_number_2():
    """Test if the id of section to be repeated is correct, using Spanish 'Coro'."""

    ins = Instruction('[Coro2R]')

    assert ins.section_to_repeat == 'Chorus2'
