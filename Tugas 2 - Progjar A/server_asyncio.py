#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_asyncio1.py
# Asynchronous I/O inside "asyncio" callback methods.

import asyncio, zen_utils

value = 0

class ZenServer(asyncio.Protocol):
    # ketika mulai nyambung/acceptednya apa
    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.data = b''
        print('Accepted connection from {}'.format(self.address))
        
    # ketika isinya sama, sehingga dia menunggu ketika terdapat/ ketemu ?
    def data_received(self, data):
        # self.data += data
        # # ketika isinya sama
        # if self.data.endswith(b'?'):
        #     # mengembalikan answer
        #     answer = zen_utils.get_answer(self.data)
        #     self.transport.write(answer)
        #     # lalu datanya dikosongkan lagi agar dapat menerima input
        #     self.data = b''
        global value
        data = data[3:]
        message = str(data, encoding="ascii")
        arr = message.split()
        if arr[0] == "ADD":
            value += int(arr[1])
        else:
            value -= int(arr[1])
        send_message = "Total = : " + str(value)
        len_send_message = b"%03d" % (len(send_message),)
        send_message = len_send_message + bytes(send_message, encoding="ascii")
        self.transport.write(send_message)

    # ketika koneksi putus
    def connection_lost(self, exc):
        if exc:
            print('Client {} error: {}'.format(self.address, exc))
        elif self.data:
            print('Client {} sent {} but then closed'
                  .format(self.address, self.data))
        else:
            print('Client {} closed socket'.format(self.address))

if __name__ == '__main__':
    address = zen_utils.parse_command_line('asyncio server using callbacks')
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ZenServer, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
