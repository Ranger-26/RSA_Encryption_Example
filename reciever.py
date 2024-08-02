import socket
import threading
from threading import Thread

#Server variables
HOST = '0.0.0.0'
PORT = 8089

#RSA info
p,q,e,d = 23,19,5,317
#p,q,e,d = 11,5,3,27



def decrypt(s:str):
    #return (ord(s) ** d) % (p*q)
    return sqr_mult(ord(s), d, p*q)

def sqr_mult(x, n, mod):
    if n == 0:
        return 1
    elif n%2 == 0:
        return sqr_mult(x*x % mod, n/2, mod)
    else:
        return x * sqr_mult(x*x % mod, (n-1)/2, mod) % mod

#create server socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))


#listen for an incomming connection
print('Socket bind complete')
server_socket.listen(10)
print('Socket now listening')

conn, addr = server_socket.accept()
print('Got connection!')

conn.send(("RSA Public Key: "+str(p*q)+","+str(e)).encode())



def socket_listen_thread():
    while True:
        message = conn.recv(1024).decode()
        print("Message from sender: "+message)
        encrypted_data = [ord(char) for char in message]
        print("Encrypted Data: "+str(encrypted_data))
        # decoded_message = ''
        # for char in message:
        #     cur_val = ord(char)
        #     print("Numerical value for "+char+": "+str(cur_val))
        #     new_val = (cur_val ** d) % (p*q)
        #     print("Translated value: "+str(new_val))
        #     print("New char: "+chr(new_val))
        #     decoded_message += chr(new_val)
        decrypt_data = [decrypt(char) for char in message]
        print("Decrypted Data: "+str(decrypt_data))
        print("Decoded message: "+str("".join([chr(val) for val in decrypt_data])))

t = threading.Thread(target=socket_listen_thread)
t.start()




    
