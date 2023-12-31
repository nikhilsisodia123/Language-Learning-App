# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import sqlite3
import random 
import numpy as np
from PIL import Image, ImageTk
from tkfontawesome import icon_to_image

menu_width = 10
topbar_colour = "lightblue"
topbar_height=44


class initialise(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        #icons
        self.sandwich = icon_to_image("bars", fill="#111212", scale_to_height=30)  #Doesn't need to be self as mainloop() is in same scope but better 
        self.cog = icon_to_image("cog", fill="#111212", scale_to_height=30)        #incase mainloop is moved
        
        self.topbar = tk.Frame(self, bg=topbar_colour)
        self.topbar.rowconfigure(0)
        self.topbar.columnconfigure(0, weight=1, uniform="b")
        self.topbar.columnconfigure(1, weight=200)
        self.topbar.columnconfigure(2, weight=1, uniform="b")
        self.topbar.pack(side=tk.TOP, fill = tk.X)
        self.menu = tk.Button(self.topbar, image=self.sandwich,width=109, command=self.sidebar_change)
        #self.menu.image = sandwich
        self.menu.grid(row=0, column=0, sticky="nsw")
        #self.languages = Languages(self.topbar, "blue")
        self.settings =tk.Button(self.topbar, text="Settings", image=self.cog)
        #self.settings.image=cog
        self.settings.grid(row=0, column=2, sticky = "nsew") #No set width
        #Dont use self.title as it will create problems when using dialogbox in database section
        self.title_ = tk.Label(self.topbar, text = "Language Learning APP", font = ("Arial", 25), bg=topbar_colour)
        self.title_.grid(row=0, column=1, sticky="nsew")
        

        self.main = tk.Frame(self)
        self.main.pack(fill = tk.BOTH, side = tk.BOTTOM, expand=True)
        self.main.rowconfigure(0, weight=1)
        self.main.columnconfigure(0, weight=1)
        
        self.home = Home(self.main)
        
        self.database = Database(self.main)
        #self.tran_only.tkraise() #change to home section
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.sidebar = Sidebar(self)
        self.sidebar_click = 0
        
        self.home.tkraise()
        self.mainloop()
        
    def tran_only_mode(self):
        if self.database_check() != []:    #NEED TO CHECK THIS WARNING WORKS AND ADD WARNING WHEN REFRESH QUIZ
            self.tran_only = Pages(self.main, "tran_only")
            self.tran_only.content.page2.tkraise()
            self.sidebar.home_btn2.configure(command = lambda: [self.sidebar.highlight(2), self.tran_only.tkraise()])
        else:
            tk.messagebox.showerror("ERROR", "Database is empty. Put data in before using quizes")
    def pic_only_mode(self):
        if self.database_check() != []:
            self.pic_only = Pages(self.main, "pic_only")
            self.pic_only.content.page2.tkraise()
            self.sidebar.home_btn3.configure(command = lambda: [self.sidebar.highlight(3), self.pic_only.tkraise()])
        else:
            tk.messagebox.showerror("ERROR", "Database is empty. Put data in before using quizes")
        
    def sidebar_change(self):
        if self.sidebar_click == 0:
            #self.sidebar.place(x=0, y=44, width=115, height= (parent.winfo_height())-44, anchor = "nw")
            self.sidebar.place(x=0, y=0, width=115, relheight= 1, anchor = "nw")
            self.topbar.tkraise()
            self.sidebar.focus_force()
            self.sidebar_click = 1
        else:
            self.sidebar.place(x=0, y=44, width=115, relheight= 1, anchor = "ne")
            self.sidebar_click = 0
    
    def database_check(self):    #implement method into Quiz maybe? Check every restart 
        conn = sqlite3.connect("french.db")
        c = conn.cursor()
        c.execute("""SELECT * FROM french""")
        return(c.fetchone())
    
class Home(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.welcome = tk.Label(self, text="W E L C O M E")
        self.welcome.pack(fill=tk.BOTH, expand=True)
        
class Languages(tk.Frame):
    def __init__(self, parent, color):
        tk.Frame.__init__(self, parent, bg=color)
        langs = self.query_col()
        
        self.language1 = tk.StringVar()
        self.language1.set("english")
        self.language2 = tk.StringVar()
        self.language2.set("french")
        
        self.right_btn = ttk.Combobox(self, state="readonly", width=7, textvariable= self.language2)
        self.right_btn["values"] = langs
        self.right_btn.current(1)
        self.right_btn.pack(side = tk.RIGHT, fill = tk.Y, expand = True)
        self.left_btn = ttk.Combobox(self, state="readonly", width=7, textvariable= self.language1)
        self.left_btn["values"] = langs
        self.left_btn.current(0)
        self.left_btn.pack(side = tk.LEFT, fill = tk.Y, expand=True)
        self.arrow = tk.Label(self, text = "Translate to", bg="lightgrey")
        self.arrow.pack(side = tk.LEFT, fill=tk.BOTH, expand = True)
        
    def query_col(self):
        conn=sqlite3.connect("french.db")
        c = conn.cursor()
        c.execute("""PRAGMA table_info(french);
                 """
           )
        result = c.fetchall()
        #print(result)
        conn.commit()
        conn.close()
        #try to make col the right size before storing info (data allocation) instead of appending
        col = np.zeros((len(result)-3))
        col = list(col.astype(str))
        #result = result[4:]
        for i,j in enumerate(result[3:]):
            #col[i[0]-3] = i[1]
            col[i] = j[1].capitalize()
        
        self.col = col
        return self.col
     
        
class Sidebar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.configure(bg="black")        
        self.top=tk.Frame(self, height=topbar_height, bg="blue")
        self.bottom=tk.Frame(self, bg="pink")
        self.top.pack(side=tk.TOP, fill=tk.X)
        self.bottom.pack(expand=True, fill=tk.BOTH)
        self.place(x=0, width=parent.menu.winfo_width(), relheight=1, anchor = "ne")
        #self.home_btn1 = tk.Button(self.bottom, text="HOME", command = lambda: [self.highlight(1)])
        self.home_btn1 = tk.Button(self.bottom, text="HOME", command = lambda: [self.highlight(1), parent.home.tkraise()]) 
        self.home_btn2 = tk.Button(self.bottom, text="TRANSLATE ONLY", command = lambda: [self.highlight(2), parent.tran_only_mode()]) #Add function to check the language pairs will not give all nulls in question method
        self.home_btn3 = tk.Button(self.bottom, text="PICTURES ONLY", command = lambda: [self.highlight(3), parent.pic_only_mode()])
        self.home_btn4 = tk.Button(self.bottom, text="DATABASE", command = lambda: [self.highlight(4), parent.database.tkraise()])
        
        self.home_btn1.pack(side=tk.TOP, fill=tk.X)
        self.home_btn2.pack(side=tk.TOP, fill=tk.X)
        self.home_btn3.pack(side=tk.TOP, fill=tk.X)
        self.home_btn4.pack(side=tk.TOP, fill=tk.X)
        
        
        self.btn_dict = {1:self.home_btn1,
                         2:self.home_btn2,
                         3:self.home_btn3,
                         4:self.home_btn4}
        self.indicator = 0
        
    #Function creates highlighting on selected mode. Make a cleaner and mor efficient function if possible.           
    def highlight(self,indicator):
        if self.indicator != indicator:
            if self.indicator in list(range(1,6)):
                self.btn_dict[self.indicator].configure(bg="SystemButtonFace")
            if indicator in list(range(1,6)):
                self.btn_dict[indicator].configure(bg="darkgrey")
            self.indicator=indicator

    
class Pages(tk.Frame):
    def __init__(self, parent, opt):
        tk.Frame.__init__(self, parent)
        #self.language1 = parent.language1
        #self.language2 = parent.language2
        self.grid(row=0, column=0, sticky="nsew")
        #self.rowconfigure(0, weight=1)
        #self.columnconfigure(0, weight=1)
        
        self.language_bar = tk.Frame(self)
        self.language_bar.pack(side=tk.TOP, fill=tk.X, pady=5)
        self.content = tk.Frame(self)
        self.content.pack(fill=tk.BOTH, expand=True)
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)
        
        self.refresh = tk.Button(self.language_bar, text= "Refresh?", command = lambda:[self.content.page2.tkraise(),self.content.page2.questions(self.content.page1.picked)])
        self.refresh.pack(side=tk.RIGHT)
        self.languages = Languages(self.language_bar, "grey")
        self.languages.pack(side=tk.RIGHT, fill=tk.Y)
        self.content.language1 = self.languages.language1
        self.content.language2 = self.languages.language2   
        self.content.page4 = Completed(self.content)
        self.content.page1 = Categories(self.content)
        if opt == "tran_only":
            self.content.page2 = Q_translate(self.content)
        if opt == "pic_only":
            self.content.page2 = Q_picture(self.content)
            self.languages.left_btn.destroy()
            self.languages.arrow.destroy()
        self.content.page3 = Judge(self.content, False)
        self.current_page = 0
        #self.page2.tkraise()

        
        
class Categories(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky = "nsew")
        self.placeholder_btns = tk.Frame(self)
        self.placeholder_btns.pack(side=tk.BOTTOM, fill=tk.X)
        self.placeholder_box = tk.Frame(self)
        self.placeholder_box.pack(fill=tk.BOTH)
        self.placeholder_box.columnconfigure([0,1,2,3,4], weight=1, uniform="a")
        
        
        self.btns = tk.Frame(self.placeholder_btns)
        self.btns.pack(side=tk.BOTTOM, fill=tk.X)
        #Incorporate raising previous page with cancel button- use vectors and dot product

        self.btns.rowconfigure(0, weight=1)
        self.btns.columnconfigure([0, 1, 2], weight=1, uniform="a")
        self.cat_btn = tk.Button(self.btns, text="Cancel", width=20, command = lambda: self.cancel(parent))
        self.sub_btn = tk.Button(self.btns, text="Apply Changes", width = 20, command = lambda: [parent.page2.questions(self.selected()),parent.page2.tkraise()])
        self.sub_btn.grid(row=0, column=1)
        self.cat_btn.grid(row=0, column=2, sticky="se", padx=10, pady=10)
        self.cat_list = self.categories()
        self.checkbox_init(self.cat_list)
        self.selected()
        
    def checkbox_init(self, categories):
        self.checkboxes_live = {}
        self.variables_live = {}
        column=0
        row=0
        
        #Don't need to index i to get element of tuple, interesting... 
        for i in categories:
            self.variables_live[i] = tk.IntVar()
            self.variables_live[i].set(1)
            self.checkboxes_live[i] = tk.Checkbutton(self.placeholder_box, text = i, bg="pink", variable = self.variables_live[i])
            self.checkboxes_live[i].bind("<Button-1>", self.untick)
            if column>4:
                column=0
                row+=1
            self.checkboxes_live[i].grid(row=row, column=column, pady=20)
            column+=1
            
    
    def untick(self, event):
        for i in self.variables_live:    
            if self.variables_live[i].get() == 1:
                self.checkboxes_live[i].config(activebackground = "red")
            else:
                self.checkboxes_live[i].config(activebackground = "limegreen")
                
    def cancel(self,parent):
        if parent.current_page == 2:
            parent.page2.tkraise()
        elif parent.current_page == 3:
            parent.page3.tkraise()
            
    def categories(self):
        conn = sqlite3.connect("french.db")
        c = conn.cursor()
        c.execute("""SELECT DISTINCT category
                  FROM french;""")
        category = c.fetchall()
        #print(category)
        conn.commit()
        conn.close()
        
        return category
    
    def selected(self):
        self.picked = []
        for i in self.cat_list:
            if self.variables_live[i].get()==1:
                self.picked.append(i[0])
                
        return self.picked
            


        
        
class Quiz(tk.Frame):
    def __init__(self, parent):
        #self.questions(parent.page1.picked)
        #random.shuffle(self.Q)
        #self.Q_iter = iter(self.Q)
        tk.Frame.__init__(self, parent)
        
        #self.language1 = parent.language1
        #self.language2 = parent.language2
        
        self.grid(row=0, column=0, sticky="nsew")
        #Format this page for the appropriate mode and then implement question randomisation and storing the answers
        
        self.btns = tk.Frame(self)
        self.btns.pack(side=tk.BOTTOM, fill=tk.X)
        self.btns.rowconfigure(0, weight=1)
        self.btns.columnconfigure([0, 1, 2], weight=1, uniform="a")
        self.cat_btn = tk.Button(self.btns, text="Categories", width=20, command = lambda: self.cat_btn_command(parent))
        self.sub_btn = tk.Button(self.btns, text="Submit", width = 20, command = lambda: [self.check(parent), parent.page3.tkraise(), self.string.set(""), self.next_question(parent)])
        #self.sub_btn.bind(<"Return">, self.sub_click)
        self.sub_btn.grid(row=0, column=1)
        self.cat_btn.grid(row=0, column=2, sticky="se", padx=10, pady=10)
        
        self.symbols = tk.Frame(self)
        self.symbols.pack(side=tk.BOTTOM)
        self.char_list = ["\u0300", "\u0301", "\u0303", "\u0304", "\u0305", "\u0306", "\u0307"]
        self.accent_btns(self.char_list)
        
        self.string = tk.StringVar()
        self.input_ans = tk.Entry(self,textvariable = self.string)
        self.input_ans.pack(side=tk.BOTTOM)

        
    def check(self, parent):
        print(self.current)
        if " ".join(self.string.get().split()) ==  self.current[1]:    #Removes all extra whitespace
            print("correct")
            parent.page3.correct.tkraise()
            
        else:
            print("incorrect")
            parent.page3.wrong.tkraise()
            
    def accent_btns(self,char_list):
         self.btns = {}
         self.strings = {}
         column=0
         row=0
         for i in char_list:
             self.btns[i] = tk.Button(self.symbols, text=i, font=(20),anchor="s", width=2, command=lambda i=i: self.add_accent(i))
             self.btns[i].grid(row=row, column=column)
             column += 1

    def add_accent(self, char):
        a = self.string.get()
        self.string.set(a+char)
        self.input_ans.icursor(len(a)+1)
        
    def cat_btn_command(self,parent):
        parent.page1.tkraise()
        parent.current_page = 2

class Q_translate(Quiz):
    def __init__(self, parent):
        Quiz.__init__(self, parent)
        self.parent=parent
        self.prompt = tk.Label(self, text="Translate this", justify="center")
        self.prompt.pack(side=tk.TOP, fill=tk.X, pady=20)
                   
        self.question = tk.Label(self, font=("arial", 30), justify="center")
        self.question.pack(side=tk.TOP, fill=tk.X)
        self.questions(parent.page1.picked)
        
    def questions(self, options):
        query = """SELECT """ + self.parent.language1.get().lower() + """,""" + self.parent.language2.get().lower() + """ FROM french WHERE category IN ("""
        for i in range(len(options)):
            query += """?,"""
        query = query[:-1] + """) AND """ + self.parent.language1.get().lower() + """ IS NOT NULL AND """ + self.parent.language2.get().lower() + """ IS NOT NULL"""
        print(query)
            
        conn = sqlite3.connect('french.db')
        c = conn.cursor()
        c.execute(query, (options))
        self.Q = c.fetchall()
        if len(self.Q) != 0: 
            random.shuffle(self.Q)
            self.Q_iter = iter(self.Q)
            self.current = next(self.Q_iter)
            self.question.configure(text = self.current[0])
        else:
            tk.messagebox.showerror("ERROR", "The language pair has no translations between eachother. Please choose another language pair or add relevant translations in Database.")
        conn.commit()
        conn.close()
        
        #return Q
    
    def next_question(self, parent):
        try:
            self.current = next(self.Q_iter)
            self.question.configure(text=(self.current[0]))
        except StopIteration:
            parent.page3.correct.sub_btn.configure(command= parent.page4.tkraise)
            parent.page3.wrong.sub_btn.configure(command= parent.page4.tkraise)
            
    def restart(self):
        random.shuffle(self.Q)
        self.Q_iter = iter(self.Q)
        self.current = next(self.Q_iter)
        self.question.configure(text=(self.current[0]))
        
        
class Q_picture(Quiz):
    def __init__(self, parent):
        Quiz.__init__(self, parent)
        self.parent = parent
        self.prompt = tk.Label(self, text="What is this? ", justify="center")
        self.prompt.pack(side=tk.TOP, fill=tk.X, pady=20)
                  
        self.question = tk.Label(self, font=("arial", 30), justify="center")
        self.question.pack(side=tk.TOP, fill=tk.BOTH, expand=True, ipadx=10, ipady=10)
        self.questions(parent.page1.picked)
        
    def questions(self, options):
        query = """SELECT """+ self.parent.language2.get().lower() + """, image_path FROM french WHERE category IN ("""
        for i in range(len(options)):
            query += """?,"""
        query = query[:-1] + """) AND image_path IS NOT NULL AND """ + self.parent.language2.get().lower() + """ IS NOT NULL"""  #Only need one language_.get().lower()
        print(query)                                        #query filters out rows with no image paths, so error isn't raised
            
        conn = sqlite3.connect('french.db')
        c = conn.cursor()
        c.execute(query, (options))
        self.Q = c.fetchall()
        if len(self.Q) != 0:
            random.shuffle(self.Q)
            self.Q_iter = iter(self.Q)
            print(self.Q)
            self.current = next(self.Q_iter)
            self.display_image()
        else:
            tk.messagebox.showerror("ERROR", "The language pair has no translations between eachother. Please choose another language pair or add relevant image paths into Database.")
            self.parent.page4.tkraise()
        conn.commit()
        conn.close()
        
        #return Q
    
    def check(self, parent):
        print(self.current)
        if " ".join(self.string.get().split()) ==  self.current[0]:    #Removes all extra whitespace
            print("correct")
            parent.page3.correct.tkraise()
            
        else:
            print("incorrect")
            parent.page3.wrong.tkraise()
    
    def next_question(self, parent):
        try:
            self.current = next(self.Q_iter)
            self.display_image()
        except StopIteration:
            parent.page3.correct.sub_btn.configure(command= parent.page4.tkraise)
            parent.page3.wrong.sub_btn.configure(command= parent.page4.tkraise)
            
    def restart(self):
        random.shuffle(self.Q)
        self.Q_iter = iter(self.Q)
        self.current = next(self.Q_iter)
        self.display_image()

    def display_image(self):
        image = Image.open(self.current[1])
        image.thumbnail((300,300), Image.Resampling.LANCZOS)
        self.image= ImageTk.PhotoImage(image)
        self.question.configure(image = self.image)
    

class Judge(tk.Frame):
    def __init__(self, parent, good):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.correct = Judge_correct(self, parent)
        self.wrong = Judge_wrong(self, parent)
 
    def cat_btn_command(self,parent):
        parent.page1.tkraise()
        parent.current_page = 3
        
    def btns(self, root, grandparent):
        self.btns = tk.Frame(root)
        self.btns.pack(side=tk.BOTTOM, fill=tk.X)
        self.btns.rowconfigure(0, weight=1)
        self.btns.columnconfigure([0, 1, 2], weight=1, uniform="a")
        self.cat_btn = tk.Button(self.btns, text="Categories", width=20, command = lambda: self.cat_btn_command(grandparent))
        self.sub_btn = tk.Button(self.btns, text="Next Question", width = 20, command = grandparent.page2.tkraise)
        self.sub_btn.grid(row=0, column=1)
        self.cat_btn.grid(row=0, column=2, sticky="se", padx=10, pady=10)
        
class Judge_correct(Judge):
    def __init__(self, parent, grandparent):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.configure(bg="green")
        self.congrats = tk.Label(self, text="Congratulations! You are correct.", font=("arial", 35))
        self.congrats.pack(expand=True)
        self.btns(self, grandparent)
    
class Judge_wrong(Judge):
    def __init__(self, parent, grandparent):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.configure(bg="red")
        self.disappoint = tk.Label(self, text="Wrong. It's okay, you'll do better.", font=("arial", 35))
        self.disappoint.pack(expand=True)
        self.btns(self, grandparent)

        
class Completed(tk.Frame):
    def __init__ (self, parent):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.complete = tk.Label(self, text = "C O M P L E T E D", font= ("arial", 45))
        self.complete.pack(expand=True)
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.BOTTOM)
        self.restart_btn = tk.Button(self.frame, text = "Restart?", width=20, command= lambda: [parent.page2.restart(), self.command_change(parent), parent.page2.tkraise()])
        self.restart_btn.pack(side = tk.LEFT, pady=10, padx=5)
        
    def command_change(self, parent):
        parent.page3.correct.sub_btn.configure(command= parent.page2.tkraise)
        parent.page3.wrong.sub_btn.configure(command= parent.page2.tkraise)
        
