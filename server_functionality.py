from os import *
import sys
from ex2utils import Server

class MyServer(Server):
    global no_of_user
    # This tells us the no of users connected to the server. 
    no_of_user = 0
    # we store all the users in an array.
    global users_stored
    users_stored = []
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
    # function tells us that server has started.
    def onStart(self):
        print("Server has started!!!")

#----------------------------------------------------------------------------------------------------------------------
    
    # function tells us that servers has stopped.
    def onStop(self):
        print("closing the server!!!")

#---------------------------------------------------------------------------------------------------------------------------------------------


    #function first adds the user which has joined to the server. then prints the no of users .
    def onConnect(self, socket):
        global no_of_user
        no_of_user += 1
        global users_stored
        users_stored.append(socket)
        print("number of users still on server =  ", no_of_user)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #main function which deals with all commands 
    def onMessage(self, socket,message):
        
        (command, sep, parameter) = message.strip().partition(' ')
        print("Command chosen: ", command)
        #First option of the command pallet is userName in which user gets to decide their name.it first checks if the user is already on the server,it tells the user to choose another name.
        if (command == "Name"):
            socket.name = None
            for user in users_stored:
                if (user.name == parameter):
                    message = "user name already exists,please choose another name using the command Name username"
                    message=message.encode()
                    socket.send(message)
                    socket.allowedMessages = False
                    print("the chosen name is invalid!!!")
                    return True
            print("Username:  ", parameter)
            socket.name = parameter
            socket.allowedMessages = True
            message = "welcome " + socket.name
            socket.send(message.encode())
            
            for user in users_stored:
                if (user == socket):
                    continue
                message = socket.name + " in the server. "           
                user.send(message.encode())
            return True

        if (socket.allowedMessages == False):
            message = "you have to choose a username. for help choose the command Name to set username."            
            socket.send(message.encode())
            return True

        #---------------------------------------------------------------------------------------------------------------------------
        #second option of the command pallet is connectedUsers which shows all the users that are connected to the server.
        elif (command == "connectedUsers"):
            for user in users_stored:
                name = "!" + str(user.name)
                socket.send(name.encode())

        #------------------------------------------------------------------------------------------------------------------------------
        # command to broadcast a message to everyone on the server.
        elif (command == "everyone"):
            print("Message is ", parameter)
            for user in users_stored:
                if (user == socket):
                    continue
                if (type(parameter) == str):
                    parameter = socket.name + ": " + parameter
                    parameter = parameter.encode()
                else:
                    parameter = parameter.decode()
                    parameter = socket.name + ": " + parameter
                    parameter = parameter.encode()
                user.send(parameter)
        #---------------------------------------------------------------------------------------------------------------
        #to send a message to a specific user on the server
        elif (command == "specify"):
            (username, sep, message) = parameter.strip().partition(' ')
            print("username: ", username)
            print("message:  ", message)
            if (socket.name == username):
                message = "!Invalid functionality as one cannot send a message to himself"
                socket.send(message.encode())
                return True

            for user in users_stored:
                if (user.name == username):
                    message = "Private message from " + socket.name + ": " + message
                    user.send(message.encode())
                    return True
            message = "!user is not on the server , please see the list of users using 'connectedUsers'"
            socket.send(message.encode())
        #-------------------------------------------------------------------------------------------------------------
        # to leave the chat application.
        elif (command == "exit"):
            None
        #implemented in client code.
            
        #-----------------------------------------------------------------------------------------------------------------
        # if the command given does not match any of the above commands.
        else:
            message = "The command you specified is not allowed, please choose the command again!!!"
            message=message.encode()
            socket.send(message)

        return True
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------


    # removes the user from the server if the user disconnects. then prints the no of users still left.
    def onDisconnect(self, socket):
        global no_of_user
        global users_stored
        print("Client disconnected")
        no_of_user -= 1
        print("number of users still on server =  ", no_of_user)
        users_stored.remove(socket)
        for user in users_stored:
            message = socket.name + " have left the chat!!!"
            user.send(message.encode())


    


#-----------------------------------------------------------------------------------------------------------------------------------------------------

# connects to the desired ip and port address.		  
ip = sys.argv[1]
port = int(sys.argv[2])

# Create server.
server = MyServer()

# Starts the server.
server.start(ip, port)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------