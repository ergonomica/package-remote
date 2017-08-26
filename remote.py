#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os
import sys
from base64 import b64decode
import random
from ergonomica.lib.interface.prompt import prompt
import string
from ergonomica.lib.lang.environment import Environment

vowels = list('aeiou')

try:
    input = raw_input
except NameError:
    pass

def gen_word(min, max):
	word = ''
	syllables = min + int(random.random() * (max - min))
	for i in range(0, syllables):
		word += gen_syllable()
	
	return word.capitalize()


def gen_syllable():
	ran = random.random()
	if ran < 0.333:
		return word_part('v') + word_part('c')
	if ran < 0.666:
		return word_part('c') + word_part('v')
	return word_part('c') + word_part('v') + word_part('c')


def word_part(type):
	if type is 'c':
		return random.sample([ch for ch in list(string.lowercase) if ch not in vowels], 1)[0]
	if type is 'v':
		return random.sample(vowels, 1)[0]

def gen_valid_word():
    return gen_word(2,4)

def keygen():
    return os.urandom(16).decode("utf-8")

def sendmsg(ip, port, msg):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((ip, port))
    clientsocket.send(msg)

def connect(ip="0.0.0.0", port=2222):
    key = input("[ergo: remote]: Please enter a key: ")
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (ip, port)
    print >>sys.stderr, 'connecting to %s port %s' % ip
    sock.connect(ip)
    
    try:
    
        # Send data
        message = 'This is the message.  It will be repeated.'
        #print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
    
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print("Recv" + data)
            #print >>sys.stderr, 'received "%s"' % data

    finally:
        print("clsoin'")
        #print >>sys.stderr, 'closing socket'
        sock.close()
    
    
    sendmsg(ip, port, 'hello')
    
    # stdin = str(prompt(Environment(), {}))
    # for line in file_lines(stdin):
    #     sendmsg(line)
    
    # initialize ptk
    
    
def server(port=2222):
    print("[ergo: remote]: Starting an Ergonomica server locally on 0.0.0.0:{}...".format(str(port)))
    
    key = gen_valid_word() + " " + gen_valid_word() + " " + gen_valid_word()    
    print("[ergo: remote]: Key is {}.".format(key))
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', port)
    sock.bind(server_address)
    
    sock.listen(1)
    while True:
        # Wait for a connection
        print("[ergo: remote]: Waiting for a connection...")
        connection, client_address = sock.accept()
        try:
            print("[ergo: remote]: Connection from {}.".format(client_address))

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(1024)
                print("[ergo: remote]:<{}> {}".format(client_address, data))
                if data:
                    #print >>sys.stderr, 'sending data back to the client'
                    connection.sendall(data)
                else:
                    print("No more data from client!")
                    break
            
        finally:
            # Clean up the connection
            connection.close()


#server()   
connect("0.0.0.0")