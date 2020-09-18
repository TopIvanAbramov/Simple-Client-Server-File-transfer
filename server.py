import asyncio
import socket

def get_new_filename(name, extension):
    try:
        f = open(name + "." + extension)
        f.close()
        i = 1
        while True:                                                     # try different file names
            try:                                                        # untill find one which is free
                f = open(name + "_copy{}".format(i) + "." + extension)
                f.close()
                i += 1
                continue
            except IOError:
                return name + "_copy{}".format(i) + "." + extension

    except IOError:
        f = open(name + "." + extension, "w+")
        f.close()
        return name + "." + extension


async def handle_echo(reader, writer):                                 # handle client packets
    data = await reader.read(100)                                      # receive file name from client and send it back
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received filename {} from {}".format(message, addr))
    filename = message

    name, extension = filename.split('.')
    new_filename = get_new_filename(name, extension)                   # check if file with given name already exists

    print("\nNew filename: {}\n".format(new_filename))                 # then return new file name

    f = open(new_filename, "wb")

    print("Send: %r" % message)
    writer.write(data)

    data = await reader.read(100)                                       # receive file size from client and send it back
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print("Received file size {} from {}".format(message, addr))
    filesize = int(message)

    print("Send: %r" % message)
    writer.write(data)
    await writer.drain()

    size_of_packet = 512
    number_of_packets = filesize // size_of_packet + 1

    for i in range(number_of_packets):                                  # start to receive file by packets
        print("Packer number: {}\n".format(i))                          # each packet is up to 512 b
        data = await reader.read(size_of_packet)
        f.write(data)

    f.close()

    print("File successfully transferred: {} ".format(filename))

    print("Close the client socket")
    writer.close()


def main():
    TCP_IP = socket.gethostbyaddr("your_server_ip")[0]
    TCP_PORT = 9001

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, TCP_IP, TCP_PORT, loop=loop)
    server = loop.run_until_complete(coro)

                                                                        # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


    server.close()                                                        # Close the server
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    main()
