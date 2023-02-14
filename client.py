from tkinter import *
import socket
import threading
from tkinter import messagebox


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddr=((socket.gethostname(),9999))

class APP:
    def __init__(self):
        self.root = Tk()
        self.root.title("Chat room")
        self.name = StringVar()
        self.msg = StringVar()
        self.login = Frame(self.root)
        self.login.pack(fill='both',expand=True)

        self.root.eval('tk::PlaceWindow . center')
        
        self.welcome_label = Label(self.login,text="Welcome to the chat room",font=("Helvetica",16))
        self.welcome_label.pack(pady=10)

        self.name_label = Label(self.login,text="Enter your name: ",font=("Helvetica",12))
        self.name_label.pack()

        self.name_entry = Entry(self.login,textvariable=self.name,font=("Helvetica",12))
        self.name_entry.pack()

        self.enter_button = Button(self.login,text="Enter",font=("Helvetica",12),command=self.validate_login)
        self.enter_button.pack()




        self.mainpage = Frame(self.root)
        


        self.l1 = Label(self.mainpage,text='')
        self.l1.pack()

        self.frame = Frame(self.mainpage)
        self.frame.pack()

        self.textbox = Text(self.frame,height=22,width=47)
        self.textbox.pack(side='left')

        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side='right',fill='y')

        self.scrollbar.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=self.scrollbar.set)
        self.textbox.config(state=DISABLED)

        self.frame2 = Frame(self.mainpage)
        self.frame2.pack()

        self.input_left = Entry(self.frame2,textvariable=self.msg,width=35,font=17)
        self.input_left.pack(side='left')
        self.button_right = Button(self.frame2,text='Send',font=17,command=self.send_message)
        self.button_right.pack(side='right')

        self.exit_button = Button(self.mainpage,text='Exit',font=17,command=self.logout)
        self.exit_button.pack()

        self.root.mainloop()

    def logout(self):
        s.sendto(f'exit:{self.name.get()} Left the chat'.encode(),serverAddr)
        self.root.destroy()
    def send_message(self):
        s.sendto(f'send:{self.msg.get()}'.encode(),serverAddr)
        self.input_left.delete(0,END)
            
    def get_message(self):
        
        while True:
            try:
                s.settimeout(None)
                reply,cIp=s.recvfrom(1024)

                self.textbox.config(state=NORMAL)
                self.textbox.insert(END,reply.decode()+'\n')
                self.textbox.config(state=DISABLED)
                
            except:
                break


    def validate_login(self):
        name = self.name_entry.get()
        try:
            if name:
                s.sendto(f'login:{name}'.encode(),serverAddr)
                s.settimeout(2)
                self.login.pack_forget()
                self.mainpage.pack(fill='both',expand=True)
                get_message = threading.Thread(target=self.get_message)
                get_message.start()
                self.l1.config(text=self.name.get())
                self.root.title(f'Chatroom:{self.name.get()}')
                self.root.eval('tk::PlaceWindow . center')
                
            else:
                messagebox.showinfo('Error','Enter your name to continue') 
            
        except socket.timeout:
            messagebox.showinfo('Error','Connection timed out\nServer Down')
            self.root.destroy()
            
   

client = APP()
