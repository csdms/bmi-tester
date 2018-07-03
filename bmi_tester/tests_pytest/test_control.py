#! /usr/bin/env python
import pytest

from . import Bmi, INPUT_FILE


def test_has_initialize(new_bmi):
    """Test component has an initialize method."""
    assert hasattr(new_bmi, "initialize")


def test_initialize(new_bmi):
    """Test component can initialize itself."""
    bmi = Bmi()
    assert bmi.initialize(INPUT_FILE) is None


def test_update(new_bmi):
    """Test component can update itself."""
    assert new_bmi.update() is None


def test_has_finalize(new_bmi):
    """Test component has a finalize method."""
    assert hasattr(new_bmi, "finalize")
