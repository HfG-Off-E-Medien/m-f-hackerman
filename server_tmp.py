import socket
from tqdm import tqdm

IP = "127.0.0.1"#socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
PW_SIZE = 16
PW = "heiligespasswort"
BUFFER_SIZE = 1024
FORMAT = "utf-8"
FILENAME = "/home/pi/Desktop/moritz_filter/empfangen.jpg"


def main():
    print("[STARTING] Server is starting.")
    """ Staring a TCP socket. """
    print(IP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)

    """ Server is listening, i.e., server is now waiting for the client to connected. """
    server.listen()

    while True:
        print("[LISTENING] Server is listening.")
        
        """ Server has accepted the connection from the client. """
        conn, addr = server.accept()
        #print(f"[NEW CONNECTION] {addr} connected.")

        conn.send("Authentificate yourself.".encode(FORMAT))
        PW_SENT = conn.recv(PW_SIZE).decode(FORMAT)
        
        if PW_SENT != PW:
            conn.send("Bye!!".encode(FORMAT))
            conn.close()
        else:
            print("Client is cool! Let em in.")
            conn.send("Hello".encode(FORMAT))
        
        """ Receive filesize from the client """
        filesize = int(conn.recv(BUFFER_SIZE).decode())
        print(filesize)
        
        """ Receive buffers """
        progress = tqdm(range(filesize), f"Receiving {FILENAME}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(FILENAME, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = conn.recv(BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

        conn.close()
        

if __name__ == "__main__":
    main()