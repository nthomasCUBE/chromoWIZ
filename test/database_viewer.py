from Tkinter import *
from tkFileDialog import *
import os
import sys

def import_path(fullpath):
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.append(path)
    module = __import__(filename)
    reload(module) 
    del sys.path[-1]
    return module

class AutoScrollbar(Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"
    
class db_viewer:
    def __init__(self, master):
        self.entry_list = []
        self.column_names = []
        self.master = master
        self.content = ""
        self.nmb_pages=-1
        
    def get_tables(self):
        print "INFO", "get_tables"
        file = askopenfilename(parent=self.master, title='Choose a file')
        self.v12.set(str(file))
        self.e12.update()
        sqlite_methods = import_path("../sqlite_methods.py")
        table_names = sqlite_methods.getAllTableNames2(file)
        
        self.options21 = []
        for table_name in table_names:
            self.options21.append(table_name[0])
        self.e22.destroy()
        self.e22 = apply(OptionMenu, (self.master, self.v21) + tuple(self.options21))
        self.e22.grid(row=1, column=1)
        self.e22.update()
    
    def fill_table(self, values, export=False):
        self.nmb_pages=(len(values)+29)/30
        print self.nmb_pages
        self.e43.delete(0,END)
        self.e43.insert(1,self.nmb_pages)
        self.e43["state"]=NORMAL
        
        nmb_entries = len(values)
        nmb_columns = -1

        if(nmb_entries > 0):
            nmb_columns = len(values[0])

        for entry in self.entry_list:
            entry.destroy()
            
        if(export == True):
            self.content = ""

        if(len(self.column_names) > 0):
            for j in range(nmb_columns):
                e = Entry(master=self.master, relief=RIDGE, bg="yellow")
                e.grid(row=5, column=j, sticky=NSEW)
                e.insert(END, self.column_names[j])
                if(export == True):
                    self.content = self.content + str(self.column_names[j]) + "_sep_"
                self.entry_list.append(e)
        
        self.content = self.content + "\n"
        
        for i in range(0, nmb_entries, 1):
            cols = []
            for j in range(nmb_columns):
                try:
                    if(i < 30):
                        e = Entry(master=self.master, relief=RIDGE, bg="white")
                        e.grid(row=i + 6, column=j, sticky=NSEW)
                        self.entry_list.append(e)
                        e.insert(END, values[i][j])
                        cols.append(e)
                    if(export == True):
                        self.content = self.content + str(values[i][j]) + "_sep_"
                except Exception:
                    print sys.exc_info()
            if(i < 30):
                self.rows.append(cols)
            if(export == True):
                self.content = self.content + "\n"
            print "INFO", "fill_table", i, "of", nmb_entries, "elements"

        if(export == True):
            fn = asksaveasfilename(filetypes=[('TAB', '*.tab')])
            f = open(fn, 'w')
            self.content = self.content.replace("_sep_", "\t")
            f.write(self.content)
            f.close()
                        
    def get_column(self):
        sqlite_methods = import_path("../sqlite_methods.py")
        db_file = self.v12.get()
        table_name = self.v21.get()
        columns = sqlite_methods.getAllColumnNames(db_file, table_name)
        self.column_names = []
        for column in columns:
            print "---", column[1]
            self.column_names.append(column[1])
        values = sqlite_methods.getAllValuesFromDatabase(db_file, table_name)

        self.fill_table(values, False)

    def get_column2(self):
        sqlite_methods = import_path("../sqlite_methods.py")
        db_file = self.v12.get()
        table_name = self.v21.get()
        columns = sqlite_methods.getAllColumnNames(db_file, table_name)
        self.column_names = []
        for column in columns:
            print "---", column[1]
            self.column_names.append(column[1])
        values = sqlite_methods.getAllValuesFromDatabase(db_file, table_name)
        self.fill_table(values, True)
          
    def run_sql_command(self):
        sqlite_methods = import_path("../sqlite_methods.py")
        db_file = self.v12.get()
        cmd = self.v42.get()
        values = sqlite_methods.exec_command(db_file, cmd)
        print "values=", values
        self.column_names = []
        self.fill_table(values,True)
         
    def init(self):
        self.rows = []

        if(self.master == None):
            self.master = Canvas(master)
            self.master.grid(row=0, column=0, sticky=N + S + E + W)
            
        # ***************************************************************************
        self.b11 = Label(master=self.master, text='database file')
        self.b11.grid(row=0, column=0)
        self.v12 = StringVar()
        self.e12 = Entry(master=self.master, textvariable=self.v12)
        self.e12.grid(row=0, column=1)
        self.e13 = Button(master=self.master, text="Choose...", command=self.get_tables)
        self.e13.grid(row=0, column=2)
        # ***************************************************************************
        self.b21 = Label(master=self.master, text='table name')
        self.b21.grid(row=1, column=0)
        self.v21 = StringVar(self.master)
        self.v21.set("") 
        self.e22 = OptionMenu(self.master, self.v21, "")
        self.e22.grid(row=1, column=1)
        # ***************************************************************************
        self.b31 = Button(master=self.master, text='Show entries', command=self.get_column)
        self.b31.grid(row=2, column=0)
        self.frame = Frame(master=self.master)
        self.b32 = Button(master=self.frame, text='TAB', command=self.get_column2)
        self.b32.grid(row=0, column=0)
        self.frame.grid(row=2, column=1)
        # ***************************************************************************
        self.b41 = Label(master=self.master, text='sql_command')
        self.b41.grid(row=3, column=0)
        self.v42 = StringVar(self.master)
        self.e42 = Entry(master=self.master, textvariable=self.v42)
        self.e42.config(width=40)
        self.e42.grid(row=3, column=1)
        self.e42 = Button(master=self.master, text="Execute", command=self.run_sql_command)
        self.e42.grid(row=3, column=2)
        self.e43 = Spinbox(master=self.master)
        self.e43["state"] = DISABLED
        self.e43.grid(row=4, column=0)
        self.e44 = Button(master=self.master, text="Show page", command=self.run_sql_command)
        self.e44.grid(row=4, column=1)
        # ***************************************************************************

    def onPress(self):
        for row in self.rows:
            for col in row:
                print col.get(),
            print

master = Tk()
dbv = db_viewer(master)
dbv.init()
master.mainloop()


