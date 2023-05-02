import socket
from os.path import getsize
from tqdm import tqdm

def send_file(client, filename, BUFFER_SIZE):
    filesize = getsize(filename)
    client.send(f"{filename}".encode())

    # start sending the file
    progress = tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=BUFFER_SIZE)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            client.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))