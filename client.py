import socket
import threading
import sys
from encryption import Encryption
from rsa import *
import binascii
import ast


def byte_to_binary(n):
    return ''.join(str((n & (1 << i)) and 1) for i in reversed(range(8)))


def bin_to_decimal(n):
    return n


def hex_to_binary(h):
    return ''.join(byte_to_binary(ord(b)) for b in binascii.unhexlify(h))


host = "localhost"
port = 8080

# Try to connect to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # receive server public key
    serv_pub_key_data = sock.recv(1024).decode().split(",")
    e = int(serv_pub_key_data[0])
    n = int(serv_pub_key_data[1])
    serv_pub_key = (e, n)


except:
    print("Could not make a connection to the server, Please make sure your server is running")
    input("Press enter to quit")
    sys.exit(0)


# Send data to server
while True:

    try:
        print("INPUT:")
        message = int(input("Please enter an binary number: "), 2)
        key = int(input("\nPlease enter an binary key: "), 2)

        cipherText = Encryption(key).encrypt(message)

        ce, cn = input(
            "\nEnter public key parameters:").split(" ")
        client_pub_key = (int(ce), int(cn))
        ce, cn = client_pub_key
        cpd, cpn = input(
            "\nEnter private key parameters:").split(" ")
        client_private_key = (int(cpd), int(cpn))
        cpd, cpn = client_private_key

        # digest
        digest = (hashing(str(message)).hexdigest())

        # Encrypted secret key
        sec_key = bin_to_decimal(key)

        encrypt_sec_key = rsa_encrypt(e, n, sec_key)
        print(f"\nEncrypted Secret key: {encrypt_sec_key}")
        print("\nCipher Text: " + str(cipherText))
        print(f"\nDigest: {digest}")

        int_digest = int(digest, 16)

        client_signature = rsa_encrypt(ce, cn, int_digest)
        print(f"\nDigital signature {client_signature}\n")

        # passing data to server
        data = str(cipherText)+"|" + str(encrypt_sec_key)+"|" + \
            str(client_signature)+"|"+str(ce)+"|"+str(cn)
        sock.send(bytes(data, 'utf-8'))

    except ValueError:
        print("Please enter binary value only")
