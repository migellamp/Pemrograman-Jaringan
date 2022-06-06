#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter18/rpyc_client.py
# RPyC client

import rpyc
import time
import sys

def main():
    while True:
        config = {'allow_public_attrs': True}
        proxy = rpyc.connect('localhost', 18861, config=config)
        print("Input Client: ")
        input_msg = input("> ")
        first_split = input_msg.split()
        
        if first_split[0] == "ping":
            print(proxy.root.exeCommand(input_msg))

        elif first_split[0] == "ls":
            if len(first_split) == 1:
                print(proxy.root.exeCommand(input_msg))
            # print(proxy.root.exeCommand(input_msg))
            else :
                print(proxy.root.exeCommand(input_msg))

        elif first_split[0] == "count":
            print(proxy.root.exeCommand(input_msg))

        elif first_split[0] == "get":
            print(proxy.root.exeCommand(input_msg))

        elif first_split[0] == "quit":
            proxy.root.exeCommand(input_msg)
            # time.sleep(1)
            # print("client shutdown...")
            sys.exit(0)


        # fileobj = open('testfile.txt')
        # linecount = proxy.root.line_counter(fileobj, noisy)
        # print('The number of lines in the file was', linecount)

# def noisy(string):
#     print('Noisy:', repr(string))

if __name__ == '__main__':
    main()