class Database(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.list = tk.Frame(self, width = 900, height = 250)   
        self.list.pack_propagate(0)                             #stops self.list frame from resizing according to its children widgets
        self.input=tk.Frame(self)
        self.symbols = tk.Frame(self)
        
        self.list.pack()
        self.input.pack()
        self.symbols.pack(pady=10)
        
        self.scrollbar_v = tk.Scrollbar(self.list, bg="black")
        self.scrollbar_h = tk.Scrollbar(self.list, bg="black", orient = "horizontal")
        self.scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
        self.treeview()
        
        self.input.rowconfigure([0,1], weight=1, uniform="a")
        self.input.columnconfigure([0,1,2], weight=1, uniform="z")
        
        self.add_btn = tk.Button(self.input, text="Add Data", command=self.addition)
        self.add_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.add_lang_btn = tk.Button(self.input, text="Add Language", command=self.add_language)
        self.add_lang_btn.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.ren_lang_btn = tk.Button(self.input, text="Rename Language", command=self.rename_language)
        self.ren_lang_btn.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.del_lang_btn =  tk.Button(self.input, text="Delete Language", command=self.delete_language)
        self.del_lang_btn.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        #self.symbols.columnconfigure(0, )
        char_list = ["\u0300", "\u0301", "\u0303", "\u0304", "\u0305", "\u0306", "\u0307"]
        self.accent_btns(char_list)
        #self.accents = tk.Button(self.symbols, text="\u0300 ", width=2, command=lambda: self.add_accent("\u0300"))
        #self.accents.pack()
        self.cat_combobox = tk.StringVar() #For category combobox in Modify class, keeps memory of last stored category
        

    def treeview(self):
        columns = self.query_col()+["Category", "Image Path", "id"]
        self.tree = ttk.Treeview(self.list, column=columns, show="headings")
        self.heading_names = {}
        for i in columns:
            self.tree.heading(i, text=i.capitalize())
        for i in self.all_data():
            display = i[3:]+i[:3]
            self.tree.insert("", tk.END, values = display)
        
        self.tree.bind("<Delete>", self.delete)
        self.tree.bind("<Double-1>", lambda event: self.modify())
        self.tree.config(yscrollcommand = self.scrollbar_v.set)
        self.tree.config(xscrollcommand = self.scrollbar_h.set)
        self.scrollbar_v.config(command = self.tree.yview)
        self.scrollbar_h.config(command = self.tree.xview)
        self.tree.pack(pady=10, padx=10, expand=True)

        
    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for j in self.all_data():
            display = j[3:]+j[:3]
            self.tree.insert("", tk.END, values=display)
    #def current_box(self,event):
        
    def accent_btns(self,char_list):
        self.btns = {}
        self.strings = {}
        column=0
        row=0
        for i in char_list:
            self.btns[i] = tk.Button(self.symbols, text=i, font=(20),anchor="s", width=2, command=lambda i=i: self.add_accent(i))
            self.btns[i].grid(row=row, column=column)
            column += 1
        
    
    

    def add_accent(self, char):
        if self.current_box == 1:
            self.string = self.string1
            self.data = self.data1
        elif self.current_box == 2:
            self.string = self.string2
            self.data = self.data2
        elif self.current_box == 3:
            self.string=self.string3
            self.data = self.cat_data
            
        a = self.string.get()
        self.string.set(a+char)
        print(char)
        self.data.icursor(len(a)+1)
        
    def query_col(self):
        conn=sqlite3.connect("french.db")
        c = conn.cursor()
        c.execute("""PRAGMA table_info(french);
                 """
           )
        result = c.fetchall()
        #print(result)
        conn.commit()
        conn.close()
        #try to make col the right size before storing info (data allocation) instead of appending
        col = np.zeros((len(result)-3))
        col = list(col.astype(str))
        #result = result[4:]
        for i,j in enumerate(result[3:]):
            #col[i[0]-3] = i[1]
            col[i] = j[1]
        
        self.col = col
        self.result = result[3][0]
        return self.col
     
    def all_data(self):
        conn = sqlite3.connect("french.db")
        c = conn.cursor()
        c.execute("""SELECT * FROM french""")
        all = c.fetchall()
        print(all)
        conn.commit()
        conn.close()
        return all
    
    def delete(self,event):
        s = self.tree.selection()
        query = """DELETE FROM french 
                   WHERE id in ("""
        for i in s:
            query += str(self.tree.item(i)["values"][-1])+","
            self.tree.delete(i)
        query = query[:-1] +""");"""
        conn=sqlite3.connect("french.db")
        c=conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()
        
    def addition(self):
        self.dialogue = Dialogue(self)
        
    def modify(self):
        self.mod = Modify(self)
        
    def add_language(self):
        self.add_lang = Add_language(self)
        #print(self.cat_combobox.get())
        
    def delete_language(self):
        self.del_lang = Delete_language(self)
        
    def rename_language(self):
        ren_lang=Rename_language(self)
        

class Dialogue(tk.simpledialog.Dialog):
    def __init__(self, parent):
        self.columns = parent.query_col()             #Why did I have to put this before the init of parent class??
        self.parent = parent        
        tk.simpledialog.Dialog.__init__(self, parent) #It's because the init uses the body function so need to define self.columns = query_cols() first, otherwise when called
        self.current_page = "null"                                            #it would be undefined
 
        
    
    def body(self, parent):
        self.labels={}
        self.entries={}
        self.inputs={}
        for i,j in enumerate(self.columns):
            self.inputs[j] = tk.StringVar()
            self.labels[j] = tk.Label(parent, text=j.capitalize()+":")
            self.labels[j].grid(row=i, column=0)
            self.entries[j] = tk.Entry(parent, textvariable=self.inputs[j])
            self.entries[j].grid(row=i, column=1)
            self.entries[j].bind("<Button-1>", lambda event, j=j: self.current_ent(j))
        self.inputs["category"] =  tk.StringVar()
        self.inputs["category"].set(self.parent.cat_combobox.get())
        self.labels["category"] = tk.Label(parent, text = "Category:")
        self.labels["category"].grid(row=i+1, column=0)
        self.entries["category"]= ttk.Combobox(parent, textvariable = self.inputs["category"], values= self.categories())
        self.entries["category"].grid(row=i+1, column=1)
        self.entries["category"].bind("<Button-1>", lambda event: self.current_ent("category"))
        self.inputs["image_path"] = tk.StringVar()
        self.labels["image_path"] = tk.Label(parent, text = "Image path:")
        self.labels["image_path"].grid(row=i+2, column=0)
        self.entries["image_path"]=tk.Entry(parent, textvariable = self.inputs["image_path"])
        self.entries["image_path"].grid(row=i+2, column=1)
        self.entries["image_path"].bind("<Button-1>", lambda event: self.current_ent("image_path"))
        
        self.accents = tk.Frame(parent)
        self.accents.grid(row=i+3, column=0, columnspan=2)
        char_list = ["\u0300", "\u0301", "\u0303", "\u0304", "\u0305", "\u0306", "\u0307"]
        self.accent_btns(char_list)


    def add_data(self):   
        #print(self.parent.cat_combobox.get())                          
        query_start = """INSERT INTO french("""
        query_end = """ VALUES ("""
        values = []
        for i in (self.columns + ["category", "image_path"]):
            val = self.inputs[i].get()
            print(val)
            if len(val) != 0:
                query_start += i + ""","""
                query_end += """?,""" 
                values.append(val)
        query = query_start[:-1] + """)""" + query_end[:-1] + """);""" 
        print(query)
        conn = sqlite3.connect("french.db")
        c = conn.cursor()
        try:
            c.execute(query,values)
        except sqlite3.OperationalError:
            print("All values are null")
            tk.messagebox.showerror("ERROR", "All values are null")       #Shows error when all fields are empty
        except sqlite3.IntegrityError:                                    #Shows error message when NOT NULL constraint of SQL table is breached (in our case this is category)
            print("category field cannot be empty")
            tk.messagebox.showerror("ERROR", "Category field cannot be empty")
        conn.commit()
        conn.close()
        
        self.parent.cat_combobox.set(self.inputs["category"].get()) #Stores the category in parent instance if category added to database
        
        
    def buttonbox(self):        
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=lambda: [self.ok(),self.add_data(), self.parent.update_treeview()], default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()
    
    def categories(self):
        conn = sqlite3.connect("french.db")
        c = conn.cursor()
        c.execute("""SELECT DISTINCT category
                  FROM french;""")
        category = c.fetchall()
        #print(category)
        conn.commit()
        conn.close()
        return category
    
    def accent_btns(self,char_list):
        self.btns = {}
        self.strings = {}
        column=0
        row=0
        for i in char_list:
            self.btns[i] = tk.Button(self.accents, text=i, font=(5), anchor="s", width=2, command=lambda i=i: self.add_accent(i))
            self.btns[i].grid(row=row, column=column)
            column += 1
    

    def add_accent(self, char):
        self.string = self.inputs[self.current_entry]
        self.entry = self.entries[self.current_entry]
        a = self.string.get()
        self.string.set(a+char)
        self.entry.icursor(len(a)+1)
            
    def current_ent(self, ind):
        self.current_entry = ind
        print(self.current_entry)
        
    
class Modify(tk.simpledialog.Dialog):              #Comment and document this whole class its a mess also rename to better variable names
    def __init__(self, parent):
        self.columns = parent.query_col() + ["category", "image_path"]
        self.s = parent.tree.selection()
        self.s_cols = parent.tree.item(self.s)["values"]
        self.id = parent.tree.item(self.s)["values"][-1]
        self.parent=parent
        tk.simpledialog.Dialog.__init__(self, parent)
        
    def body(self, parent):
        self.labels={}
        self.entries={}
        self.inputs={}
        for i,j in enumerate(self.columns):
            self.inputs[j] = tk.StringVar()
            self.inputs[j].set(self.s_cols[i])
            self.labels[j] = tk.Label(parent, text=j+":")
            self.labels[j].grid(row=i, column=0)
            self.entries[j] = tk.Entry(parent, textvariable=self.inputs[j])
            self.entries[j].grid(row=i, column=1)
            
    def add_data(self):
        list = []
        list_att = []
        for i,j in enumerate(self.columns):
            new_input = " ".join(self.inputs[j].get().split())
            old_input = " ".join(self.s_cols[i].split())               #Shouldn't need to do this as all tree values will be formatting this way anyways
            print(new_input)
            print(old_input)
            #old_input = """" """ + self.s_cols[i] + """" """
            #old_input = old_input[:1] + old_input[2:-1]
            if new_input != self.s_cols[i]:
                list_att.append(j)
                list.append(new_input)
        query = """UPDATE french SET """
        for i in range(len(list)):
            if list[i] != "": 
                query += list_att[i] + """ = ?,"""
            else:
                query += list_att[i] + """ = NULL,"""
                list.pop(i)
            
        query = query[:-1]
        query += """ WHERE id=?;"""
        list.append(self.id)
        print(query, list)
        
        conn = sqlite3.connect("french.db")
        c = conn.cursor()
        c.execute(query, list)
        conn.commit()
        conn.close()
        
    def buttonbox(self):        
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=lambda: [self.ok(),self.add_data(), self.parent.update_treeview()], default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

class Add_language(tk.simpledialog.Dialog):
    def __init__(self, parent):
        tk.simpledialog.Dialog.__init__(self, parent)
        self.parent = parent
    
    def body(self,master):        
        self.entry_frame = tk.Frame(master)
        self.entry_frame.pack(side=tk.TOP, fill=tk.X)
        self.entry_frame.columnconfigure([0,1], weight=1)
        self.count = 0
        self.strings = {self.count: tk.StringVar()}
        self.entries = {self.count: tk.Entry(self.entry_frame, textvariable= self.strings[self.count])}
        self.entries[self.count].grid(row=0, column=0)
        self.entries[0].update()
        self.bin = icon_to_image("trash", scale_to_height = self.entries[0].winfo_height()-5)   #Bin icon for delete button
        another_frame = tk.Frame(master)
        another_frame.pack(side=tk.TOP, fill=tk.X)
        another_btn = tk.Button(another_frame, text="Add another language", command= self.add_another)
        another_btn.grid(row=0, column=0, sticky = "w", pady=10)
        
        #sub_btn = tk.Button(master, text="Confirm additions")
        #sub_btn.pack(side=tk.BOTTOM)
    
    def add_another(self):
        self.count += 1
        i=self.count
        self.strings[self.count] = tk.StringVar()
        self.entries[self.count] = [tk.Entry(self.entry_frame, textvariable= self.strings[self.count]), tk.Button(self.entry_frame, image = self.bin, command = lambda i=i: self.delete(i))]
        self.entries[self.count][0].grid(row=self.count, column=0)
        self.entries[self.count][1].grid(row=self.count, column=1)
        
    def delete(self, index):
        self.entries[index][0].destroy()
        self.entries[index][1].destroy()
        
    def add_data(self):
        query_start = """ALTER TABLE french 
                   ADD """ 
        #for key in self.strings:
        #    query += self.strings[key].get() + """ VARCHAR(255), """
        #query = query[:-2]
        #print(query)
        
        conn = sqlite3.connect("french.db")
        c = conn.cursor()
        for key in self.strings:
            if self.strings[key].get().split() != []:      #shows as [] if string is empty or only contains white spaces
                query = query_start + self.strings[key].get() + """ VARCHAR(255);"""
                c.execute(query)
        conn.commit()
        conn.close()
        
    def buttonbox(self):         
        box = tk.Frame(self)

        w = tk.Button(box, text="Confirm", width=10, justify=tk.LEFT, command=lambda: [self.ok(), self.add_data(), self.parent.tree.destroy(), self.parent.treeview()], default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        
        box.pack()
     
class Rename_language(tk.simpledialog.Dialog):
    def __init__(self, parent):
        self.languages = parent.query_col()
        self.parent=parent
        tk.simpledialog.Dialog.__init__(self, parent)
        
    def body(self, master):
        self.input = tk.Frame(master)
        self.input.pack(side=tk.TOP, fill=tk.X)
        self.input.columnconfigure([0, 1], weight=1, uniform="a")
        self.chosen = tk.StringVar()
        self.new = tk.StringVar()
        self.cat_combobox = ttk.Combobox(self.input, textvariable = self.chosen, values=self.languages)
        self.cat_combobox.grid(row=0, column=0)
        self.entry = tk.Entry(self.input, textvariable=self.new)
        self.entry.grid(row=0, column=1)
        
                
    def ren_data(self):
        query = """ALTER TABLE french
                   RENAME COLUMN """ + self.chosen.get() + """ TO """ + self.new.get()
        print(query)

        conn = sqlite3.connect("french.db")
        c =conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()
            
    def buttonbox(self):         
        box = tk.Frame(self)

        w = tk.Button(box, text="Confirm", width=10, justify=tk.LEFT, command=lambda: [self.ok(), self.ren_data(), self.parent.tree.destroy(), self.parent.treeview()], default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        
        box.pack()    
        
     
        
class Delete_language(tk.simpledialog.Dialog): #Rename self.cats?
    def __init__(self, parent):
        self.languages = parent.query_col()
        self.parent=parent
        tk.simpledialog.Dialog.__init__(self, parent)
        
    def body(self, master):
        master.columnconfigure([0,1,2,3,4], weight=1, uniform="y")
        row=0
        column=0
        self.values = {}
        self.cats = {}
        for i in self.languages:
            self.values[i] = tk.IntVar() 
            self.cats[i] = tk.Checkbutton(master, text=i, variable = self.values[i])
            self.cats[i].grid(row=row, column=column)
            column += 1 
            if column==4:
                row+=1
                column=0
                
    def del_data(self):
        query_start = """ALTER TABLE french
                         DROP COLUMN """
        query = []
        tick_count = 0
        for i in self.cats:
            if self.values[i].get() == 1:
                query.append(query_start + i.lower())     #Change append method to different algorithm?
                tick_count += 1
        
        if len(self.cats)-tick_count < 2:
            tk.messagebox.showerror("ERROR", "Need to keep atleast 2 langauges")
        else:
            conn = sqlite3.connect("french.db")
            c =conn.cursor()
            for i in query:
                c.execute(i)
            conn.commit()
            conn.close()
            
    def buttonbox(self):         
        '''add standard button box.
    
        override if you do not want the standard buttons
        '''
    
        box = tk.Frame(self)

        w = tk.Button(box, text="Confirm", width=10, justify=tk.LEFT, command=lambda: [self.ok(), self.del_data(), self.parent.tree.destroy(), self.parent.treeview()], default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        
        box.pack()    
        
    
root = initialise()
#root.tran_only.content.page2.input_ans.focus_force()
#root.home.tkraise()
#root.mainloop()


#conn=sqlite3.connect("french.db")
#c=conn.cursor()
#c.execute("""DROP TABLE french""")
#c.execute("""CREATE TABLE french(
#              category VARCHAR(100) NOT NULL,
#             image_path VARCHAR(100),          
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             english VARCHAR(100),
#             french VARCHAR(100),
#             gujrati VARCHAR(100),
#             hindi VARCHAR(100));""")
#c.execute("""INSERT INTO french(english, french, category) VALUES("A dog","Un chien", "Animals")""")
#conn.commit()
#conn.close()
