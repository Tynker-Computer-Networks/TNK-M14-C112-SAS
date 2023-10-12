import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))
print("Connected with the server...")

class GUI():
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()

        self.login = Toplevel()

        self.login.title("Login")
        
        self.login.resizable(width=False, height=False)
        
        self.login.configure(width=400, height=300, bg='#DAFFFB')

        self.page_label = Label( self.login, text = "Please login to continue",
                                font = "Helvetica 14 bold", bg='#DAFFFB')
        self.page_label.place(relx = 0.2, rely = 0.07)
        
        self.name_entry = Entry(self.login, font = "Helvetica 14",
							bg = "#b1e5e2",
							fg = "#222222")
        self.name_entry.place(relwidth = 0.4,
                            relheight = 0.12,
                            relx = 0.35,
                            rely = 0.2)
        self.name_entry.focus()

        self.name_label = Label(self.login,  text = "Name:",
                                font = "Helvetica 12", bg='#DAFFFB')
        self.name_label.place(relx = 0.1, rely = 0.2)
        
        self.login_button = Button(self.login, text = "Login",
                                  font = "Helvetica 14 bold",
                                  bg = "#176B87",
                                  fg = "#ffffff",
                                  command = lambda: self.go_ahead(self.name_entry.get()))
        self.login_button.place(relx = 0.4, rely = 0.55)

        self.window.mainloop()

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                print(message)
            except Exception as e:
                print("An error occurred!", e)
                client.close()
                break
            
    def go_ahead(self, name):
        # Call destroy method from self.login
        self.login.destroy()
        # Call layout method and pass the name
        self.layout(name)    
        receive_thread = Thread(target=self.receive)
        receive_thread.start()

    def layout(self,name):
        self.name = name

        # Call deiconify() from self.window
        self.window.deiconify()
        # Add title as CHATROOM
        self.window.title("CHATROOM")

        self.window.resizable(width = False,
							height = False)
        self.window.configure(width = 470,
							height = 550,
							bg = "#176B87")
        
        # Uncomment rest of the code to place various controls on the screen
        self.label_head = Label(self.window,
							bg = "#176B87",
							fg = "#ffffff",
							text = self.name ,
							font = "Helvetica 13 bold",
							pady = 5)
		
        self.label_head.place(relwidth = 1)
        self.line = Label(self.window,
						width = 450,
						bg = "#ABB2B9")
		
        self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
				
        self.label_bottom = Label(self.window,
								bg = "#fffff0",
								height = 80)
		
        self.label_bottom.place(relwidth = 1,
							rely = 0.825)
		
        self.entry_msg = Entry(self.label_bottom,
							bg = "#b1e5e2",
							fg = "#222222",
							font = "Helvetica 13")
		
        self.entry_msg.place(relwidth = 0.74,
							relheight = 0.06,
							rely = 0.008,
							relx = 0.011)
		
        self.entry_msg.focus()
		
        self.button_msg = Button(self.label_bottom,
								text = "Send",
								font = "Helvetica 10 bold",
								width = 20,
								bg = "#176B87",
                                fg = "#ffffff",
                                )
		
        self.button_msg.place(relx = 0.77,
							rely = 0.008,
							relheight = 0.06,
							relwidth = 0.22)
	

def write():
    while True:
        message = '{}: {}'.format("nickname", input(''))
        client.send(message.encode('utf-8'))

write_thread = Thread(target=write)
write_thread.start()


app = GUI()
