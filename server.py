import asyncio

class Metric:
    metric = dict()

class Server(asyncio.Protocol):

    global metric
    metric = Metric.metric

    def __init__(self):
        self.transport = None
    
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        wrd = data.decode()[:-1].split(' ')
        command = wrd[0]
        inp = wrd[1:]
        if  command == 'get':
            rep = self.c_get(inp)
        elif command == 'put':
            rep = self.c_put(inp)
        else:
            rep = 'error\nwrong command\n\n'
        self.transport.write(rep.encode())
        
    @staticmethod
    def c_put(inp):
        if len(inp) != 3:
            return 'error\nwrong command\n\n'
        key = inp[0]
        try:
            timestamp, val = int(inp[2]), float(inp[1])
        except ValueError:
            return 'error\nwrong command\n\n'
        timestamp = str(timestamp)
        val = str(val)
        if key not in metric:
            metric[key] = []
        if (timestamp, val) not in metric[key]:
            for i in range(len(metric[key])):
                        if timestamp in metric[key][i]:
                            del metric[key][i]
            metric[key].append((timestamp, val))
            metric[key].sort(key = lambda time: time[0])
        return 'ok\n\n'
    
    @staticmethod
    def c_get(inp):
        if len(inp) != 1:
            return 'error\nwrong command\n\n'
        key = inp[0]
        rep = 'ok\n'
        if key == '*':
            for key, vals in metric.items():
                for val in vals:
                    rep = rep + key + ' ' + val[1] + ' ' + val[0] + '\n'
        else:
            if key in metric:
                for val in metric[key]:
                    rep = rep + key + ' ' + val[1] + ' ' + val[0] + '\n'
        return rep + '\n'

def run_server(host = '127.0.0.1', port = 8888):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(Server, host, int(port))
    print('server started at {} {}'.format(host, port))
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
        
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

run_server('127.0.0.1', 8888)

