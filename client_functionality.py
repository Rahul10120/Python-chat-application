"""

IRC client exemplar.

"""

import sys
from ex2utils import Client


class IRCClient(Client):
    def onMessage(self, socket, message):
		# *** process incoming messages here ***
        if (message[0] == "!"):
            print(message[1:])
        else:
           print(message)
           print("choose from the given commands: ")
        return True


# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])
Name_on_display = sys.argv[3]

# Create an IRC client.
client = IRCClient()

# Start server
client.start(ip, port)


#send message to the server
#message = "hello world"
#client.send(message.encode())

# show the possible commands a user can access.
print("choose a command: ")
print("connectedUsers: shows all the users that are in the chat with you.")
print("Name username: you have to choose your username in order to continue.")
print("everyone message: You can message all the people that are in the chat")
print("specify username message: You can message a specific user in the chat")
print("exit: to leave the chat")
print("To choose a command and enter a message type for example: 'everyone hello all, how are we doing?'")

#---------------------------------------------------------------------------------------------------------------------------------

message="Name "+Name_on_display
client.send(message.encode())
#print("HI " + Name_on_display + " !")

#--------------------------------------------------------------------------------------------------------------------------
while client.isRunning():
    command = input()
    if (command == "exit"):
        client.send(command.encode())
        client.stop()
        print("Connection closed! Thanks for using the chat application")
    else:
        client.send(command.encode())
        print("Enter a command of your choice:")

#stops client
client.stop()
