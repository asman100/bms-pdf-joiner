# Gunicorn configuration file for BMS PDF Joiner
# Save this as gunicorn.conf.py

import multiprocessing

# Server socket
bind = "0.0.0.0:8000"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"

# Timeout settings - increased for large file uploads
timeout = 300
keepalive = 5

# Request settings
limit_request_line = 0
limit_request_fields = 100
limit_request_field_size = 0

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "bms-pdf-joiner"

# Max requests per worker before restart
max_requests = 1000
max_requests_jitter = 50
