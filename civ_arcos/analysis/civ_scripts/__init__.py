"""
CIV-Scripts: Custom implementations replacing external tools.

This module provides replacements for external Python tools and standard library modules:
- civ_cov: Replacement for coverage.py (CodeCoverage)
- civ_pyt: Replacement for pytest (TestRunner)
- civ_my: Replacement for mypy (TypeChecker)
- civ_bla: Replacement for black (CodeFormatter)
- civ_fla: Replacement for flake8 (CodeLinter)
- submarine: Wrapper for subprocess (Submarine)  
- jason: Wrapper for json (Jason)
- hashish: Wrapper for hashlib (Hashish)
- hamburger: Wrapper for hmac (Hamburger)
- pathfinder: Wrapper for pathlib (PathFinder)
- asterisk: Wrapper for ast (Asterisk)
- webfetch: Wrapper for urllib (WebFetch)
- dataclass: Wrapper for dataclasses (DataClass)
- enumeration: Wrapper for enum (Enumeration)
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

try:
    from .asterisk import *
except ImportError:
    pass

try:
    from .webfetch import *
except ImportError:
    pass

try:
    from .dataclass import *
except ImportError:
    pass

try:
    from .enumeration import *
except ImportError:
    pass
