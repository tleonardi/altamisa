# -*- coding: utf-8 -*-
"""Tests for writing ISA study files"""


import filecmp
import pytest
import os

from altamisa.exceptions import ModerateIsaValidationWarning, IsaWarning, ParseIsatabWarning
from altamisa.isatab import (
    InvestigationReader,
    InvestigationValidator,
    StudyReader,
    StudyValidator,
    StudyWriter,
)
from .conftest import sort_file


# Helper to load, write and compare studies
def _parse_write_assert(investigation_file, tmp_path, quote=None):
    # Load investigation
    investigation = InvestigationReader.from_stream(investigation_file).read()
    InvestigationValidator(investigation).validate()
    directory = os.path.normpath(os.path.dirname(investigation_file.name))
    # Iterate studies
    for s, study_info in enumerate(investigation.studies):
        # Load study
        path_in = os.path.join(directory, study_info.info.path)
        with open(path_in, "rt") as inputf:
            study = StudyReader.from_stream("S{}".format(s + 1), inputf).read()
        StudyValidator(investigation, study_info, study).validate()
        # Write study to temporary file
        path_out = tmp_path / study_info.info.path
        with open(path_out, "wt", newline="") as file:
            StudyWriter.from_stream(study, file, quote=quote).write()
        # Sort and compare input and output
        path_in_s = tmp_path / (study_info.info.path.name + ".in.sorted")
        path_out_s = tmp_path / (study_info.info.path.name + ".out.sorted")
        assert filecmp.cmp(
            sort_file(path_in, path_in_s), sort_file(path_out, path_out_s), shallow=False
        )


def test_study_writer_minimal(minimal_investigation_file, tmp_path):
    with pytest.warns(IsaWarning) as record:
        _parse_write_assert(minimal_investigation_file, tmp_path)
    # Check warnings
    assert 1 == len(record)


def test_study_writer_minimal2(minimal2_investigation_file, tmp_path):
    with pytest.warns(IsaWarning) as record:
        _parse_write_assert(minimal2_investigation_file, tmp_path)
    # Check warnings
    assert 1 == len(record)


def test_study_writer_small(small_investigation_file, tmp_path):
    with pytest.warns(IsaWarning) as record:
        _parse_write_assert(small_investigation_file, tmp_path)
    # Check warnings
    assert 1 == len(record)


def test_study_writer_small2(small2_investigation_file, tmp_path):
    _parse_write_assert(small2_investigation_file, tmp_path)


def test_study_writer_BII_I_1(BII_I_1_investigation_file, tmp_path):
    with pytest.warns(IsaWarning) as record:
        _parse_write_assert(BII_I_1_investigation_file, tmp_path, quote='"')
    # Check warnings
    assert 1 == len(record)


def test_study_writer_gelelect(gelelect_investigation_file, tmp_path):
    with pytest.warns(IsaWarning) as record:
        _parse_write_assert(gelelect_investigation_file, tmp_path, quote='"')
    # Check warnings
    assert 2 == len(record)
    msg = "Skipping empty ontology source: , , , "
    assert record[0].category == ParseIsatabWarning
    assert str(record[0].message) == msg
    msg = "Study without title:\nID:\tstudy01\nTitle:\t\nPath:\ts_study01.txt"
    assert record[1].category == ModerateIsaValidationWarning
    assert str(record[1].message) == msg
