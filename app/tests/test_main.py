import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status
import io

from app.main import app

# Mark all tests in this module as asyncio tests
pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def async_client():
    """
    Creates an async test client for making requests to th e app.
    This is the equivalent of 'self.client' in Django
    """
    # 'AsyncClient from httpx is used to make async requests to our app
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
        
async def test_scan_file(async_client, monkeypatch):
    """
    Test the /scan endpoint for a successful file upload
    
    We will 'mock' the 'scan_file' service to return a successful response without actually calling the API
    
    Args:
        async_client: The test client fixture
        monkeypatch: Pytest fixture for mocking objects/functions
    """
    
    # Define the mock response we want our service to return
    mock_success_response = {
        "scan_id": "test_scan_id_123",
        "resource": "test_resource_456",
        "response_code": 1,
        "verbose_msg": "Scan request successfully queued",
        "permalink": "http://example.com/scan/123"
    }
    
    # Define an async mock function
    async def mock_scan_service(*args, **kwargs):
        return mock_success_response
    
    # Apply the mock 
    monkeypatch.setattr('app.main.scan_file', mock_scan_service)
    
    # Prepare a dummy file for upload
    dummy_file_content = b"This is a test file"
    dummy_file = io.BytesIO(dummy_file_content)
    
    # Make the POST request to our app's /scan endpoint
    response = await async_client.post(
        "/scan",
        files={"file": ("test_file.txt", dummy_file, "text/plain")},
    )
    
    # Assert the results
    assert response.status_code == status.HTTP_200_OK
    
    # Check if the response body matches our mock response
    response_data = response.json()
    assert response_data['scan_id'] == mock_success_response['scan_id']
    assert response_data['verbose_msg'] == mock_success_response['verbose_msg']

async def test_scan_file_service_unavailable(async_client, monkeypatch):
    """
    Test the /scan endpoint when the VirusTotal service is unavailable
    """
    
    # Define a mock function that simulates a failure
    async def mock_scan_service_failure(*args, **kwargs):
        # We simulate teh service raising the exception we expect
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="VirusTotal service is unavailable"
        )
    
    # Apply the mock
    monkeypatch.setattr('app.main.scan_file', mock_scan_service_failure)
    
    # Prepare a dummy file for upload
    dummy_file = io.BytesIO(b"This is a test file")
    
    # Make the POST request to our app's /scan endpoint
    response = await async_client.post(
        "/scan",
        files={"file": ("test2_file.txt", dummy_file, "text/plain")},
    )
    
    # Assert the results
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    response_data = response.json()
    assert "VirusTotal service is unavailable" in response_data['detail']