import argparse, random, socket, zen_utils
import sys, random, multiprocessing

HOST = "127.0.0.1"
PORT = 1060
NUMJOBS = 6

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

# terdapat 3 argumen, yaitu adreess, nomor data, dan isi datanya
def worker(address, i, data):
    # membuat socket dan dikonek kan
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    message = ""
    # untuk setiap i di data akan di strip untuk menghilangkan newline pada kanan text
    for ii in data:
        ii = ii.strip()
        # panjang pesan , menggunakan metode pada tugas 1, sehingga nanti yang akan dikirimkan berupa len nya terlebih dahulu baru isi
        len_msg = b"%03d" % (len(ii),) 
        msg = len_msg + bytes(ii, encoding="ascii")
        sock.sendall(msg)
        len_msg = recvall(sock, 3)
        message = recvall(sock, int(len_msg))
        message = str(message, encoding="ascii")
    print('Klien: ',i, '->',message)
    sock.close()

if __name__ == '__main__':
    f = open("input.txt")
    data = f.readlines()
    f.close()

    address = (HOST, PORT)
    jobs = []
    for i in range(NUMJOBS):
        # MULTIPROSESING, DIGUNAKAN UNTUK DAPAT MELAKUKAN BANYAK PROSES JALAN BERSAMAAN, 
        # argumennya berisi adress, i(noomor proses), dan datanya berupa hasil yang dibaca di input.txt
        p = multiprocessing.Process(target=worker, args=(address, i, data))
        # memasukkan p kedalam jobs, dan dijalankan
        jobs.append(p)
    print("JOBS:", len(jobs))

    # dijalankan semua dan langsung di join, maskutnya ketika melakukan start proses
    for p in jobs:
        p.start()
    # main thread akan menunggu ketika p join terlebih dahulu, jika tidak maka p nya akan error
    for p in jobs:
        p.join()

# vim:sw=4:ai
