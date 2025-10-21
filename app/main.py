import socket
_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = _getaddrinfo(*args, **kwargs)
    # Filter out non-IPv4 addresses
    return [res for res in responses if res[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse

from .models import ScanResult, ScanError
from .services import scan_file

# Create the FastAPI application instance
app = FastAPI(
    title='File Malware Scanner API',
    description="An API to scan files for malware using VirusTotal",
    version='1.0.0',
)

# Define a simple health check endpoint
@app.get("/")
async def read_root():
    """
    Root endpoint for health check
    """
    
    return {"status": "ok", "message": "Welcome to the File Malware Scanner API"}

# Define the file scanning endpoint
@app.post(
    "/scan",
    response_model=ScanResult,
    responses={
        400: {"model": ScanError, "description": "Bad Request or VirusTotal API Error"},
        503: {"model": ScanError, "description": "Service Unavailable - VirusTotal API is down"},
        500: {"model": ScanError, "description": "Internal Server Error"},
    }
)
async def create_upload_file(
    file: UploadFile = File(..., description='The file to be scanned')
):
    """
    Accepts a file upload and submits it to VirusTotal for scanning
    
    Return:
        The scan result from VirtualTotal in a structured format
    """
    
    # We delegate all the hard work to our 'services' module.
    # This keeps our endpoint clean and follows Separation of Concerns.
    # The endpoint's only job is to handle HTTP details.
    try:
        scan_result = await scan_file(file)
        
        # If successful, we return the dictionary
        return scan_result
    
    except HTTPException as he:
        # If our service raised a controlled HTTPException, re-raise it
        # FastAPI will handle it and return the appropriate response
        raise he

    except Exception as he:
        # Catch any other unexpected error
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"An unexpected error occurred: {str(he)}"},
        )