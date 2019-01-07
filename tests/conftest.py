from pathlib import Path

import pytest


TEST_DIR = Path(__file__).parent


@pytest.fixture
def organization_details_response():
    filepath = TEST_DIR / 'data' / 'organization-details-response.json'
    return filepath.read_bytes()


@pytest.fixture
def deleted_organization_details_response():
    filepath = TEST_DIR / 'data' / 'deleted-organization-details-response.json'
    return filepath.read_bytes()
