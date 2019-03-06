# config file
# https://sanic.readthedocs.io/en/latest/sanic/config.html
"""
  Builtin Configuration Values
| Variable                  | Default   | Description                                               |
| ------------------------- | --------- | --------------------------------------------------------- |
| REQUEST_MAX_SIZE          | 100000000 | How big a request may be (bytes)                          |
| REQUEST_BUFFER_QUEUE_SIZE | 100       | Request streaming buffer queue size                       |
| REQUEST_TIMEOUT           | 60        | How long a request can take to arrive (sec)               |
| RESPONSE_TIMEOUT          | 60        | How long a response can take to process (sec)             |
| KEEP_ALIVE                | True      | Disables keep-alive when False                            |
| KEEP_ALIVE_TIMEOUT        | 5         | How long to hold a TCP connection open (sec)              |
| GRACEFUL_SHUTDOWN_TIMEOUT | 15.0      | How long to wait to force close non-idle connection (sec) |
| ACCESS_LOG                | True      | Disable or enable access log                              |
"""
REQUEST_MAX_SIZE = 100000000
REQUEST_BUFFER_QUEUE_SIZE = 100
REQUEST_TIMEOUT = 60
RESPONSE_TIMEOUT = 60
KEEP_ALIVE = True
KEEP_ALIVE_TIMEOUT = 5
GRACEFUL_SHUTDOWN_TIMEOUT = 15.0
ACCESS_LOG = True

"""
Server Config
"""
HOST = "127.0.0.1"
PORT = 8080
WORKER = 2

"""
Database Config
"""
DB_HOST = "127.0.0.1"
DB_PORT = 6379

"""
API Config
"""
API_VERSION = "1.0.0"
API_TITLE = "Session API"
API_DESCRIPTION = "Module"
API_TERMS_OF_SERVICE = "OuO"  # link to ToS page
API_PRODUCES_CONTENT_TYPES = ["application/json"]
API_CONTACT_EMAIL = "wtf"  # mailto:
