import argparse
import socket
import sys
import select

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-c", "--client", type=str)
group.add_argument("-s", "--server", action="store_true")
args = parser.parse_args()
port = args.server

def chat(socket):
	readable = [0, socket]
	while True:
		r, writeable, exceptionable = select.select(readable, [], [])
		for obj in r:
			if obj==0:
				socket.send(sys.stdin.readline())
			else:
				data = socket.recv(1024)
				if data:
					print data,

if args.client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((args.client, 9999))
	chat(sock)

elif args.server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(("", 9999))
	sock.listen(5)
	conn, addr = sock.accept()
	chat(conn)
					
				



