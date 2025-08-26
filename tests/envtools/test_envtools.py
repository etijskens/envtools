# -*- coding: utf-8 -*-

"""Tests for envtools package."""

import sys
sys.path.insert(0,'.')

import envtools


def test_platform():
    assert envtools.platform in ('darwin', 'linux')


def test_cluster():
    """"""


# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_platform

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')

# eof