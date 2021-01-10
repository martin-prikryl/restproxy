# restproxy
Simple implementation of REST API using another REST API in the backend

* Start by 'py main.py' when backend DB API is running.
* REQUEST_TIMEOUT and REQUEST_THREADS in config.py must be optimized according to:
  * backend DB reliability and allowed load
  * expected API load
  * desired API response time and success response rate
