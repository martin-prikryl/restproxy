LOGGER_NAME = 'log'
VIP_DB_API = 'http://localhost:8088/v1/coords/'

# following request parameters must be optimized according to
# expected load and desired success response rate
# REQUEST_TIMEOUT - number of seconds after which
#                   backend DB request will time out
# REQUEST_THREADS - number of backend DB requests executed
#                   in parallel (for one API request)
REQUEST_TIMEOUT = 1
REQUEST_THREADS = 1
