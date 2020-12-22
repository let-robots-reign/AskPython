"""
WSGI config for AskPython project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from urllib.parse import parse_qs
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AskPython.settings')

application = get_wsgi_application()

# curl -i -X GET "http://localhost:8081?a=1&str=python"
# curl -i -X POST -H 'Content-Type: application/json' -d '{"a": 1, "str": "python"}' http://localhost:8081/

HELLO_WORLD = b"Hello world!\n"


def simple_app(environ, start_response):
    # GET
    query = parse_qs(environ['QUERY_STRING'])
    get_parameters = b'GET: ' + json.dumps(query).encode('utf-8') if query else b''
    # POST
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    post_parameters = b'POST: ' + request_body if request_body else b''

    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD, get_parameters, post_parameters]
