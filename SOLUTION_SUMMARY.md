# Fix for 413 Request Entity Too Large

## Problem
Users were experiencing "413 Request Entity Too Large" errors when uploading PDF files, indicating that the file size exceeded server limits.

## Root Cause
While Flask had a `MAX_CONTENT_LENGTH` of 500 MB configured, several issues could cause 413 errors:
1. No client-side validation to prevent large uploads before they start
2. No user-friendly error page when 413 errors occur
3. Missing deployment configuration for production web servers (nginx, gunicorn)
4. Lack of documentation on file size limits and deployment best practices

## Solution Implemented

### 1. Client-Side Validation (templates/index.html)
- Added JavaScript file size validation before upload
  - Maximum single file size: 400 MB
  - Maximum total upload size: 450 MB
- Display file sizes in human-readable format (KB, MB, GB)
- Show immediate feedback if files are too large
- Prevent form submission if total size exceeds limit

### 2. Server-Side Error Handling (app.py)
- Added custom error handler for 413 status code
- Created styled error page with:
  - Clear explanation of the problem
  - Current size limit (500 MB)
  - Helpful suggestions for resolution
  - Easy navigation back to the main page

### 3. Production Deployment Configuration
- **gunicorn.conf.py**: Production-ready Gunicorn configuration
  - Timeout: 300 seconds (for large file processing)
  - Workers: CPU count * 2 + 1
  - No request size limits at Gunicorn level
  
- **nginx.conf.example**: Nginx reverse proxy configuration
  - `client_max_body_size 500M`
  - Increased timeouts for large uploads
  - Disabled request buffering for efficiency
  - Proper proxy headers

### 4. Documentation Updates (README.md)
- Added "File Size Limits" section
- Added "Production Deployment" section with:
  - Gunicorn setup instructions
  - Nginx configuration guide
  - Troubleshooting steps for 413 errors
- Added "System Requirements" section

### 5. Dependencies (requirements.txt)
- Added gunicorn>=20.1.0 for production deployments

## Testing
All changes have been tested:
- ✓ Flask configuration verified (MAX_CONTENT_LENGTH = 500 MB)
- ✓ 413 error handler tested and working
- ✓ Client-side validation logic verified
- ✓ Deployment configuration files validated
- ✓ Documentation completeness checked

## Benefits
1. **Better User Experience**: Users get immediate feedback on file sizes
2. **Prevents Wasted Time**: Validation happens before upload starts
3. **Clear Error Messages**: Users know exactly what to do if files are too large
4. **Production Ready**: Includes all necessary configuration for deployment
5. **Well Documented**: Clear instructions for setup and troubleshooting

## Files Changed
- `templates/index.html`: Added client-side validation
- `app.py`: Added 413 error handler
- `requirements.txt`: Added gunicorn dependency
- `README.md`: Added comprehensive documentation
- `gunicorn.conf.py`: Created production server configuration
- `nginx.conf.example`: Created reverse proxy configuration

## Usage
### Development
```bash
python app.py
```

### Production
```bash
gunicorn -c gunicorn.conf.py app:app
```

With nginx as reverse proxy (see nginx.conf.example for configuration).
