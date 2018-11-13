import socket
import json

if __name__ == '__main__':
    param = ["Dette", "Er", "Parametere", "Fra", "Server"]
    # next create a socket object
    s = socket.socket()
    print ("Socket successfully created")

    # reserve a port on your computer in our
    # case it is 12345 but it can be anything
    port = 12345

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind(('127.0.0.1', port))
    print ("socket binded to " ,port)

    # put the socket into listening mode
    s.listen(5)
    print ("socket is listening")

    # a forever loop until we interrupt it or
    # an error occurs
    while True:
        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from', addr)
        jstr = json.dumps(param)
        # send a thank you message to the client.
        c.send(jstr.encode())

        # Close the connection with the client
        c.close()
