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
        
        self.login.configure(width=400, height=300)

        self.page_label = Label( self.login, text = "Please login to continue",
                                font = "Helvetica 14 bold")
        self.page_label.place(relx = 0.2, rely = 0.07)
        
        self.name_entry = Entry(self.login, font = "Helvetica 14")
        self.name_entry.place(relwidth = 0.4,
                            relheight = 0.12,
                            relx = 0.35,
                            rely = 0.2)
        self.name_entry.focus()

        self.name_label = Label(self.login,  text = "Name:",
                                font = "Helvetica 12")
        self.name_label.place(relx = 0.1, rely = 0.2)
        
        self.login_button = Button(self.login, text = "Login",
                                  font = "Helvetica 14 bold",
                                  command = lambda: self.go_ahead(self.name_entry.get()))
        self.login_button.place(relx = 0.4, rely = 0.55)

        self.window.mainloop()


    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                print("Message: ", message)
                # Call show_message() method
                self.show_message(message)
            except Exception as e:
                print("An error occurred!", e)
                client.close()
                break
            
    def go_ahead(self, name):
        self.login.destroy()
        self.layout(name)    
        receive_thread = Thread(target=self.receive)
        receive_thread.start()

    def layout(self,name):
        self.name = name
        self.window.deiconify()
        self.window.title("CHATROOM")

        self.window.resizable(width = False,
							height = False)
        self.window.configure(width = 470,
							height = 550,
							bg = "#17202A")
        
        self.label_head = Label(self.window,
							bg = "#17202A",
							fg = "#EAECEE",
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
		
        self.text_comm = Text(self.window,
							width = 20,
							height = 2,
							bg = "#17202A",
							fg = "#EAECEE",
							font = "Helvetica 14",
							padx = 5,
							pady = 5)
        
        self.text_comm.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
        
        self.label_bottom = Label(self.window,
								bg = "#ABB2B9",
								height = 80)
		
        self.label_bottom.place(relwidth = 1,
							rely = 0.825)
		
        self.entry_msg = Entry(self.label_bottom,
							bg = "#2C3E50",
							fg = "#EAECEE",
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
								bg = "#ABB2B9",
                                command = lambda: self.send_button(self.entry_msg.get())
                                )
		
        self.button_msg.place(relx = 0.77,
							rely = 0.008,
                            relheight = 0.06,
							relwidth = 0.22)
		
        self.text_comm.config(state = DISABLED)
        self.text_comm.config(cursor = "arrow")
		
        # Add scrollbar on text_comm
        scrollbar = Scrollbar(self.text_comm)
        # Place the scroll bar
        scrollbar.place(relheight = 1, relx = 0.974)
        # Config the scrollbar to move the textCon content vertically
        scrollbar.config(command = self.text_comm.yview)
		
    def send_button(self, msg):
        self.text_comm.config(state = DISABLED)
        self.msg=msg
        self.entry_msg.delete(0, END)
        write_thread = Thread(target=self.write)
        write_thread.start()
       
    def write(self):
        while True:
            message = '{}: {}'.format(self.name, self.msg)
            client.send(message.encode('utf-8'))
            # Call show_message() method
            self.show_message(self.msg)
            break
    
    # Create show_message() method that takes a message as argument
    def show_message(self, message):
        # Configure texCons state to NORMAL
        self.text_comm.config(state = NORMAL)
        # Use insert method on text_comm to add the message
        self.text_comm.insert(END, message+"\n\n")
        # Configure texCons state to DISABLED
        self.text_comm.config(state = DISABLED)
        # Use see(END) method to scroll to end of the text_comm
        self.text_comm.see(END)
          
app = GUI()
