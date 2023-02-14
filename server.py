import socket
import threading
serverAddr=((socket.gethostname(),9999))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Server socket created")
BUFFER_SIZE = 1024

s.bind(serverAddr)

ips = {}


def handle_client():   
    while True:
        inp,cIp=s.recvfrom(1024)
        choice,msg = inp.decode().split(":")
        if choice == 'login':
            for ip in ips:
                s.sendto(bytes(f'[SERVER]: {msg} has joined the chat', 'utf-8'),ip) 
            ips[cIp] = msg
            print("Client connected: ",cIp)
            
            s.sendto(bytes(f'[SERVER]: Welcome to the chat {msg}!', 'utf-8'),cIp)
            continue
        elif choice == 'send':
            print(f'[{ips[cIp]}]:{msg}')
            #send msg to all clients in ips
            for ip in ips:
                if ip != cIp:
                    s.sendto(bytes(f'[{ips[cIp]}]:{msg}','utf-8'),ip)
                else:
                    s.sendto(bytes(f'[You]:{msg}','utf-8'),ip)
        elif choice == 'exit':
            print(ips)
            del ips[cIp]
            print(ips)
            for ip in ips:
                s.sendto(bytes(f'[SERVER]:{msg}','utf-8'),ip)
                        
def start():
    while(True):
        
        thread = threading.Thread(target = handle_client())
        thread.start()
        
start()
