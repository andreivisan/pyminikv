from gevent import socket
from gevent.pool import Pool
from gevent.server import StreamServer

from collections import namedtuple
from io import BytesIO
from socket import error as socket_error


"""
CONSTANTS
"""
ERR_BAD_REQUEST = "Bad Request"


# use exception to notify the connection-handling loop of problems
class CommandError(Exception): pass
class Disconnect(Exception): pass

Error = namedtuple('Error', ('message',))


class ProtocolHandler(object):
    def __init__(self):
        self.handlers = {
            '+': self.handle_simple_string,
            '-': self.handle_error,
            ':': self.handle_integer,
            '$': self.handle_string,
            '*': self.handle_array,
            '%': self.handle_dict
        }
        
    def handle_request(self, socket_file):
        # parse a request from the client into it's component parts
        first_byte = socket_file.read(1)
        if not first_byte:
            raise Disconnect()
        
        try:
            # delegate to the appropriate handler based on the first byte
            return self.handlers[first_byte](socket_file)
        except KeyError:
            raise CommandError(ERR_BAD_REQUEST)
        
    def handle_simple_string(self, socket_file):
        return socket_file.readline().rstrip('\r\n')
    
    def handle_error(self, socket_file):
        return Error(socket_file.readline().rstrip('\r\n'))
    
    def handle_integer(self, socket_file):
        return int(socket_file.readline().rstrip('\r\n'))
    
    def handle_string(self, socket_file):
        # first read the length ($<length>\r\n).
        length = int(socket_file.readline().rstrip('\r\n'))
        if length == -1:
            return None  # Special-case for NULLs.
        length += 2  # Include the trailing \r\n in count.
        return socket_file.read(length)[:-2]
    
    def handle_array(self, socket_file):
        num_elements = int(socket_file.readline().rstrip('\r\n'))
        # for each value in the array call handle_request to handle the appropriate value
        return [self.handle_request(socket_file) for _ in range(num_elements)]
    
    def handle_dict(self, socket_file):
        num_items = int(socket_file.readline().rstrip('\r\n'))
        elements = [self.handle_request(socket_file) for _ in range(num_items * 2)]
        return dict(zip(elements[::2], elements[1::2]))
    
    def write_response(self, socket_file, data):
        # serialize the response data and send it to the client
        pass
    
    
class Server(object):
    def __init__(self, host='127.0.0.1', port=31337, max_clients=64):
        self._pool = Pool(max_clients)
        self._server = StreamServer(
            (host, port),
            self.connection_handler,
            spawn=self._pool
        )
        
        self._protocol = ProtocolHandler()
        self.kv = {}
        
    def connection_handler(self, conn, addr):
        # convert "conn" (a socket object) into a file-like object
        socket_file = conn.makefile('rwb')
        
        # process client requests until client disconnects
        while True:
            try:
                data = self._protocol.handle_request(socket_file)
            except Disconnect:
                break
            
            try:
                resp = self.get_response(data)
            except CommandError as exc:
                resp = Error(exc.args[0])
                
            self._protocol.write_response(socket_file, resp)
            
        def get_response(self, data):
            # unpack the data sent by the client
            # execute the command they specified
            # pass back the return value
            pass
        
        def run(self):
            self._server._serve_forever()