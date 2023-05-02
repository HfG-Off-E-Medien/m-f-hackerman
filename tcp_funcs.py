from os.path import getsize
from tqdm import tqdm

def send_file(server, BUFFER_SIZE, FILENAME):
    filesize = getsize(FILENAME)
    print("Sending file with following size: ", filesize)
    server.sendall(f"{filesize}".encode())
    progress = tqdm(range(0, filesize, BUFFER_SIZE), f"Sending...", unit="B", unit_scale=True, unit_divisor=BUFFER_SIZE)
    with open(FILENAME, "rb") as f:
        for i in progress:
            bytes_read = f.read(BUFFER_SIZE)
            server.sendall(bytes_read)
            progress.update(len(bytes_read))

def receive_file(conn, BUFFER_SIZE, OUT_PATH):
    """ Receive filesize from the client """
    filesize = int(conn.recv(BUFFER_SIZE).decode())
    print('File mit folgender Size angekuendigt: ', filesize)

    """ Receive buffers """
    progress = tqdm(range(0, filesize, BUFFER_SIZE), f"Receiving...", unit="B", unit_scale=True, unit_divisor=BUFFER_SIZE)
    with open(OUT_PATH, "wb") as f:
        for i in progress:
            bytes_read = conn.recv(BUFFER_SIZE)
            f.write(bytes_read)
            progress.update(len(bytes_read))
    return filesize
