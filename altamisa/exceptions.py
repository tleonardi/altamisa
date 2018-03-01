# -*- coding: utf-8 -*-
"""Exceptions and Warnings for the Altamisa library.
"""

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@bihealth.de>'


class IsaException(Exception):
    """Base class for exceptions raised by Altamisa"""


class ParseIsatabException(IsaException):
    """Exception raised on problems parsing ISA-TAB"""


class IsaWarning(Warning):
    """Base class for warnings raised by Altamisa"""


class ParseIsatabWarning(IsaWarning):
    """Warning raised on problems parsing ISA-TAB"""
