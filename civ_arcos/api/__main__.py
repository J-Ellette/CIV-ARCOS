"""
Main entry point for CIV-ARCOS API server.

This allows running the server with:
    python -m civ_arcos.api
"""

# The main API server code is in the parent api.py file, not in this package
# We need to import it correctly
import importlib.util
import os
import sys

# Get the path to the api.py file in the parent directory
api_py_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'api.py')

# Load the api.py module directly
spec = importlib.util.spec_from_file_location("civ_arcos_api", api_py_path)
api_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_module)

if __name__ == "__main__":
    api_module.main()