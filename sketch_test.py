#!/usr/bin/env python3
"""
@created 14/04/17
@author sbr

**This file contains the unit tests for Sketch, using the pytest framework.**
"""

from _curses import *
import os as _os
import sys as _sys
from pytest import fixture
from . import sketch


@fixture(scope="module")
def initscr():
    import _curses, curses
    setupterm(
        term=_os.environ.get("TERM", "unknown"), fd=_sys.__stdout__.fileno())
    stdscr = _curses.initscr()
    for key, value in _curses.__dict__.items():
        if key[0:4] == 'ACS_' or key in ('LINES', 'COLS'):
            setattr(curses, key, value)
    return stdscr


@fixture(scope="module")
def blank_pad():
    return sketch.Pad()


@fixture(scope="module")
def pad_15():
    cmd = ['c', 15, 15]
    pad, _ = sketch.Pad().new(cmd)
    return pad


def test_new_pad_sucess(initscr, blank_pad):
    cmd = ['c', 15, 15]
    pad, err = blank_pad.new(cmd)
    assert err == None


def test_new_pad_fail(initscr, blank_pad):
    cmd = ['c', 500, 500]
    pad, err = blank_pad.new(cmd)
    assert err


def test_line_stored_in_history(initscr, pad_15):
    cmd = ['l', 1, 2, 1, 10]
    err = pad_15.draw(cmd)
    assert [5, 1] in pad_15.history


def test_draw_before_pad_ready(initscr):
    cmd = ['l', 1, 2, 1, 20]
    assert sketch.Pad().draw(
        cmd) == "Cant start drawing until your pad's ready"


def test_draw_line_outside_pad(initscr, pad_15):
    cmd = ['l', 1, 2, 1, 20]
    assert pad_15.draw(cmd) == "Stay on the pad!"


def test_draw_line_incomplete_input(initscr, pad_15):
    cmd = ['l', 1, 1, 20]
    assert pad_15.draw(
        cmd) == "Incorrect input, requires pos_x1, pos_y1, pos_x2, pos_y2"


def test_draw_bucket_incomplete_input(initscr, pad_15):
    cmd = ['b', 1, 'o']
    assert pad_15.draw(cmd) == "Incorrect input, required pos_x1, pos_y1, c"


def test_draw_rectangle_outside_pad(initscr, pad_15):
    cmd = ['r', 1, 5, 10, 20]
    assert pad_15.draw(cmd) == "Stay on the pad!"


def test_draw_bucket_outside_pad(initscr, pad_15):
    cmd = ['b', 1, 20, 'o']
    assert pad_15.draw(cmd) == "Stay on the pad!"


def test_draw_incorrect_rectangle(initscr, pad_15):
    cmd = ['r', 1, 5, 1, 10]
    assert pad_15.draw(
        cmd) == "pos_x2 and pos_y2 need to be larger than pos_x1 and pos_y1"
