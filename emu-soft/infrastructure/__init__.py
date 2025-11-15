"""
Core infrastructure emulations for CIV-ARCOS.

This package contains emulations of common infrastructure components,
implemented without external dependencies.

Components:
- cache.py: Redis emulator - in-memory caching with pub/sub
- tasks.py: Celery emulator - background task processing
- framework.py: Web framework emulator (FastAPI/Flask-like)
- graph.py: Neo4j emulator - graph database
"""

__version__ = "1.0.0"
