import socket
import threading
from encryption import Encryption
from decryption import Decryption
from rsa import *
import binascii
import ast


class Client():
    def __init__(self, socket):
        self.socket = socket

    # Receive key and cipher text from server and decrypt cipher-text to generate plain-text
    def start(self):
        print("\nClient Successfuly connected\n")
        while True:
            try:
                print("\nInput\n")
                e, n = input(
                    "Enter public key parameters(with space in between):").split(" ")
                spe, spn = input(
                    "Enter private key parameters(with space in between):").split(" ")
                serv_public_key = e+","+n

                server_public_key = (int(e), int(n))
                server_private_key = (int(spe), int(spn))
                e, n = server_public_key
                spe, spn = server_private_key

                self.socket.send(bytes(serv_public_key, 'utf-8'))

                data = self.socket.recv(1024)

            except:
                print("\nClient is disconnected\n")
                exit()
                break
            if data != "":
                data_arr = data.decode("utf-8").split("|")
                cipherText = data_arr[0]
                encrypt_sec_key = int(data_arr[1])
                client_signature = int(data_arr[2])
                ce = int(data_arr[3])
                cn = int(data_arr[4])

                decrypt_secret_key = rsa_decrypt(spe, spn, encrypt_sec_key)
                decrypt_secret_key_bin = bin(decrypt_secret_key).split('b')[-1]
                print(f"\nDecrypted Secret Key: { decrypt_secret_key_bin }")

                plaintext = Decryption(decrypt_secret_key).decrypt(
                    int(cipherText))
                plain = bin(plaintext)

                print("\nDecrypted Message: " + str(plain))

                # Hashing
                message = str(plaintext)
                digest = hashing(message).hexdigest()
                print(f"\nMessage Digest: {digest}")

                int_digest = int(digest, 16)
                signature = rsa_encrypt(ce, cn, int_digest)
                print(f"\nIntemediate verification code: {signature}")

                if signature == client_signature:
                    print("\nSignature Verified")
                else:
                    print("\nSignature Not Verified")


def main():
    # Get host and port
    host = "localhost"
    port = 8080

    # Create new server socket
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)

    print("Server started\n")

    while True:
        _socket, addr = sock.accept()
        Client(_socket).start()


main()
