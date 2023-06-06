from os.path import getsize
from tqdm import tqdm

def int_from_32_byte(s):
    i = ""
    for b in s:
        if b=='a':
            break
        i+=b
    return int(i)

def int_to_32_byte(i):
    i = str(i)
    while len(i) < 32:
        i+="a"
    return i

def send_file(server, BUFFER_SIZE, FILENAME):
    filesize = getsize(FILENAME)
    print("Sending file with following size: ", filesize)
    server.sendall(int_to_32_byte(filesize).encode("utf-8"))
    
    progress = tqdm(range(0, filesize, BUFFER_SIZE), f"Sending...", unit="B", unit_scale=True, unit_divisor=BUFFER_SIZE)
    with open(FILENAME, "rb") as f:
        for i in progress:
            bytes_read = f.read(BUFFER_SIZE)
            server.sendall(bytes_read)
            progress.update(len(bytes_read))
    
def receive_file(conn, BUFFER_SIZE, OUT_PATH):
    """ Receive filesize from the client """
    filesize = int_from_32_byte(conn.recv(32).decode("utf-8"))
    print('File mit folgender Size angekuendigt: ', filesize)

    """ Receive buffers """
    progress = tqdm(range(0, filesize, BUFFER_SIZE), f"Receiving...", unit="B", unit_scale=True, unit_divisor=BUFFER_SIZE)
    with open(OUT_PATH, "wb") as f:
        for i in progress:
            bytes_read = conn.recv(BUFFER_SIZE)
            f.write(bytes_read)
            progress.update(len(bytes_read))
    return filesize