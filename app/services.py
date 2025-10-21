import httpx
from fastapi import UploadFile, HTTPException, status
import io

from .config import settings # Import our settings instance

# VirusTotal API endpoint configuration
VIRUSTOTAL_SCAN_URL = "https://www.virustotal.com/vtapi/v2/file/scan"

async def scan_file(file: UploadFile) -> dict:
    """
    Submits a file to the VirusTotal API for scanning.

    This function reads the file content un memory, prepares the request parameters
    and files, and sends it to the VirusTotal API.
    
    Args:
        file (UploadFile): The file to be scanned.
        
    Returns:
        dict: The JSON response from the VirusTotal API.
        
    Raises:
        HTTPException: If the file upload or API request fails.
            - 503 SERVICE UNAVAILABLE: If the VirusTotal API call fails.
            - 400 BAD REQUEST: If VirusTotal returns an error (e.g., bad API key).
    """
    try:
        # Read the file's content into memory
        file_content = await file.read()
        
        # Prepare the request parameters
        data = {
            "apikey": settings.VIRUSTOTAL_API_KEY,
        }
        
        # Prepare the file for the multipart/form-data request
        files = {
            "file": (file.filename, io.BytesIO(file_content), file.content_type),
        }
        
        # Use httpx.AsyncClient to make an asynchronous POST request
        # Esto no bloqueará el servidor, es la forma correcta en FastAPI
        async with httpx.AsyncClient() as client:
            response = await client.post(
                VIRUSTOTAL_SCAN_URL,
                files=files,
                data=data
            )
        
        # Raise an HTTPError for bad responses
        response.raise_for_status()
        
        # Parse the JSON response
        json_response = response.json()
        
        # VirusTotal API returns a 'response_code'
        # 0 usually means an error, 1 means success.
        if json_response.get('response_code') == 1:
            # The v2 API 'permalink' field is not a real URL.
            # We will build the correct GUI URL using the 'resource' hash.
            resource_hash = json_response.get('resource')
            if resource_hash:
                json_response['permalink'] = f"https://www.virustotal.com/gui/file/{resource_hash}"
            return json_response
        else:
            # If the response_code is not 1, it's an error
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"VirusTotal API error: {json_response.get('verbose_msg', 'Unknown error')}"
            )
    
    except httpx.RequestError as e:
        # Handle network errors or non-200 responses
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"VirusTotal API request failed: {str(e)}"
        )

    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )