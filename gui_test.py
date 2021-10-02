#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
import select
from tkinter import *
from tkinter import font
import tkinter.messagebox
from tkinter import ttk
from chat_utils import *
import json
import time
from datetime import date
 

  
class tkinterApp(Tk):
     
    # __init__ function for class tkinterApp
    def __init__(self, send, recv, sm, s, *args, **kwargs):
         
        # __init__ function for class Tk
        Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""
        self.friends = ''
        self.current_page = ''
        
        # initializing frames to an empty array
        self.frames = {} 
        
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
        self.current_page = "SP"
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
  
# first window frame startpage
  
class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.controller = controller
        parent.grid_rowconfigure(1, weight = 1)
        parent.grid_columnconfigure(2, weight = 1)
        
        self.parent = parent
        
        self.namelbl = ttk.Label(self, text="Name:")
        self.name_field = ttk.Entry(self)
        # we need to set a function linked to the listener for the login button
        # if the button is pressed and the self.out message from UP3 is good
        #then we move to close this window and open the main_window - (still need to figure this one out)
        # otherwise we have to create a message dialog box that displays the warning message from the UP3 
        
        #PS: We might also consider a message dialogbox for the main window
        
        
        #self.themes = ttk.Combobox(self, text="Light", values = ['Light', 'Dark'], state = "readonly", width=5)
        #self.themes.set('Light')
        
        self.login_button = ttk.Button(self, text="Login",command = lambda: self.goAhead(self.name_field.get()))
        
        self.grid(column=0, row=2, sticky=(N, S, E, W))
        self.grid(column=2, row=2, sticky=(N, S, E, W))
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        self.grid(column=1, row=0, sticky=(N, S, E, W))
        self.grid(column=2, row=1, sticky=(N, S, E, W))
        self.grid(column=2, row=0, sticky=(N, S, E, W))
        #these are the empty sqares on the GUI
        
        self.namelbl.grid(column=0, row=1, sticky=(S, E), padx=(70, 10), pady=(70,0))
        self.name_field.grid(column=1, row=1, sticky=(S, W), pady=(70,0))
        #self.themes.grid(column=2, row=0, sticky=(N,E))
        
        self.login_button.grid(column=1, row=2, sticky=(N, W), pady=(0,70))
        

        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
   
    
    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action":"login", "name": name})
            self.controller.send(msg)
            response = json.loads(self.controller.recv())
            if response["status"] == 'ok':
                
                self.controller.sm.set_state(S_LOGGEDIN)
                self.controller.sm.set_myname(name)
                
                self.controller.friends = self.get_friends()
                self.controller.frames[Page1].set_friends()
                
                self.controller.show_frame(Page1)
                self.controller.current_page = "P1"
              
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()
            
    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.controller.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            # if self.controller.sm.get_state() == S_CHATTING and self.controller.current_page != "P2":
            #     self.controller.frames[Page2].set_members()
            #     self.controller.show_frame(Page2)
            #     self.controller.current_page = "P2"
            
            # if self.controller.sm.get_state() == S_LOGGEDIN and self.controller.current_page != "P1":
            #     self.controller.show_frame(Page1)
            #     self.controller.current_page = "P1"
            
            if self.controller.socket in read:
                peer_msg = self.controller.recv()
                
                    #print(self.controller.friends, "check")
            if len(self.controller.my_msg) > 0 or len(peer_msg) > 0:
                #print()
                show = False
                if self.controller.my_msg == 'refresh':
                    self.controller.friends = self.get_friends()
                    self.controller.my_msg = ""
                
                
                    
                    #print(self.controller.system_msg)
                    #self.controller.system_msg = self.controller.sm.proc(self.controller.my_msg, peer_msg) # used to be +=
                    #self.controller.my_msg = ""
                    #print(self.controller.system_msg)
                elif self.controller.sm.get_state() == S_LOGGEDIN:
                    
                    #if len(self.my_msg) > 0 or len(peer_msg) > 0:
                        #if self.parent.focus_get() == ".!frame.!page1.!entry":
                        if len(self.controller.my_msg) > 2 and self.controller.my_msg[0] == 'c':
                                self.controller.sm.set_state(S_CHATTING)
                                print( self.controller.sm.get_state())
                                
                                self.controller.system_msg = self.controller.sm.proc(self.controller.my_msg, peer_msg)
                                self.controller.show_frame(Page2)
                                self.controller.current_page = "P2"
                                self.controller.my_msg = ""
                            
                        elif len(peer_msg) > 0:
                            #print("We are here")
                            response = json.loads(peer_msg)
                            print(str(response))
                            if response["action"] == "connect":
                                self.controller.sm.set_state(S_CHATTING)
                                print( self.controller.sm.get_state())
                                self.controller.show_frame(Page2)
                                self.controller.current_page = "P2"
                            
                        elif self.controller.frames[Page1].menu.get()== self.controller.frames[Page1].combo_options[0]:
                            
                            print(self.controller.system_msg)
                            if self.controller.my_msg in "1234567890":
                                self.controller.system_msg = self.controller.sm.proc("p"+self.controller.my_msg, peer_msg) # used to be +=
                                self.controller.my_msg = ""
                                print(self.controller.system_msg)
                                show = True
                            
                            else:
                                #self.controller.frames[Page1].wrong_input('poem')
                                self.controller.frames[Page1].wrong_input()
                                self.controller.frames[Page1].search_field.delete(0, END)
                                self.controller.my_msg = ''

                        elif self.controller.frames[Page1].menu.get()== self.controller.frames[Page1].combo_options[1]:
                            print(self.controller.system_msg)
                            self.controller.system_msg = self.controller.sm.proc("?"+self.controller.my_msg, peer_msg) # used to be +=
                            self.controller.my_msg = ""
                            show = True
                        
                            
                        if show:
                            self.controller.frames[Page1].srtext.config(state = NORMAL)
                            self.controller.frames[Page1].srtext.insert(END, self.controller.system_msg +"\n\n")      
                            self.controller.frames[Page1].srtext.config(state = DISABLED)
                            self.controller.frames[Page1].srtext.see(END)
                            
                            
                    # self.controller.frames[Page1].srtext.config(state = NORMAL)
                    # self.controller.frames[Page1].srtext.insert(END, self.controller.system_msg +"\n\n")      
                    # self.controller.frames[Page1].srtext.config(state = DISABLED)
                    # self.controller.frames[Page1].srtext.see(END)
                    
                elif self.controller.sm.get_state() == S_CHATTING:
                    
                    if self.controller.my_msg == 'bye':
                        #new addition
                        self.controller.frames[Page2].chat.config(state = NORMAL)
                        self.controller.frames[Page2].chat.insert(END, ( "[["+self.controller.sm.get_myname()+"]] : " + "Has left the chat" )+"\n\n", ('left'))     
                        self.controller.frames[Page2].chat.config(state = DISABLED)
                        self.controller.frames[Page2].chat.see(END)
                        self.controller.sm.proc(self.controller.my_msg, peer_msg)
                        #print( self.controller.sm.proc(self.controller.my_msg, peer_msg), "test")
                        self.controller.my_msg = "" 
                        # msg = json.dumps({"action":"disconnect"})
                        # self.controller.send(msg)
                        self.controller.frames[Page2].chat.tag_configure("left", justify='left')
                        self.controller.frames[Page2].chat.tag_add('1.0', 'end')
                        
                       
                        
                    
                                                                  
                        self.controller.show_frame(Page1)
                        self.controller.current_page = "P1"
                        

                    elif len(peer_msg) > 0:
        
                        #print("We are here")
                        response = json.loads(peer_msg)
                        print(str(response))
                        if response["action"] == "exchange":
                            
                            self.controller.frames[Page2].chat.tag_configure("left", justify='left')
                            self.controller.frames[Page2].chat.tag_add('1.0', 'end')
        
                            self.controller.frames[Page2].chat.config(state = NORMAL)
                            self.controller.frames[Page2].chat.insert(END, ( "["+response["from"]+"] : " + response["message"]) +"\n\n", ('left'))     
                            self.controller.frames[Page2].chat.config(state = DISABLED)
                            self.controller.frames[Page2].chat.see(END)
                
                else:
                    print(self.controller.system_msg)
                    self.controller.my_msg = ""

    def get_friends(self):
        msg = json.dumps({"action":"list"})
        self.controller.send(msg)
        response =json.loads(self.controller.recv())
        return response["results"]
  
  
# second window frame page1
class Page1(Frame):
     
    def __init__(self, parent, controller):
         
        Frame.__init__(self, parent)
        
        parent.grid_columnconfigure(3, weight=1)     
        parent.grid_rowconfigure(3, weight=1)
        
        self.parent = parent
        self.controller = controller
        
        # self.send = send
        # self.recv = recv
        # self.sm = sm
        # self.socket = s
        # self.my_msg = my_msg
        # self.system_msg = system_msg
        
        self.s = ttk.Style()
        self.s.configure('check.TLabel', font='helvetica 20')
        
        self.timelbl = ttk.Label(self, anchor='center', style='check.TLabel')
        
        
        self.search_field = ttk.Entry(self)
    
        #themevar = StringVar()
        #menuvar= StringVar()

        #self.themes = ttk.Combobox(self, text='Light', values = ['Light', 'Dark'], state = "readonly", width=5)
        #self.themes.set('Light')
        
        
        #self.themes.bind("<<ComboboxSelected>>", self.night_on)
        self.combo_options  = ['Poem', 'Chat history']
        self.menu = ttk.Combobox(self, text='Poem', values = self.combo_options, state = "readonly", width=9)
        self.menu.set(self.combo_options[0])
        
        
        #self.srvalues = ('1. '+'Pouette Pouette'*200) 
        
        # for now this is what the result shows, but this must be changed to self.out drom the UP3
        #I suggest we create a function linked to a listener in the entry field (wait for the enter key to be pressed)
        # Then this value is updated in the listener function and we change the text of the textfield
        # by deleting the current content and adding the new one - this is a bit tricky check TKdocs


        self.srtext = Text(self, width=50, height=25, wrap='word')
        self.srtext.config(state = NORMAL)
        self.srtext.insert(END, menu +"\n\n")      
        self.srtext.config(state = DISABLED)
        self.srtext.see(END)
        self.srtext.grid(column=3, row=2, columnspan=2, sticky= (N,S,E,W))
        
        #self.srtext.insert('1.0', self.srvalues)
        
        self.srtext.config(state=DISABLED)
        self.srtext.bind("<1>", lambda event: self.srtext.focus_set()) 
        # This enables the user to copy/ select the search results
        
        sr_vscroll = ttk.Scrollbar( self, orient=VERTICAL, command=self.srtext)
        sr_vscroll.grid(column = 5, row= 2, sticky= (N,S) )
        self.srtext.configure(yscrollcommand= sr_vscroll.set)
        
        self.quit_button = ttk.Button(self, text="Quit", command = lambda : self.controller.destroy() )
        
        self.clear_button = ttk.Button(self, text="Clear", command = lambda : self.wipe() )
        
        self.refresh_button = ttk.Button(self, text="Refresh", command = lambda : self.sendQuery('refresh') )
        
        self.choices = [""]
        self.choicesVar = StringVar(value= self.choices)
        self.friends = Listbox(self, height=35)
        self.friends.bind("<Double-1>", lambda e: self.connect( self.choices [ self.friends.curselection()[0] ] ) )
        
        
        self.timelbl.grid(column=3, row=0, padx=(45,0), pady=(25,0))
        self.display_time() 
        # This function is executed every second
        # The code sets its own event so it is detected in the loop
        
        
        
        self.friends.grid(column = 0, row=0, rowspan = 4, sticky=(N,S))
        friends_vscroll = ttk.Scrollbar( self, orient=VERTICAL, command=self.friends.yview)
        friends_vscroll.grid(column = 1, row= 0, sticky= (N,S) )
        self.friends.configure(yscrollcommand=friends_vscroll.set)
        self.set_friends()
            
        # This function is executed every second
        # The code sets its own event so it is detected in the loop
        # We need to change the names to those from the UP3 group class 
        # Make sure to send them to the listbox as --> StringVar(value= list_of_string) 
        
        self.refresh_button.grid(column=2, row=0, sticky=(N,W)) 
        self.menu.grid(column=2, row=1, pady=(35,0), padx=(30,0), sticky=(E) ) 
        self.search_field.grid(column=3, row=1, columnspan=2, pady=(35,0), sticky=(W))
        self.search_field.bind('<Return>', lambda event: self.sendQuery(self.search_field.get() ) )
       
        self.clear_button.grid(column=3, row=3, sticky=(S, E), pady=(0,10))
        self.quit_button.grid(column=4, row=3, sticky=(S, E), pady=(0,10))
        
    
        self.grid(column=2, row=0, sticky=(N, S, E, W))
        self.grid(column=2, row=2, sticky=(N, S, E, W))
        self.grid(column=2, row=3, sticky=(N, S, E, W))
        #content.grid(column=3, row=3, sticky=(N, S, E, W))
        
        
        
        self.rowconfigure(2, weight=1)
       
        self.columnconfigure(4, weight=1)
        self.columnconfigure(3, weight=3)
    
        
    def sendQuery(self, msg):
        self.controller.my_msg = msg
        print(self.controller.my_msg)
        self.search_field.delete(0, END)
        
            
    
    def display_time(self):
        time_string = time.strftime('%H:%M')
        today = str(date.today()).split('-')
        today[0], today[1], today[2] = today[1], today[2], today[0]
        today = time_string+'  '+ '/'.join(today)
        self.timelbl['text'] = today
        self.parent.after(1000, self.display_time)
        
    def wipe(self):
        self.srtext.config(state=NORMAL)
        self.srtext.delete('1.0', END)
        self.srtext.config(state = DISABLED)
        self.srtext.see(END)
            
            
        
    # def set_friends(self):
    #     choices = ["Dany", "Nawaf", "Ola"] # this will come from the group class
    #     choicesvar = StringVar(value=choices)
    #     self.friends['listvariable'] = choicesvar
    #     for i in range(0,len(choices),2):
    #         self.friends.itemconfigure(i, background='#f0f0ff')
    #     self.parent.after(1000, self.set_friends)
    
    

    def set_friends(self):
        if len(self.controller.friends) > 0:
            list_of_members = [""]
            list_of_members =self.controller.friends.split(" ")
           
            list_of_members.pop()
    
            for i in range(len(list_of_members)):
                value = list_of_members[i]
    
                if value == self.controller.sm.get_myname():
                    list_of_members[i] += "(you)"
                    list_of_members[0], list_of_members[i] = list_of_members[i], list_of_members[0]
             
             # for i in range(0,len(list_of_members),2):
             #     self.controller.frames[Page1].friends.itemconfigure(i, background='#f0f0ff')
            
            self.choices = list_of_members
            #print(ch, "check")
            self.choicesVar.set(self.choices)
            self.friends['listvariable'] = self.choicesVar
            
            
            self.parent.after(1000, self.set_friends)
    
    def connect(self, peer):
        #print("c "+peer)
        #self.sendQuery("c "+peer)
        msg = json.dumps({"action":"connect", "target": peer})
        self.controller.send(msg)
        
        
        
    
    def wrong_input(self):
        tkinter.messagebox.showinfo("Input Error", "Please enter a poem number.")
     # msg = json.dumps({"action":"list"})
     #        self.controller.send(msg)
     #        response =json.loads(self.controller.recv())
     #        choices = response["results"]
     #        print(choices)
 
     #        list_of_members = [""]
     #        list_of_members =choices.split(" ")
     #        list_of_members.pop()

     #        for i in range(len(list_of_members)):
     #            value = list_of_members[i]
    
     #            if value == self.controller.sm.get_myname():
     #                list_of_members[i] += "(you)"
     #                list_of_members[0], list_of_members[i] = list_of_members[i], list_of_members[0]
             
             # for i in range(0,len(list_of_members),2):
             #     self.controller.frames[Page1].friends.itemconfigure(i, background='#f0f0ff')
         
            # ch = list_of_members
            # self.controller.frames[Page1].choicesVar.set(ch)
            # self.controller.frames[Page1].friends['listvariable'] = self.controller.frames[Page1].choicesVar

    # def proc(self):
    #     # print(self.msg)
    #     while True:
    #         read, write, error = select.select([self.socket], [], [], 0)
    #         peer_msg = []
    #         # print(self.msg)
    #         if self.socket in read:
    #             peer_msg = self.recv()
    #         if len(self.my_msg) > 0 or len(peer_msg) > 0:
    #             # print(self.system_msg)
    #             self.system_msg = self.sm.proc(self.my_msg, peer_msg) # used to be +=
    #             self.my_msg = ""
    #             self.srtext.config(state = NORMAL)
    #             self.srtext.insert(END, self.system_msg +"\n\n")      
    #             self.srtext.config(state = DISABLED)
    #             self.srtext.see(END)
  
      
    #function to basically start the thread for sending messages
    # def sendButton(self, msg):
    #     self.textCons.config(state = DISABLED)
    #     self.my_msg = msg
    #     # print(msg)
    #     self.entryMsg.delete(0, END)
    

  
  
  
  
# third window frame page2
class Page2(ttk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        parent.grid_columnconfigure(1, weight=1)     
        parent.grid_rowconfigure(1, weight=1)
        
        self.parent = parent
        self.controller = controller
        
        self.s = ttk.Style()
        self.s.configure('check.TLabel', font='helvetica 20')
        
        self.timelbl = ttk.Label(self, anchor='center', style='check.TLabel')
        
        
        self.message_field = ttk.Entry(self)
    
        #themevar = StringVar()
        #menuvar= StringVar()

        #self.themes = ttk.Combobox(self, text='Light', values = ['Light', 'Dark'], state = "readonly", width=5)
        #self.themes.set('Light')
        
        #self.themes.bind("<<ComboboxSelected>>", self.night_on)
        
        self.s1 = ttk.Style()
        self.s1.configure('members.TLabel', font='helvetica 15')
        #self.set_members()
        self.memberslbl = ttk.Label(self, text=self.controller.sm.get_myname(), style = 'members.TLabel' )
        
        #self.srvalues = ('1. '+'Pouette Pouette'*200) 
        
        # for now this is what the result shows, but this must be changed to self.out drom the UP3
        #I suggest we create a function linked to a listener in the entry field (wait for the enter key to be pressed)
        # Then this value is updated in the listener function and we change the text of the textfield
        # by deleting the current content and adding the new one - this is a bit tricky check TKdocs
        
       
         
        self.chat = Text(self, width=50, height=25, wrap='word', bg = "#17202A",  fg = "#EAECEE", 
                           font = "Helvetica 14", padx = 5,  pady = 5)
        
        self.chat.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
        
        self.chat.grid(column=0, row=2, columnspan=3, sticky= (N,S,E,W), padx= (25,0))
        
        #self.srtext.insert('1.0', self.srvalues)
        
        self.chat.config(state=DISABLED)
        self.chat.bind("<1>", lambda event: self.chat.focus_set()) 
        # This enables the user to copy/ select the search results
        
        
        chat_vscroll = ttk.Scrollbar( self, orient=VERTICAL, command=self.chat)
        chat_vscroll.grid(column = 3, row= 2, sticky= (N,S) )
        self.chat.configure(yscrollcommand= chat_vscroll.set)
        
        self.disconnect_button = ttk.Button(self, text="Disconnect", command = lambda : self.controller.frames[Page1].sendQuery("bye") )
        
        
        self.send_button = ttk.Button(self, text="Send", command = lambda : self.send_chat_Msg( self.message_field.get() ) )
        
        
        #self.friends = Listbox(self, height=35)
        
        
        
        self.timelbl.grid(column=1, row=0, sticky= (N,S,W,E) ) #padx=(45,0), pady=(25,0)
        
        
        self.memberslbl.grid(column=1, row=1, sticky= (N,S,W,E) ) #padx=(45,0), pady=(25,0)
        
        self.display_time() 
        # This function is executed every second
        # The code sets its own event so it is detected in the loop
        
        
        
        #self.friends.grid(column = 0, row=0, rowspan = 4, sticky=(N,S))
        #friends_vscroll = ttk.Scrollbar( self, orient=VERTICAL, command=self.friends.yview)
        #friends_vscroll.grid(column = 1, row= 0, sticky= (N,S) )
        #self.friends.configure(yscrollcommand=friends_vscroll.set)
        
        #self.set_friends() 
        # This function is executed every second
        # The code sets its own event so it is detected in the loop
        # We need to change the names to those from the UP3 group class 
        # Make sure to send them to the listbox as --> StringVar(value= list_of_string) 
        
        #self.themes.grid(column=4, row=0, sticky=(N,E)) 
        #self.menu.grid(column=2, row=1, pady=(35,0), padx=(30,0), sticky=(E) ) 
        self.message_field.grid(column=0, row=3, columnspan=2,  sticky=(W, E), pady=(0,25), padx= (25,0) )
        self.message_field.bind('<Return>', lambda event: self.send_chat_Msg(self.message_field.get() )  )
       
        self.send_button.grid(column=2, row=3, pady=(0,25),  ) #sticky=(S, E) pady=(0,10)
        self.disconnect_button.grid(column=4, row=3, pady=(0,25), padx= (10,0) ) # sticky=(S, E), pady=(0,10)
        
    
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        self.grid(column=0, row=1, sticky=(N, S, E, W))
        self.grid(column=2, row=0, sticky=(N, S, E, W))
        self.grid(column=2, row=1, sticky=(N, S, E, W))
        self.grid(column=4, row=2, sticky=(N, S, E, W))
        self.grid(column=4, row=1, sticky=(N, S, E, W))
        self.grid(column=4, row=0, sticky=(N, S, E, W))
        
        #content.grid(column=3, row=3, sticky=(N, S, E, W))
        
        
        
        self.rowconfigure(2, weight=1)
       
        #self.columnconfigure(4, weight=1)
        #self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)
    
    
    # def sendMsg(self, message):
    #     self.controller.my_msg = message
        
    # def set_members(self):
        
    #     self.parent.after(1000, self.set_members)
    
    def display_time(self):
        time_string = time.strftime('%H:%M')
        today = str(date.today()).split('-')
        today[0], today[1], today[2] = today[1], today[2], today[0]
        today = time_string+'  '+ '/'.join(today)
        self.timelbl['text'] = today
        self.parent.after(1000, self.display_time)
    
    def send_chat_Msg(self, msg):
        self.chat.tag_configure("right", justify='right')
        self.chat.tag_add('1.0', 'end')
        
        self.chat.config(state = NORMAL)
        self.chat.insert(END, (msg +"\n\n"), ('right'))     
        self.chat.config(state = DISABLED)
        self.chat.see(END)
        self.message_field.delete(0, END)
                            
        the_msg = json.dumps({"action":"exchange", "message": msg, "from": self.controller.sm.get_myname() })
        self.controller.send(the_msg)
            
# Driver Code
def run_gui(send, recv, sm, socket):
    app = tkinterApp(send, recv, sm, socket)
    app.mainloop()
    