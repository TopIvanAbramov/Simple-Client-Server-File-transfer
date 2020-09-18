import asyncio
import sys
import os
import tqdm

BUFFER_SIZE = 1024


async def tcp_client(filename, TCP_IP, TCP_PORT, loop):
    reader, writer = await asyncio.open_connection(TCP_IP, TCP_PORT,        # open connection
                                                   loop=loop)
    try:
        f = open(filename, 'rb')
    except:
        print("No such file exist")
        writer.close()
        return 1

    filesize = os.path.getsize(filename)

    print("Filesize: {} {}".format(filesize, type(filesize)))

    writer.write(filename.encode())                                         # send file name to server

    data = await reader.read(100)
    print('Received filename: %r' % data.decode())

    writer.write(str(filesize).encode())                                    # send file size to server

    data = await reader.read(100)
    print('Received file size: %r' % data.decode())

    progress = tqdm.tqdm(range(filesize), "Sending {}".format(filename), unit="B", mininterval=0,
                         leave=True, unit_scale=True, unit_divisor=1000)      # this object display progress bar

    f = open(filename, 'rb')

    size_of_packet = 512

    l = f.read(size_of_packet)

    for _ in progress:
        while (l):                                                             # send file in chuncks of 512 b to server
            writer.write(l)
            l = f.read(size_of_packet)
            progress.update(len(l))

        if not l:
            f.close()
            writer.close()
            progress.disable = True
            break

    print('Successfully send the file')

    print('Close the socket')
    writer.close()

def parse_command_line_arguments():         # parse command arguments
    if len(sys.argv) == 4:                  # especially ip, port of the server and file name to transfer
        filename = sys.argv[1]
        TCP_IP = sys.argv[2]
        TCP_PORT = int(sys.argv[3])
        return (filename, TCP_IP, TCP_PORT)
    else:
        return 1


def main():
    try:
        filename, TCP_IP, TCP_PORT = parse_command_line_arguments()
    except:
        print("Not enough arguments: file domain-name|ip-address port-number")
        return

    loop = asyncio.get_event_loop()         #
    loop.run_until_complete(tcp_client(filename, TCP_IP, TCP_PORT, loop))


if __name__ == '__main__':
    main()
