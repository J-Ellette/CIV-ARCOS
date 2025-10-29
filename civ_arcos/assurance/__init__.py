"""
Assurance case builder module.
Implements CertGATE-style Digital Assurance Cases (DACs) with GSN notation.
"""

from .gsn import (
    GSNNode,
    GSNNodeType,
    GSNGoal,
    GSNStrategy,
    GSNSolution,
    GSNContext,
    GSNAssumption,
    GSNJustification,
)
from .case import AssuranceCase, AssuranceCaseBuilder
from .templates import ArgumentTemplate, TemplateLibrary
from .patterns import PatternInstantiator, ProjectType

__all__ = [
    "GSNNode",
    "GSNNodeType",
    "GSNGoal",
    "GSNStrategy",
    "GSNSolution",
    "GSNContext",
    "GSNAssumption",
    "GSNJustification",
    "AssuranceCase",
    "AssuranceCaseBuilder",
    "ArgumentTemplate",
    "TemplateLibrary",
    "PatternInstantiator",
    "ProjectType",
]
