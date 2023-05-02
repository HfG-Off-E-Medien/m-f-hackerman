import socket
from tqdm import tqdm
from pipeline import Pipeline
from tcp_funcs import send_file

IP = "10.1.30.133"#socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
PW_SIZE = 16
PW = "heiligespasswort"
BUFFER_SIZE = 1024
FORMAT = "utf-8"
FILENAME = "/home/ki-lab-02/Desktop/Studentische-Projekte/Moritz/SERVER/empfangen.jpg"


def main():
    print("Setting up tensorflow pipeline...")
    P = Pipeline()
    #P.warump()
    
    print("[STARTING] Server is starting.")
    """ Staring a TCP socket. """
    print(IP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)

    """ Server is listening, i.e., server is now waiting for the client to connect. """
    server.listen()

    while True:
        print("[LISTENING] Server is listening.")

        """ Server has accepted the connection from the client. """
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

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
        
        """ Process image """
        P.run(FILENAME, "processed.jpg")

        """ Send image back """
        send_file(conn, FILENAME, BUFFER_SIZE)

        conn.close()

if __name__ == "__main__":
    main()