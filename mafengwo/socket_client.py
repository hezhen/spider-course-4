import socket
import sys

class SocketClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

        self.families = self.get_constants('AF_')
        self.types = self.get_constants('SOCK_')
        self.protocols = self.get_constants('IPPROTO_')

        # print( >>sys.stderr, 'Family  :', families[sock.family])
        # print( >>sys.stderr, 'Type    :', types[sock.type])
        # print( >>sys.stderr, 'Protocol:', protocols[sock.proto])
        # print( >>sys.stderr)
        
    def get_constants(self, prefix):
        """Create a dictionary mapping socket module constants to their names."""
        return dict( (getattr(socket, n), n)
                     for n in dir(socket)
                     if n.startswith(prefix)
                     )

    def send(self, message):
        try:
            # Create a TCP/IP socket
            print ("connecting to ", self.server_port)
            self.sock = socket.create_connection((self.server_ip, self.server_port))
            # Send data
            print( 'connected! client sends ', message)
            self.sock.sendall(message.encode('utf8'))

            data = self.sock.recv(1024)

            return data.decode('utf8')
        except Exception as err:
            print( 'Get Error Message: ', err ) #Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            return None
        finally:
            if hasattr(self, 'sock'):
                self.sock.close()