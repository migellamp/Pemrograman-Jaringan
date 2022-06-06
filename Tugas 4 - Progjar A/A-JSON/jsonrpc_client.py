# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter18/jsonrpc_client.py
# JSON-RPC client needing "pip install jsonrpclib-pelix"

from fileinput import close
from jsonrpclib import Server
import sys
import glob
import pathlib
import os
import time

def main():
    while True:
        proxy = Server('http://localhost:7002')
        print('Input Client :')
        input_ping = input("> ")
        first_split = input_ping.split()
        # print(proxy.lengths(input_ping))

        if first_split[0] == "get":
            # print(proxy.lengths(input_ping))
            replay = proxy.lengths(input_ping)
            replay_1=replay.split()
            print('Output pada Server:')
            print('Fetch:',replay_1[0]) 
            print('size :',replay_1[1])
            print('lokal :',replay_1[2])

        if first_split[0] == "ls":
            if len(first_split) == 1:
                print(proxy.lengths(input_ping))

            if len(first_split) == 2:
                print(proxy.lengths(input_ping))

        if first_split[0] == "ping":
            print(proxy.lengths(input_ping))

        if first_split[0] == "count":
            print('Banyaknya File :', proxy.lengths(input_ping))

if __name__ == '__main__':
    main()
