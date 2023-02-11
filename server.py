from gevent import socket
from gevent.pool import Pool
from gevent.server import StreamServer

from collections import namedtuple
from io import BytesIO
from socket import error as socket_error


# use exception to notify the connection-handling loop of problems
class CommandError(Exception): pass
class Disconnect(Exception): pass

Error = namedtuple('Error', ('message',))


class ProtocolHandler(object):
    def handle_request(self, socket_file):
        # parse a request from the client into it's component parts
        pass
    
    def write_response(self, socket_file, data):
        # serialize the response data and send it to the client
        pass
    
    
class Server(object):
    def __init__(self, host='127.0.0.1', port=31337, max_clients=64):
        pass