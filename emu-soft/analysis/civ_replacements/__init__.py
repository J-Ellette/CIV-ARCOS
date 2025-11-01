"""
CIV-Scripts: Custom implementations replacing external tools.

This module provides replacements for external Python tools and standard library modules:
- civ_cov: Replacement for coverage.py (CodeCoverage)
- civ_pyt: Replacement for pytest (TestRunner)
- civ_my: Replacement for mypy (TypeChecker)
- civ_bla: Replacement for black (CodeFormatter)
- civ_fla: Replacement for flake8 (CodeLinter)
- submarine: Replacement for subprocess (Submarine)  
- jason: Replacement/wrapper for json (Jason)
- hashish: Replacement/wrapper for hashlib (Hashish)
- hamburger: Replacement/wrapper for hmac (Hamburger)
- pathfinder: Replacement/wrapper for pathlib (PathFinder)
"""

from .civ_cov import *

# Make replacements easily importable
try:
    from .submarine import *
except ImportError:
    pass

try:
    from .jason import *
except ImportError:
    pass

try:
    from .hashish import *
except ImportError:
    pass

try:
    from .hamburger import *
except ImportError:
    pass

try:
    from .pathfinder import *
except ImportError:
    pass
