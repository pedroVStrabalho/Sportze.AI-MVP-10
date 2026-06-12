# =============================================================================
# SPORTZE.AI - TRAINING CATALOG PACKAGE
# =============================================================================
# This file makes the training_catalog folder importable as a Python package.
#
# Example:
# from training_catalog.catalog_manager import get_training_session
# =============================================================================

from .catalog_manager import (
    get_training_session,
    get_catalog_sessions,
    get_available_fixed_sports,
    format_session_simple,
)

__all__ = [
    "get_training_session",
    "get_catalog_sessions",
    "get_available_fixed_sports",
    "format_session_simple",
]
