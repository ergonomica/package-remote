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

def file_lines(stdin):
    split_lines = []
    for line in stdin.split("\n"):
        if line.startswith("#"):
            pass
        elif line.startswith(" "):
            split_lines[-1] += line
        else:
            split_lines.append(line)
    return split_lines
        

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
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (ip, port)
    sock.connect((ip, port))
    
    recv = ""
    
    try:
        sock.sendall(msg)
        recv = sock.recv(1000)
            
    finally:
        sock.close()
    
    return recv


def connect(ip="0.0.0.0", port=2222):
    key = input("[ergo: remote]: Please enter a key: ")
        
    Env = Environment()
    Env.prompt = "({}).: ".format(ip)
    while True:
        stdin = str(prompt(Env, {}))
        for line in file_lines(stdin):
            print(sendmsg(ip, port, key + line))

    
def server(port=2222):
    from ergonomica.ergo import ergo_to_string
    
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
                data = connection.recv(8192)
                if data:
                    if data.startswith(key):
                        data = data[len(key):]
                        print("[ergo: remote]:<{}> {}".format(client_address, data))
                        connection.sendall(str(ergo_to_string(data)))
                    else:
                        print("[ergo: remote]: UNAUTHENTICATED CLIENT.")
                else:
                    print("No more data from client!")
                    break
            
        finally:
            # Clean up the connection
            connection.close()

exports = {'connect': connect,
           'server': server}