"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os
import pytest
from dotenv import load_dotenv
load_dotenv()

from singer_sdk.testing import get_tap_test_class

from tap_thinkific.tap import TapThinkific

SAMPLE_CONFIG = {
    "start_date": "2024-07-01",
    "api_key":  os.getenv('THINKIFIC_API_KEY'),
    "subdomain": os.getenv('THINKIFIC_SUBDOMAIN')
}


# Run standard built-in tap tests from the SDK:
TestTapThinkific = get_tap_test_class(
    tap_class=TapThinkific,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
