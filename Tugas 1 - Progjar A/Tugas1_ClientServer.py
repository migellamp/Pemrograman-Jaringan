#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter03/tcp_sixteen.py
# Simple TCP client and server that send and receive 16 octets

import argparse, socket
import sys
import glob
import pathlib
import os
import time

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(0)
    # print('Listening at', sock.getsockname())

    print('Waiting to accept a new connection')
    sc, sockname = sock.accept()
    print('We have accepted a connection from', sockname)
    while True:

        # print('Socket name:', sc.getsockname())
        # print('Socket peer:', sc.getpeername())
        # print('\n')
        #message = recvall(sc, 16)
        
        len_msg = recvall(sc, 3)
        message = recvall(sc, int(len_msg))
        first_text = message.decode()
        second_text = first_text.split()

        # print(second_text)


        # print('  Textnya :', repr(second_text))

        if second_text[0] == "ping":
            remove_ping = second_text[1:]
            join_now = ' '.join(remove_ping)
            # print('  Textnya :', repr(join_now))
            # print('  Message len:', repr(len(join_now)))

            # print('Output:')
            # print(repr(join_now))

            new_text = join_now.encode()
            sc.sendall(new_text)
            # print('\n')

        if second_text[0] == "ls":
            # path = "*.py"
            # for file in glob.glob(path, recursive=True):
            #     print(file)
            # if len(second_text) == 1:
            #     dest = '*.py'
            if len(second_text) == 1:
                dest = '*.py'

            if len(second_text) == 2:
                dest = second_text[1]
            # if second_text[1] != "":
            #     dest = second_text[1]
            list_file =  glob.glob(dest)
            space = ''
            for i in list_file:
                space += i + '\n'

            # print('Output:')
            # print(space)

            # print(second_text[0])
            len_space = b"%03d" % (len(space),)
            sc.sendall(len_space)
            new_space = space.encode()
            sc.sendall(new_space)
            # print('\n')

        if second_text[0] == "get":
            path_file = second_text[1]
            path=second_text[1]
            name_file = second_text[2]
            helper = "/"
            space = " "
            path_file=path_file+helper+name_file

            f=open(path_file,"rb")
            b=f.read()
            length = len(b)

            # print('Fetch:',path) 
            # print('size :',length)
            # print('lokal :',name_file)

            new_length = b"%03d" % (len(b),) 

            output = path.encode() + space.encode() + new_length + space.encode() + name_file.encode() 
            len_output = b"%03d" % (len(output.decode()),) 
            sc.sendall(len_output)
            sc.sendall(output) 
            # print('\n')

            
            # len_path = b"%03d" % (len(path),)
            # sc.sendall(len_path)
            # new_path = path.encode()
            # sc.sendall(new_path)

 

        if second_text[0] == "quit":
            print('Server shutdown...') 
            time.sleep(2)
            print('Client shutdown...') 
            sys.exit(0)


        # if second_text[0] == "error":
        #     a = "Masukkan perintah kembali.."
        #     print(a)
        #     print('\n')p
        #     err_msg = a.encode()
        #     sc.sendall(err_msg)
        #     print('\n')



        # if second_text[0] == "ls":
        #     print('ws_tcp2.py')
        # message = join_now.encode()
        
        
        # print('  Pesan Dari Client:', repr(message))
        # print('  Pesan Dari Client:', repr(new_text))
        
        # sc.close()
        # print('Reply sent, socket closed')

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    #sock.sendall(b'Hi there, server')
    #msg = b'Hi there, server'
    while True:


        print('Input Client :')
        input_ping = input("> ")
        first_split = input_ping.split()
        # line 48-54 =  setup text, and remove ping

        if first_split[0] == "ls":
            if len(first_split) == 1:
                msg = input_ping.encode()
                len_msg = b"%03d" % (len(msg),)
                msg = len_msg + msg
                sock.sendall(msg)
                len_recv = recvall(sock, 3)
                msg_recv = recvall(sock, int(len_recv))

                # print(len_recv)
                # print(msg_recv)
                replay = msg_recv.decode()
                print('Output pada Server:')
                print(replay)
                print('\n')

            if len(first_split) == 2:
                join_all = ' '.join(first_split)
                msg = join_all.encode()
                len_msg = b"%03d" % (len(msg),)
                msg = len_msg + msg
                sock.sendall(msg)
                len_recv = recvall(sock, 3)
                msg_recv = recvall(sock, int(len_recv))

                # print(len_recv)
                # print(msg_recv)
                replay = msg_recv.decode()
                print('Output pada Server:')
                print(replay)   
                print('\n')         


        # if input_ping == "ls *.py":
        #     msg = input_ping.encode()
        #     len_msg = b"%03d" % (len(msg),)
        #     msg = len_msg + msg
        #     sock.sendall(msg)
        #     len_recv = recvall(sock, 3)
        #     msg_recv = recvall(sock, int(len_recv))

        #     print(len_recv)
        #     print(msg_recv)
        #     replay = msg_recv.decode()
        #     print('Output pada Server:')
        #     print(replay)

        if first_split[0] == "ping":
            # remove_ping = first_split[1:]
            join_all = ' '.join(first_split)
            msg = join_all.encode()
            len_msg = b"%03d" % (len(msg),)
            msg = len_msg + msg
            sock.sendall(msg)
            reply = recvall(sock, len(msg)-8)
            replay = reply.decode()
            print('Output pada Server:')
            print(replay)
            print('\n')

        if first_split[0] == "get":
            join_all = ' '.join(first_split)
            msg = join_all.encode()
            len_msg = b"%03d" % (len(msg),)
            msg = len_msg + msg
            sock.sendall(msg)      

            len_recv = recvall(sock, 3)
            msg_recv = recvall(sock, int(len_recv))

            # print(len_recv)
            # print(msg_recv)
            replay = msg_recv.decode()
            replay_1=replay.split()
            print('Output pada Server:')
            print('Fetch:',replay_1[0]) 
            print('size :',replay_1[1])
            print('lokal :',replay_1[2])

            print('\n')

            # print('fetch:',replay_1[0],'size: ',replay_1[1],'lokal:',replay_1[2])
            # print('Fetch: ,size: , lokal:',replay_1[0],replay_1[1], repr(replay_1[2]))
            
            # print(replay_1)         


        if first_split[0] == "quit": 
            msg = input_ping.encode()
            len_msg = b"%03d" % (len(msg),)
            msg = len_msg + msg
            sock.sendall(msg)
            print('Server shutdown...') 
            time.sleep(2)
            print('Client shutdown...')
            sys.exit(0)

        # else:
        #     text = "error"
        #     a = "Masukkan perintah kembali.."
        #     msg = text.encode()
        #     len_msg = b"%03d" % (len(msg),)
        #     msg = len_msg + msg
        #     sock.sendall(msg)
        #     reply = recvall(sock, len(a))
        #     replay = reply.decode()
        #     print('Output pada Server:')
        #     print(replay)
        #     print('\n')


    # if first_split[0] == "ls":
    #     msg = input_ping.encode()
    #     sock.sendall(msg)

    # if first_split[0] == "ls":
    #     list_file =  glob.glob('/Semester_6/Pemrograman Jaringan/Tugas 1/*')
    #     sock.sendall(list_file)
    # elif first_split[0] == "ls":
    #     msg = input_ping.encode()
    #     sock.sendall(msg)

    # sock.close()

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
