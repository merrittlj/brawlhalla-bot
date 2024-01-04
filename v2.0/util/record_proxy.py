import socket
import logging_utils

def get_free_port():
    """
    Gets and returns a free port form the kernel's ip port range.
    """
    
    locate_port_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    locate_port_socket.bind(('', 0))
    free_port = locate_port_socket.getsockname()[1]
    locate_port_socket.close()

    return free_port

class TransparentProxy:
    def __init__(self, listen_host = "127.0.0.1", listen_port = get_free_port(), is_UDP = True):
        self._listen_host = listen_host
        self._listen_port = listen_port
        self._is_UDP = is_UDP

    def __str__(self):
        return f"Transparent Proxy: Listen host = {self._listen_host}, Listen port = {self._listen_port}, UDP/TCP = {'UDP' if self._is_UDP else 'TCP'}"

    def run(self):
        soc = socket.socket(socket.AF_INET, (socket.SOCK_DGRAM if self._is_UDP else socket.SOCK_STREAM))
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind((self._listen_host, self._listen_port))
        soc.listen()

        connection, address = soc.accept()  # Block execution until connection is received.
        logging_utils.logpr(f"Connected to by address: {address}")
        while True:  # Data reception loop.
            data = connection.recv(1024)
            if not data:  # Client has stopped sending data.
                break

            logging_utils.logpr(f"Received data:\n\n==========\n\n{data}\n\n==========\n")
            logging_utils.logpr("Sending received data back.")
            connection.sendall(data)
        connection.close()

        soc.close()
