"""Pytest configuration and fixtures."""
import pytest


@pytest.fixture
def mock_snb_response():
    """Mock SNB API response."""
    return {
        "timeseries": [
            {
                "header": [
                    {"dim": "Overview", "dimItem": "Switzerland - SNB policy rate"}
                ],
                "metadata": {
                    "key": "EPB@SNB.snboffzisa{LZ}",
                    "frequency": "P1M",
                    "scale": "",
                    "unit": "In percent"
                },
                "values": [
                    {"date": "2022-01", "value": -0.75},
                    {"date": "2022-06", "value": -0.25},
                    {"date": "2022-09", "value": 0.5},
                    {"date": "2023-06", "value": 1.75},
                    {"date": "2024-01", "value": 1.75},
                    {"date": "2025-01", "value": 0.0},
                ]
            }
        ]
    }


@pytest.fixture
def mock_snb_single_value_response():
    """Mock SNB response with single value."""
    return {
        "timeseries": [
            {
                "header": [{"dim": "Overview", "dimItem": "Switzerland - SNB policy rate"}],
                "metadata": {"key": "EPB@SNB.snboffzisa{LZ}", "frequency": "P1M", "scale": "", "unit": "In percent"},
                "values": [
                    {"date": "2025-01", "value": 0.0},
                ]
            }
        ]
    }