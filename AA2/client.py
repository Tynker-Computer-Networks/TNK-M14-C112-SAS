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
                print("Message: ", message)
                self.show_message(message)
            except Exception as e:
                print("An error occurred!", e)
                client.close()
                break
            
    def go_ahead(self, name):

        # Use iconify() instead of destroy
        # self.login.destroy()
        self.login.iconify()
        
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
							bg = "#176B87")
        
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
		
        self.text_comm = Text(self.window,
							width = 20,
							height = 2,
							bg = "#DAFFFB",
							fg = "#444444",
							font = "Helvetica 14",
							padx = 5,
							pady = 5)
        
        self.text_comm.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
        
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
								font = "Helvetica 14 bold",
								width = 20,
								bg = "#176B87",
                                fg = "#ffffff",
                                command = lambda: self.send_button(self.entry_msg.get())
                                )
		
        self.button_msg.place(relx = 0.55,
							rely = 0.008,
                            relheight = 0.06,
							relwidth = 0.22)
       
        self.button_clear = Button(self.label_bottom,
								text = "Clear",
								font = "Helvetica 14 bold",
								width = 20,
								bg = "#176B87",
                                fg = "#ffffff",
                                command = lambda: self.clear_button()
                                )
		
        self.button_clear.place(relx = 0.77,
							rely = 0.008,
                            relheight = 0.06,
							relwidth = 0.22)
		
        self.text_comm.config(state = DISABLED)
        self.text_comm.config(cursor = "arrow")
		
        scrollbar = Scrollbar(self.text_comm)
        scrollbar.place(relheight = 1, relx = 0.974)
        scrollbar.config(command = self.text_comm.yview)

        # Call logout() method on the button click
        self.logout_button = Button(self.label_bottom, text="Logout", font="Helvetica 14 bold",
                                    width=20, bg="#176B87", fg="#ffffff", command=self.logout)
        self.logout_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    # Define logout method
    def logout(self):
        # Hide the chat window using withdraw()
        self.window.withdraw() 
        # Show the login window using deiconify() 
        self.login.deiconify()  
		
    def send_button(self, msg):
        self.text_comm.config(state = DISABLED)
        self.msg=msg
        self.entry_msg.delete(0, END)
        write_thread = Thread(target=self.write)
        write_thread.start()

    def clear_button(self):
        self.text_comm.config(state = NORMAL)
        self.text_comm.delete('1.0', END)
        self.text_comm.config(state = DISABLED)
       
    def write(self):
        while True:
            message = '{}: {}'.format(self.name, self.msg)
            client.send(message.encode('utf-8'))
            self.show_message(message)
            break
    
    def show_message(self, message):
        self.text_comm.config(state = NORMAL)
        self.text_comm.insert(END, message+"\n\n")
        self.text_comm.config(state = DISABLED)
        self.text_comm.see(END)
          
app = GUI()
