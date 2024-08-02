import socket
import threading
from threading import Thread


#connect to server
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8089))

#rsa public key (p*q, e)
rsa_public_key = [-1,-1]

def socket_listen_thread():
    while True:
        data = clientsocket.recv(1024)
        str_data = data.decode()
        parts = str_data.split(":")[1].strip().split(",")
        rsa_public_key[0] = int(parts[0])
        rsa_public_key[1] = int(parts[1])
        print("Setting RSA public key: "+str(rsa_public_key))
        print("Message from reciever: "+str_data)
        



def keyboard_listen_thread():
    text: str = ""
    while text != "q":
        text = input("Enter a message you want to send: ")
        send_message(text.upper())

def encrypt(s:str):
    return (ord(s) ** rsa_public_key[1]) % rsa_public_key[0]

def send_message(message: str):
    print("Sending Message: "+message)
    encrypted_message = ''
    encrypted_data = [encrypt(char) for char in message]
    # for char in message:
    #     cur_val = ord(char)
    #     print("Numerical value for "+char+": "+str(cur_val))
    #     new_val = (cur_val ** rsa_public_key[1]) % rsa_public_key[0]
    #     print("Translated value: "+str(new_val))
    #     print("New char: "+chr(new_val))
    #     encrypted_message += chr(new_val)
    print("Message Data: "+str([ord(char) for char in message]))
    print("Encrypted Data: "+str(encrypted_data))
    #print('Encrypted message! '+str("".join([chr(val) for val in encrypted_data])))
    clientsocket.send(str("".join([chr(val) for val in encrypted_data])).encode())

t = threading.Thread(target=keyboard_listen_thread)
t.start()

socket_listen_thread()