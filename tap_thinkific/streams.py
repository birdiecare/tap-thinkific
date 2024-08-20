"""Stream type classes for tap-thinkific."""

from __future__ import annotations

import sys
from typing import Any, Dict, Optional

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_thinkific.client import ThinkificStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"

class CoursesStream(ThinkificStream):
    """Define stream for /courses endpoint."""
    name = "courses"
    path = "/courses"
    primary_keys = ["id"]

    schema_filepath = SCHEMAS_DIR / "Courses.json"


class EnrollmentsStream(ThinkificStream):
    """Define stream for /enrollments endpoint."""
    name = "enrollments"
    path = "/enrollments"
    primary_keys = ["id"]
    replication_key = "updated_at"

    schema_filepath = SCHEMAS_DIR / "Enrollments.json"

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}

        params["query[updated_after]"] = self.get_starting_timestamp(context).strftime(self.api_date_format)

        if next_page_token:
            params["page"] = next_page_token

        return params