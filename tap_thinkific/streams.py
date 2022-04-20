"""Stream type classes for tap-thinkific."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_thinkific.client import thinkificStream

# Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class CoursesStream(thinkificStream):
    """Define stream for /courses endpoint."""
    name = "courses"
    path = "/courses"
    primary_keys = ["id"]
    
    schema_filepath = SCHEMAS_DIR / "Courses.json"

    
class EnrollmentsStream(thinkificStream):
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