"""Tests standard tap features using the built-in SDK tests library."""

import datetime
# from dotenv import load_dotenv
import os
import pytest

from singer_sdk.testing import get_standard_tap_tests

from tap_thinkific.tap import Tapthinkific

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "api_key":  os.getenv('THINKIFIC_API_KEY'),
    "subdomain": os.getenv('THINKIFIC_SUBDOMAIN')
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(
        Tapthinkific,
        config=SAMPLE_CONFIG
    )
    for test in tests:
        test()


# Create additional tests as appropriate for your tap.
