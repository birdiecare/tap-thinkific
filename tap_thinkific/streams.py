"""Stream type classes for tap-thinkific."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_thinkific.client import thinkificStream

# Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class EnrollmentsStream(thinkificStream):
    """Define stream for /enrollments endpoint."""
    name = "enrollments"
    path = "/enrollments"
    primary_keys = ["id"]
    replication_key = "updated_at"
    
    schema_filepath = SCHEMAS_DIR / "Enrollments.json"