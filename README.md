# File Malware Scanner Challenge

## Challenge Description
Create a containerized REST API using FastAPI that allows users to upload files and scan them for malware using VirusTotal's API.

## Technical Requirements

### Core Functionality
Create an API endpoint that:
- Accepts file uploads via POST request
- Submits the file to VirusTotal's scanning service
- Returns the scan results in a structured format

### Framework & Platform
- Use FastAPI for the API implementation
- Application must run in Docker
- Include necessary Docker configurations to run the service

### VirusTotal API Reference
Endpoint for file scanning:
```
https://www.virustotal.com/vtapi/v2/file/scan
```

Parameters:
- apikey: Your VirusTotal API key
- file: The file to be scanned

Example curl request:
```bash
curl --request POST \
  --url 'https://www.virustotal.com/vtapi/v2/file/scan' \
  --form 'apikey=<apikey>' \
  --form 'file=@/path/to/file'
```

## Requirements for Submission

1. Create a private GitHub repository containing:
   - Application code
   - Docker configuration
   - README.md with:
     - Docker build and run instructions
     - API documentation
     - Any assumptions made
2. Share access to your repository with: klahnen@gmail.com

### Docker Requirements
- Include all necessary Docker files to run the application
- The application should be runnable with simple Docker commands
- Document any required environment variables or configurations
- Ensure proper handling of file uploads within the container

## Time Limit
You have 2 hours to complete this challenge.

---
Notes: 
- You'll need to register for a free VirusTotal API key at https://www.virustotal.com/
- The solution should work by simply following your Docker instructions
- Consider security best practices when handling file uploads
