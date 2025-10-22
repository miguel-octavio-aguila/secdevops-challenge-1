# Solution: Malware Scanner API (SecDevOps Challenge)

This is a containerized REST API, built with FastAPI, that allows users to upload files to be scanned for malware using the VirusTotal v2 API.

## Technical Features

* **Framework**: FastAPI (Asynchronous)
* **HTTP Client**: `httpx` for non-blocking, asynchronous API calls.
* **Platform**: Fully containerized with Docker.
* **Configuration**: Manages API keys by copying a local `.env` file into the image at build time.
* **Testing**: Includes a unit test suite using `pytest` and `monkeypatch`.

---

## Docker Build & Run Instructions

The challenge requires the application to be runnable with simple Docker commands.

docker build -t malware-scanner .

docker run -d -p 8000:8000 --env-file ./.env --name scanner-api malware-scanner-api

### Prerequisites

* Docker Desktop (or Docker Engine) installed and running.
* A valid VirusTotal API Key.

### 1. Prepare the Configuration File (`.env`)

In the root of this project, create a file named `.env`. Add your API key to it **without any quotes**.

**File: `.env`**
```env
# Environment variables file
VIRUSTOTAL_API_KEY=yourApiKeyGoesHereWithoutQuotes12345

# API Documentation

Interactive documentation (Swagger UI) is automatically available once the container is running.

**Documentation URL:** http://localhost:8000/docs

## Endpoints

### `GET /`

* **Description:** Root endpoint for a simple health check.
* **Success Response (200 OK):**

```json
{
  "status": "ok",
  "message": "Welcome to the File Malware Scanner API"
}
```

### `POST /scan`

* **Description:** Accepts a file upload (`multipart/form-data`) and submits it to VirusTotal for scanning.
* **Request Body:**
  * `file`: (Required) The binary file to be scanned.
* **Example `curl`:**

```bash
curl -X 'POST' \
  'http://localhost:8000/scan' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/file.txt'
```

* **Success Response (200 OK):**

```json
{
  "scan_id": "a1b2c3d4...",
  "resource": "f1e2d3c4...",
  "response_code": 1,
  "verbose_msg": "Scan request successfully queued, come back later for the report",
  "permalink": "https://www.virustotal.com/gui/file/f1e2d3c4..."
}
```

* **Error Response (e.g., 403 Forbidden):**

```json
{
  "detail": "VirusTotal API error: Client error '403' for url '...'"
}
```

## Assumptions and Design Decisions

During development, the following decisions and assumptions were made to achieve a functional solution:

1. **API Key Handling:** The API key is loaded from the `.env` file at build time. This is secure and aligns with best practices for containerized applications.

2. **API Submission Method:** Following the challenge's `curl` example, the `apikey` is sent as part of the `form-data` (`data=...`), not as a URL parameter (`params=...`). This was critical for resolving the `403 Forbidden` error.

3. **Asynchronous Client (`httpx`):** The `requests` library was replaced with `httpx`. This respects FastAPI's async nature, prevents blocking the server on external API calls, and helped resolve network issues.

4. **IPv4 Network Patch:** A patch was applied to the `socket` library in `app/main.py` to force IPv4. This resolved persistent network connectivity issues (`503 Service Unavailable`) that occurred only inside the Docker environment.

5. **Permalink Fix:** The VirusTotal v2 API returns an outdated `permalink` field. The API response is modified to build the correct, modern GUI URL (`/gui/file/...`) using the `resource` hash.

6. **Scope:** The API is responsible only for submitting the file for a scan. It does not implement logic to poll for the final scan report, as that is an asynchronous process on VirusTotal's side.
