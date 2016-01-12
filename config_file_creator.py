from Tkinter import *
import data_to_db
from tkFileDialog import askdirectory, askopenfilename, asksaveasfilename
import os
import tkFont

DEFAULT_FONT = {'family':"arial", 'weight':'bold', 'size':12} 
DEFAULT_FONT_2 = {'family':"arial", 'weight':'normal', 'size':8} 

def info_panel(text):
    import tkMessageBox
    tkMessageBox.showinfo("Window Title", text) 

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
    
class ConfigFileCreator(Frame):
    def LCS(self, X, Y):
         m = len(X)
         n = len(Y)
         C = [[0] * (n + 1) for i in range(m + 1)]
         for i in range(1, m + 1):
             for j in range(1, n + 1):
                 if X[i - 1] == Y[j - 1]: 
                     C[i][j] = C[i - 1][j - 1] + 1
                 else:
                     C[i][j] = max(C[i][j - 1], C[i - 1][j])
         lcs_len = C[len(C) - 1][len(C[len(C) - 1]) - 1]
         return lcs_len

    def identical_letter_end(self, element_A, list_B_e):
        min_len_elmn = 0
        
        if(len(element_A) > len(list_B_e)):
            min_len_elmn = len(list_B_e)
        else:
            min_len_elmn = len(element_A)
    
        identical_end_letter = 0
        for i in range(0, min_len_elmn):
            if(list_B_e[len(list_B_e) - i - 1] == element_A[len(element_A) - i - 1]):
                identical_end_letter = identical_end_letter + 1
            else:
                return identical_end_letter
        return 0
    
    def find_max_lcs(self, element_A, list_B):
        lcs_len_max = -1
        element_B = -1
        identical_end_letter_max = -1
        
        for list_B_e in list_B:
            lcs_len_cur = self.LCS(element_A, list_B_e)
            if(lcs_len_cur > lcs_len_max):
                element_B = list_B_e
                lcs_len_max = lcs_len_cur
                identical_end_letter_max = self.identical_letter_end(element_A, list_B_e)
            elif(lcs_len_cur == lcs_len_max):
                identical_end_letter_cur = self.identical_letter_end(element_A, list_B_e)
                if(identical_end_letter_cur > identical_end_letter_max):
                    identical_end_letter_max = identical_end_letter_cur
                    element_B = list_B_e
        return element_B

    def addSequenceIdMapping(self):
        list = self.list_A
        
        self.conf_file_mapping = ""
        
        rownum = 1
        for item in list:
            self.conf_file_mapping = self.conf_file_mapping + "seq_id_orig::seq_id_gff" + "::" + item + "::" + self.bla[rownum - 1].get() + "\n"
            rownum = rownum + 1
        
        self.root2.destroy()
        
        self.export_data(None)

    def shift_size_changed(self, *args):
        self.master.v_win_size.set(int(self.master.v_shift.get()) * 5)
        
    def win_size_changed(self, *args):
        self.master.v_shift.set(int(self.master.v_win_size.get()) / 5)
              
    def sequence_id_mapping(self, list_A, list_B):
        self.root2 = Toplevel()
        self.root2.title("Sequence Id Mapping")
        Label(self.root2, text="Sequence Id Mapping", fg='#006699', font=('Courier New', 20)).grid(row=0, column=0, columnspan=2) 

        vscrollbar = AutoScrollbar(self.root2)
        vscrollbar.grid(row=0, column=1, sticky=N + S)
        hscrollbar = AutoScrollbar(self.root2, orient=HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky=E + W)
        
        canvas = Canvas(self.root2, yscrollcommand=vscrollbar.set,
                        xscrollcommand=hscrollbar.set)
        canvas.grid(row=0, column=0, sticky=N + S + E + W)

        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)
        
        self.root2.grid_rowconfigure(0, weight=1)
        self.root2.grid_columnconfigure(0, weight=1)
            
        frame = Frame(canvas, bd=1)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)
                        
            
        self.list_A = list_A
        
        list = list_A
        rownum = 1 
        colnum = 0 
            
        self.option_entries = []

        for item in list: 
            lbl = Label(frame, text=item) 
            lbl.grid(row=rownum, column=colnum, pady=2, sticky=W) 
            
            self.option_entries.append(StringVar())
            _options = list_B
            _item_selected = self.find_max_lcs(item, _options)
            
            self.option_entries[rownum - 1].set(_item_selected)                   
            w = apply(OptionMenu, (frame, self.option_entries[rownum - 1]) + tuple(_options))
                    
            w.grid(row=rownum, column=colnum + 1, pady=2) 
            rownum += 1 
            colnum = 0 
        
        b = Button(frame, text="OK", command=self.addSequenceIdMapping)
        b.grid(row=rownum, column=colnum)
        
        canvas.create_window(0, 0, anchor=NW, window=frame)

        frame.update_idletasks()
            
        canvas.config(scrollregion=canvas.bbox("all"))
            
        self.root2.mainloop()
        
    def check_seq_id_mapping(self):
        allowed_seq_ids = self.master.allowed_seq_ids.keys()
        self.find_seq_file_seq_ids(self.master.b_seq_file["text"])
        found_seq_ids = self.master.found_seq_ids.keys()
        error_occured = False
        
        seq_ids_not_matched = []
        for allowed_seq_id in allowed_seq_ids:
            try:
                assert(allowed_seq_id in found_seq_ids)
            except AssertionError:
                error_occured = True
                seq_ids_not_matched.append(allowed_seq_id)
            
        if(error_occured == True):
            self.sequence_id_mapping(seq_ids_not_matched, found_seq_ids)
        else:
            self.export_data(None)
        
    def find_seq_file_seq_ids(self): 
        file_path = self.master.v_seq_file.get()
        self.master.found_seq_ids = {}
        f = open(file_path)
        cur_key = ""
        for line in f.readlines():
            line = line.strip()
            if(len(line) > 0 and line[0] == ">"):
                line = line.split(" ")[0]
                line = line[1:]
                self.master.found_seq_ids[line] = 0
                cur_key = line
            else:
                self.master.found_seq_ids[cur_key] = self.master.found_seq_ids[cur_key] + len(line)
        
        if(len(self.master.found_seq_ids.values()) > 0):
            m1 = self.master.o_min_chromosome_length["menu"]
            m1.delete(0, END)
    
            self.master.found_seq_ids["zero"] = 0
            values = self.master.found_seq_ids.values()
            values.sort()
            values.reverse()
            
            self.master.v_min_chromosome_length.set(values[0])
            
            for key in values:
                m1.add_command(label=key, command=lambda v=self.master.v_min_chromosome_length, l=key:v.set(l))
            
            self.master.o_min_chromosome_length["state"] = NORMAL
            self.master.o_min_chromosome_length.update()
                
        f.close()    
        
    def path_exist(self, type):
        
        if(self.master.o21 == None):
            self.find_gff3_types()
        
        for path in self.master.o21:
            paths = path.split(",")
            types = type.split(",")
            not_found = False
            for c_type in types:
                if(not (c_type in paths)):
                    not_found = True
            if(not_found == False):
                return True
        return False
        
    def find_gff3_types(self):
        file_path = self.master.v_gff3.get()
        self.master.allowed_gff3_types = {}
        self.master.allowed_seq_ids = {}
        
        f = open(file_path)
        for line in f.readlines():
            values = str(line).split("\t")

            if(len(values) == 9):
                self.master.allowed_gff3_types[values[2]] = 1
                self.master.allowed_seq_ids[values[0]] = 1

        self.master.o21 = data_to_db.path_possible(file_path)
        
        self.master.o21.sort()
        
    def getDirectory(self):
        filePath = askdirectory()
        return filePath
    
    def getFile(self):
        file = askopenfilename()
        return file
        
    def chooseWorkspaceDirectory(self):
        directory = self.getDirectory()
        if(len(directory) > 0):
            self.master.v_workspace.set(directory)
            
    def chooseConfigExportDirectory(self):
        directory = self.getDirectory()
        if(len(directory) > 0):
            self.master.b_config_export_path.config(text=directory)

    def chooseSeqFileDirectory(self):
        directory = self.getFile()
        if(len(directory) > 0):
            self.master.v_seq_file.set(directory)
            self.master.b_gff3["state"] = NORMAL
            self.find_seq_file_seq_ids()
            
    def GFF3orTabFile(self,file_path):
        file = open(file_path, "r")
        
        nine_column=False
        fasta_format=False
        
        for line in file:
            line = line.strip()
            if(len(line)>0):
                if(line[0]==">"):
                    file.close()
                    return False
                values=line.split("\t")
                if(len(values)==9):
                    file.close()
                    return True
        
    def chooseGff3Directory(self):
        directory = self.getFile()
        if(len(directory) > 0):
            self.master.v_gff3.set(directory)
            self.master.b_gff3["state"] = NORMAL
            if(self.GFF3orTabFile(directory)==True):
                self.changeGff3Directory()
            
    def changeGff3Directory(self):
        self.find_gff3_types()
        self.master.o_gff3_types_1["state"] = NORMAL
         
    def chooseTallymerOutputFilesDirectory(self):
        directory = self.getDirectory()
        if(len(directory) > 0):
            self.master.v_tallymer_output_files_directory.set(directory)
    
    def quit(self):
        print "INFO", "quit", "closing config_file_creator..."
        
    def check_mapping(self, file_path=None):
        if(self.check_data() == True):
            if(self.master.v_b3.get() == 1):
                print "INFO", "check_mapping", "check_seq_id_mapping"
                self.check_seq_id_mapping()
            else:
                self.export_data(file_path)
      
    def check_data(self):
        value2 = self.master.v_b3.get()
        
        if(int(value2) == 1):
            if(len(self.master.v_win_size.get()) == 0):
                print "INFO", "check_data", "win_size not defined"
                info_panel("win_size not defined")
                return False
            if(len(self.master.v_shift.get()) == 0):
                print "INFO", "check_data", "shift not defined"
                info_panel("shift not defined")
                return False
        return True
    
    def export_data(self, export_file_path=None):
        if(export_file_path == None):
            export_file_path = "config_file.txt"
            
        f = open(export_file_path, 'w')

        f.write("# generated with automatisation of chromoWIZ\n")
        f.write("genome_id::" + self.master.v1.get() + "\n")
        f.write("workspace::" + self.master.v_workspace.get() + "\n")
        f.write("seq_file::" + self.master.v_seq_file.get() + "\n")
        value = self.master.v_min_chromosome_length.get()
        value = value.strip()
        f.write("min_chromosome_length::" + value + "\n\n\n")
                
        value1 = self.master.v_b2.get()
        value2 = self.master.v_b3.get()
        if(int(value1) == 1):
            f.write("# data extraction\n")
            f.write("extract_data::yes\n")
     
            for key in self.master.anno_container.keys():
                f.write("gff3_file::" + self.master.anno_container[key]["file"] + "\n")
                f.write("gff3_type::" + self.master.anno_container[key]["type"] + "\n")
                f.write("anno_id::" + key + "\n")
                f.write("\n\n")
 
            if(not(self.master.v_anno_id.get() in self.master.anno_container.keys())):  
                if(len(self.master.v_gff3.get())>0 and len(self.master.v_gff3_types.get())>0 and len(self.master.v_anno_id.get())>0):
                    f.write("gff3_file::" + self.master.v_gff3.get() + "\n")
                    f.write("gff3_type::" + self.master.v_gff3_types.get() + "\n")
                    f.write("anno_id::" + self.master.v_anno_id.get() + "\n\n\n")
            
        if(int(value1) != 1 and int(value2) == 1):
            f.write("anno_id::" + self.master.v_anno_id.get() + "\n\n\n")
        if(int(value2) == 1):
            f.write("# density calculation\n")
            f.write("calc_densities::yes\n")
        if(int(value2) == 1):
            f.write("win_size::" + self.master.v_win_size.get() + "\n")
            f.write("shift::" + self.master.v_shift.get() + "\n")
           
        f.write(self.conf_file_mapping)
        f.close()
        
        info_panel("Export successful!")
        
        self.conf_file_mapping = ""
        
    def gff3_to_anno_table(self):
        value1 = self.master.c_run_gff3_to_anno_table_var.get()
        value2 = self.master.c_run_calculate_densities_var.get()
        value3 = self.master.c_run_tallymer_to_sql_var.get()

        if(int(value1) == 0):
            self.master.o_gff3_types_1["state"] = DISABLED
            if(int(value2) == 0):            
                self.master.e_anno_id["state"] = DISABLED
        else:
            self.master.o_gff3_types_1["state"] = NORMAL
            self.master.e_anno_id["state"] = NORMAL

    def saveFile(self):
        file_path = asksaveasfilename()
        self.check_mapping(file_path)
        
    def openFile(self):
        file_path = askopenfilename()
        
        f = open(file_path)
        cur_key = ""
        
        cur_gff3_file=""
        cur_gff3_types=""
        cur_anno_id=""
        
        for line in f.readlines():
            line = line.strip()
            
            i = line.find("#")
            if(i >= 0):
                line = line[0:i]
                
            if(line.find("extract_data") >= 0):
                value = line.split("::")
                value = value[1].strip()
                try:
                    assert(value == "yes" or value == "no")
                except AssertionError:
                    info_panel("parameter extract_data invalid or missing")
            elif(line.find("calc_densities") >= 0):
                value = line.split("::")
                value = value[1].strip()
                try:
                    assert(value == "yes" or value == "no")
                except AssertionError:
                    info_panel("parameter calc_densities invalid or missing")
            values = line.split("::")
            if(len(values) == 2):
                values[0], values[1]
                key = values[0]
                value = values[1]
                key = key.strip()
                value = value.strip()

                if(key == "genome_id"):
                    self.master.v1.set(value)
                elif(key == "workspace"):
                    self.master.v_workspace.set(value)
                elif(key == "seq_file"):
                    self.master.v_seq_file.set(value)
                elif(key == "gff3_file"):
                    self.master.v_gff3.set(value)
                    cur_gff3_file=value
                    self.master.o_gff3_types_1["state"] = NORMAL
                elif(key == "gff3_type"):
                    self.master.v_gff3_types.set(value)
                    cur_gff3_types=value
                elif(key == "anno_id"):
                    self.master.v_anno_id.set(value)
                    cur_anno_id=value
                elif(key == "win_size"):
                    self.master.v_shift.set(value)
                elif(key == "shift"):
                    self.master.v_shift.set(value)
                elif(key == "min_chromosome_length"):
                    self.master.v_min_chromosome_length.set(value)
                if(len(cur_gff3_file)>0 and len(cur_gff3_types)>0 and len(cur_anno_id)>0):
                    self.add_gff3_annotation()
                    cur_gff3_file=""
                    cur_gff3_types=""
                    cur_anno_id=""

    def prev_anno(self):
        self.master.annotation_map_index = self.master.annotation_map_index - 1
        if(self.master.annotation_map_index >= 0):
            self.master.v6.set(self.master.annotation_map[self.master.annotation_map_index]["anno_id"])
            self.master.v21.set(self.master.annotation_map[self.master.annotation_map_index]["gff3_types"])
            self.master.v_gff3.set(self.master.annotation_map[self.master.annotation_map_index]["gff3_path"])
        if(self.master.annotation_map_index == 0):
            self.master.b_anno_prev["state"] = DISABLED
        else:        
            self.master.b_anno_prev["state"] = NORMAL

        self.master.o_gff3_types_1["state"] = NORMAL
        
    def del_anno(self):
        self.master.v_gff3.set("")
        self.master.v6.set("")
        self.master.v21.set("")
        
        self.master.o_gff3_types_1["state"] = DISABLED
        
    def add_gff3_annotation(self):
        assert(len(self.master.e_gff3.get()) > 0)
        assert(len(self.master.v_gff3_types.get()) > 0)
        assert(len(self.master.e_anno_id.get()) > 0)

        keys = self.master.anno_container.keys()
        if(self.master.e_anno_id.get() in keys):
            print "INFO", "calculation already exists"
        else:
            anno_entry = {}
            anno_entry["type"] = self.master.v_gff3_types.get()
            try:
                assert(self.path_exist(anno_entry["type"]) == True)
                anno_entry["file"] = self.master.e_gff3.get()
                self.master.anno_container[self.master.e_anno_id.get()] = anno_entry
                self.master.listbox_gff3.insert(END, self.master.e_anno_id.get())
                
                self.master.e_gff3.delete(0,END)
                self.master.e_anno_id.delete(0,END)
                self.master.o_gff3_types_1.delete(0,END)
                
            except Exception:
                info_panel("gff3_type tupel not correct")

    def remove_gff3_annotation(self):
        try:
            index_to_delete = self.master.listbox_gff3.curselection()[0]
            element = self.master.listbox_gff3.get(index_to_delete, index_to_delete)
            self.master.anno_container.pop(element[0])
            self.master.listbox_gff3.delete(index_to_delete, index_to_delete)
        except Exception:
            pass
    
    def extract_data(self):
        pass

    def data_to_db(self):
        pass

    def __init__(self, master, master_master):
        
        Frame.__init__(self, master)
        self.master = master
        self.master.anno_container = {}
        self.conf_file_mapping = ""
        
        menubar = Menu(master_master)
        filemenu = Menu(menubar, tearoff=True)

        filemenu.add_command(label="Open", command=self.openFile)
        filemenu.add_command(label="Save", command=self.saveFile)
        filemenu.add_command(label="Quit", command=master_master.destroy) # better than root.quit (at least in IDLE)
        menubar.add_cascade(label="File", menu=filemenu)
        master_master.config(menu=menubar) 
        
        self.master.annotation_map = []
        self.master.annotation_map_index = 0
        
        defaultFont = tkFont.Font(**DEFAULT_FONT)
        defaultFont2 = tkFont.Font(**DEFAULT_FONT_2)
        
        # ********************************************************************************
        
        cur_row = 0

        f = Frame(self)
        self.master.gap = Label(f, text="")
        self.master.gap.grid()
        self.master.v_b1 = StringVar()
        self.master.l_b1 = Label(f, text="general parameters", state=NORMAL, anchor=W, relief=RAISED, font=defaultFont)
        self.master.l_b1.grid(row=cur_row, column=0, columnspan=3, sticky=W) 
        self.master.gap = Label(f, text="")
        self.master.gap.grid()
        f.grid(row=cur_row, column=0, sticky="W")

        cur_row = cur_row + 1
        
        # genome_id
        self.master.l_genome_id = Label(self, text="genome_id", font=defaultFont)
        self.master.l_genome_id.grid(sticky="W", row=cur_row, column=0) 
        self.master.v1 = StringVar()
        self.master.e_genome_id = Entry(self, font=defaultFont, textvariable=self.master.v1, width=30, relief=RIDGE, bg="white")
        self.master.e_genome_id.grid(row=cur_row, column=1, sticky="W") 
        
        cur_row = cur_row + 1
        
        # workspace
        self.master.l_workspace = Label(self, text="workspace", font=defaultFont)
        self.master.l_workspace.grid(sticky="W", row=cur_row, column=0) 
        self.master.l_workspace = StringVar()
        self.master.v_workspace = StringVar()
        self.master.e_workspace = Entry(self, font=defaultFont, textvariable=self.master.v_workspace, width=30, relief=RIDGE, bg="white")
        self.master.e_workspace.grid(row=cur_row, column=1, sticky="W") 
        self.master.b_workspace = Button(self, text="Browse...", font=defaultFont2, command=self.chooseWorkspaceDirectory)
        self.master.b_workspace.grid(row=cur_row, column=2, sticky="W") 

        cur_row = cur_row + 1
        
        # seq_file
        self.master.l_seq_file = Label(self, text="seq_file", font=defaultFont)
        self.master.l_seq_file.grid(sticky="W", row=cur_row, column=0) 
        self.master.v_seq_file = StringVar()
        self.master.e_seq_file = Entry(self, font=defaultFont, textvariable=self.master.v_seq_file, width=30, relief=RIDGE, bg="white")
        self.master.e_seq_file.grid(row=cur_row, column=1, sticky="W") 
        self.master.b_seq_file = Button(self, text="Browse...", font=defaultFont2, command=self.chooseSeqFileDirectory)
        self.master.b_seq_file.grid(row=cur_row, column=2, sticky="W") 

        cur_row = cur_row + 1
        
        # min_chromosome_length
        self.master.l_min_chromosome_length = Label(self, text="min_chromosome_length", font=defaultFont)
        self.master.l_min_chromosome_length.grid(sticky="W", row=cur_row, column=0) 
        self.master.v_min_chromosome_length = StringVar()
        _options = ["---"]
        self.master.v_min_chromosome_length.set(_options[0])
        self.master.o_min_chromosome_length = apply(OptionMenu, (self, self.master.v_min_chromosome_length) + tuple(_options))
        self.master.o_min_chromosome_length["width"] = 10
        self.master.o_min_chromosome_length["relief"] = RIDGE
        self.master.o_min_chromosome_length["bg"] = "white"
        self.master.o_min_chromosome_length.grid(row=cur_row, column=1, sticky="W") 
        self.master.o_min_chromosome_length["state"] = DISABLED
                  
        cur_row = cur_row + 1

        f = Frame(self)
        self.master.gap = Label(f, text="")
        self.master.gap.grid()
        self.master.v_b2 = StringVar()
        self.master.v_b2.set(1)
        self.master.b_b2 = Checkbutton(f, text="extract_data", state=NORMAL, anchor=W, variable=self.master.v_b2, command=self.extract_data, relief=RAISED, font=defaultFont)
        self.master.b_b2.grid(row=cur_row, column=0, columnspan=3, sticky=W) 
        self.master.gap = Label(f, text="")
        self.master.gap.grid()
        f.grid(row=cur_row, column=0, sticky="W")

        #cur_row = cur_row + 1

        # gff3_file/gff3_types/anno_id
        f = Frame(self)
        self.master.l_seq_file = Label(f, text="gff3_file/tab_file", font=defaultFont)
        self.master.l_seq_file.grid(sticky="W") 
        self.master.l_seq_file = Label(f, text="gff3_types/tab_file", font=defaultFont)
        self.master.l_seq_file.grid(sticky="W") 
        self.master.l_seq_file = Label(f, text="anno_id", font=defaultFont)
        self.master.l_seq_file.grid(sticky="W") 
        f.grid(row=cur_row + 3, column=0, sticky="W")
                      
