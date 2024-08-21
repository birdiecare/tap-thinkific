"""Thinkific tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_thinkific import streams


class TapThinkific(Tap):
    """Thinkific tap class."""

    name = "tap-thinkific"

    config_jsonschema = th.PropertiesList(

        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="Thinkific API key. See https://developers.thinkific.com/api/api-key-auth."
        ),
        th.Property(
            "subdomain",
            th.StringType,
            required=True,
            description="Subdomain of the Thinkific site. See https://developers.thinkific.com/api/api-key-auth."
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Only sync records updated after this date."
        )

    ).to_dict()

    def discover_streams(self) -> list[streams.ThinkificStream]:
        """Return a list of available streams.
        """
        return [
            streams.CoursesStream(self),
            streams.EnrollmentsStream(self),
        ]


if __name__ == "__main__":
    TapThinkific.cli()
