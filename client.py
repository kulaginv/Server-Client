import socket

class ClientError(Exception):
    pass

class Client:

    def __init__(self, addr, port, timeout = None):
        self.addr = addr
        self.port = int(port)
        self.timeout = int(timeout)
        try:
            self.sock = socket.create_connection((self.addr, self.port), timeout)
        except socket.error as err:
            raise ClientError("init error", err)

    def soed (self):
        text = b''
        while not text.endswith(b"\n\n"):
            try:
                text += self.sock.recv(1024)
            except socket.error as err:
                raise ClientError(err)
        text_str = text.decode()
        stat, dann = text_str.split('\n', 1)
        if stat == 'error':
            raise ClientError("soed error", dann)
        return dann 
                
    def put(self, key, val, timestamp = None):
        timestamp = timestamp or int(time.time())
        try:
            self.sock.sendall(f"put {key} {val} {timestamp}\n".encode())
        except socket.error as err:
            raise ClientError("put error", err)

    def get(self, key):
        try:
            self.sock.sendall(f"get {key}\n".encode())
        except socket.error as err:
            raise ClientError("get error", err)
        dann = self.soed()
        slov = {}
        for line in dann.split('\n'):
            key, val, tms = line.split()
            if key not in slov:
                slov[key] = []
            slov[key].append((int(tms), float(val)))
            slov[key].sort(key = lambda time: time[0])
        return slov
        
        
        
        
        