#        cur_row = cur_row + 1
        
        f = Frame(self)
        self.master.v_gff3 = StringVar()
        self.master.e_gff3 = Entry(f, font=defaultFont, textvariable=self.master.v_gff3, width=30, relief=RIDGE, bg="white")
        self.master.e_gff3.grid(row=cur_row, column=2) 
        self.master.b_gff3 = Button(f, text="Browse..", font=defaultFont2, command=self.chooseGff3Directory)
        self.master.b_gff3.grid(row=cur_row, column=1) 
        self.master.v_gff3_types = StringVar()
        self.master.v_gff3_types.set("")
        self.master.o_gff3_types_1 = Entry(f, width=30, textvariable=self.master.v_gff3_types, relief=RIDGE, font=defaultFont, bg="white")
        self.master.o_gff3_types_1.grid(row=cur_row + 1, column=2) 
        self.master.o_gff3_types_1["state"] = DISABLED
        self.master.v_anno_id = StringVar()
        self.master.e_anno_id = Entry(f, font=defaultFont, textvariable=self.master.v_anno_id, width=30, relief=RIDGE, bg="white")
        self.master.e_anno_id.grid(row=cur_row + 2, column=2) 
        f.grid(row=cur_row + 3, column=1, columnspan=2)
        
        f = Frame(self)
        self.b_gff_add = Button(f, text=">>", command=self.add_gff3_annotation, width=1, height=1, relief=RIDGE)
        self.b_gff_add.grid()
        self.b_gff_remove = Button(f, text="X", command=self.remove_gff3_annotation, width=1, height=1, relief=RIDGE)
        self.b_gff_remove.grid()
        f.grid(row=cur_row + 3, column=3)
                    
        self.master.listbox_gff3 = Listbox(self, width=40, height=4, relief=RIDGE, bg="white")
        self.master.listbox_gff3.grid(row=cur_row + 3, column=4, columnspan=4) 

        cur_row = cur_row + 5

        f = Frame(self)
        self.master.gap = Label(f, text="")
        self.master.gap.grid()
        self.master.v_b3 = StringVar()
        self.master.v_b3.set(1)
        self.master.b_b3 = Checkbutton(f, text="data_to_db", state=NORMAL, anchor=W, variable=self.master.v_b3, command=self.data_to_db, relief=RAISED, font=defaultFont)
        self.master.b_b3.grid(row=cur_row, column=0, columnspan=3, sticky=W) 
        self.master.gap = Label(f, text="")
        self.master.gap.grid()
        f.grid(row=cur_row, column=0, sticky="W")

        cur_row = cur_row + 1
          
        # win_size
        self.master.l_win_size = Label(self, text="win_size", font=defaultFont)
        self.master.l_win_size.grid(sticky="W", row=cur_row, column=0) 
        self.master.v_win_size = StringVar()
        _options = ["50000", "100000", "500000", "1000000"]
        self.master.v_win_size.set(_options[0])
        self.master.v_win_size.trace('w', self.win_size_changed)
        self.master.o_win_size = apply(OptionMenu, (self, self.master.v_win_size) + tuple(_options))
        self.master.o_win_size["width"] = 10
        self.master.o_win_size["relief"] = RIDGE
        self.master.o_win_size["bg"] = "white"
        self.master.o_win_size.grid(row=cur_row, column=1, sticky="W") 
    
        cur_row = cur_row + 1
        
        # shift
        self.master.l_shift = Label(self, text="shift", font=defaultFont)
        self.master.l_shift.grid(sticky="W", row=cur_row, column=0) 
        self.master.v_shift = StringVar()
        _options = ["10000", "20000", "100000", "200000"]
        self.master.v_shift.set(_options[0])
        self.master.v_shift.trace('w', self.shift_size_changed)
        self.master.o_shift = apply(OptionMenu, (self, self.master.v_shift) + tuple(_options))
        self.master.o_shift["width"] = 10
        self.master.o_shift["relief"] = RIDGE
        self.master.o_shift["bg"] = "white"
        self.master.o_shift.grid(row=cur_row, column=1, sticky="W") 
        
        self.master.o21 = None

        # ********************************************************************************
                    
                               
class MainFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        master.title("Create Config File")
        self["bg"] = "white"
        
        configFileCreator = ConfigFileCreator(self, master)
        configFileCreator.grid(padx=2, pady=2)
 
        self.pack()

    def quit(self):
        print "INFO", "quit", "closing MainFrame"

def start(show=True):
    root = Tk()
    app = MainFrame(root)
    if(show == True):
        root.mainloop()
tipwindow = None

def createToolTip(widget, text):
    def enter(event):
        global tipwindow
        x = y = 0
        if tipwindow or not text:
            return
        x, y, cx, cy = widget.bbox("insert")
        x += widget.winfo_rootx() + 27
        y += widget.winfo_rooty() + 27
        tipwindow = tw = Toplevel(widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        
        defaultFont = tkFont.Font(**DEFAULT_FONT)
        
        label = Label(tw, text=text, justify=LEFT,
                       background="#ffffe0", relief=RIDGE, font=defaultFont)
        label.pack(ipadx=1)
        
    def close(event):
        global tipwindow
        tw = tipwindow
        tipwindow = None
        if tw:
            tw.destroy()
            
if __name__ == "__main__":
    start()
    
