# -*- coding: iso-8859-1 -*-
from Tkinter import *
from tkFileDialog import asksaveasfilename
import sys

def Median(x):
    return sorted(x)[len(x) / 2]

def SD(x, mu):
    sum = 0
    for i in x:
        sum = sum + (i - mu) * (i - mu)
    sum = sum / float(len(x))
    sd = sum ** (1 / 2.0)
    
    return sd

def roundDigits(digit, d):
    values = str(digit).split(".")
    if(len(values) > 1):
        newdigit = str(values[0]) + "." + str(values[1])[0:2]
    else:
        newdigit = digit
    return newdigit
    
class AllTkinterWidgets:
    
    def __init__(self, master, values, seq_ids, n_values, max_n_content, win_values, min_win_size, ok, quit, merged_blocks, show, set_id_A, block_export_file_path=None, db_file=None, density_table=None):
        
        try:
            set_id_A = set_id_A.split("_win_")[1]
            shift_len = int(set_id_A.split("_shift_")[0])
            anno_table = "anno_" + str(density_table.split("_")[1])
            
            elementKeys = []
            for seq_id in seq_ids:
                elementKeys.append(seq_id)
            
            values3 = []
    
            assert(len(values) == len(n_values))

            for elementKey in elementKeys:
                valuesList = values.get(elementKey)
                n_valuesList = n_values.get(elementKey)
                win_valuesList = win_values.get(elementKey)
                for i in range(0, len(valuesList)):
                    if(float(n_valuesList[i]) <= float(max_n_content) and float(win_valuesList[i]) >= float(min_win_size) * float(win_valuesList[0]) / 100.0):
                        values3.append(valuesList[i])
                values[elementKey] = values3
                values3 = []
                
            self.csv1 = ""
            self.tab1 = ""
            
            self.quit = quit
            self.ok = ok
            
            try:
                vscrollbar = AutoScrollbar(master)
                vscrollbar.grid(row=0, column=1, sticky=N + S)
                hscrollbar = AutoScrollbar(master, orient=HORIZONTAL)
                hscrollbar.grid(row=1, column=0, sticky=E + W)
                
                canvas = Canvas(master,
                                yscrollcommand=vscrollbar.set,
                                xscrollcommand=hscrollbar.set)
                canvas.grid(row=0, column=0, sticky=N + S + E + W)
                
                vscrollbar.config(command=canvas.yview)
                hscrollbar.config(command=canvas.xview)
                
                # make the canvas expandable
                master.grid_rowconfigure(0, weight=1)
                master.grid_columnconfigure(0, weight=1)
                
                master["width"] = 500
                frame = Frame(canvas, bd=1, bg="white", width=500)
                frame.rowconfigure(1, weight=1)
                frame.columnconfigure(1, weight=1)
            except Exception:
                pass
            
            elementKeys.append("ALL")
            
            labelfont3 = ('Courier New', 10)
            labelfont = ('Courier New', 10, 'bold')
            labelfont2 = ('Courier New', 10, 'italic') 
            
            self.tab1 = "LABEL\tMINIMUM\tMAXIMUM\tAVERAGE\tMEDIAN\n"
            self.csv1 = "LABEL;MINIMUM;MAXIMUM;AVERAGE;MEDIAN\n"
             
            try:
                l = Label(frame, text="LABEL", relief=FLAT, bg="white")
                l.grid(row=0, column=0, sticky=W)
                l.config(font=labelfont)   
                    
                l = Label(frame, text="MINIMUM", relief=FLAT, bg="white")
                l.grid(row=0, column=1, sticky=W)
                l.config(font=labelfont)   
                    
                l = Label(frame, text="MAXIMUM", relief=FLAT, bg="white")
                l.grid(row=0, column=2, sticky=W)
                l.config(font=labelfont)   
                    
                l = Label(frame, text="AVERAGE", relief=FLAT, bg="white")
                l.grid(row=0, column=3, sticky=W)
                l.config(font=labelfont)   
                   
                l = Label(frame, text="MEDIAN", relief=FLAT, bg="white")
                l.grid(row=0, column=4, sticky=W)
                l.config(font=labelfont)   
            except Exception:
                pass
            
            i = 1
                
            allElements = []
            for elementKey in elementKeys:
                    
                    values2 = values.get(elementKey)
                    
                    if(values2 != None and len(values2) > 0):
                        for cElement in values2:
                            allElements.append(cElement)
                        color = "white"
                    else:
                        if(values2 == None):
                            values2 = allElements
                            color = "yellow"
    
                    if(values2 != None and len(values2) > 0):
                        try:
                            l = Label(frame, text=elementKey, relief=FLAT, bg=color)
                            l.config(font=labelfont2)   
                            l.grid(row=i, column=0, sticky=W)
                        except Exception:
                            pass
                        self.tab1 = self.tab1 + elementKey
                        self.csv1 = self.csv1 + elementKey
                    
                        try:                            
                            l = Label(frame, text=((roundDigits(min(values2), 2))), relief=FLAT, bg=color)
                            l.grid(row=i, column=1, sticky=W)
                            l.config(font=labelfont3)   
                        except Exception:
                            pass
                        self.tab1 = self.tab1 + "\t" + roundDigits(min(values2), 2)
                        self.csv1 = self.csv1 + ";" + roundDigits(min(values2), 2)
                        
                        try:
                            l = Label(frame, text=((roundDigits(max(values2), 2))), relief=FLAT, bg=color)
                            l.grid(row=i, column=2, sticky=W)
                            l.config(font=labelfont3)   
                        except Exception:
                            pass
                        self.tab1 = self.tab1 + "\t" + roundDigits(max(values2), 2)
                        self.csv1 = self.csv1 + ";" + roundDigits(max(values2), 2)
        
                        mu = sum(values2) / float(len(values2))
                        try:
                            l = Label(frame, text=(roundDigits((mu), 2)), relief=FLAT, bg=color)
                            l.grid(row=i, column=3, sticky=W)
                            l.config(font=labelfont3)   
                        except Exception:
                            pass
                        self.tab1 = self.tab1 + "\t" + roundDigits((mu), 2)
                        self.csv1 = self.csv1 + ";" + roundDigits((mu), 2)

                        try:        
                            l = Label(frame, text=(roundDigits(Median(values2), 2)), relief=FLAT, bg=color)
                            l.grid(row=i, column=4, sticky=W)
                            l.config(font=labelfont3)   
                        except Exception:
                            pass
                        self.tab1 = self.tab1 + "\t" + roundDigits(Median(values2), 2) + "\n"
                        self.csv1 = self.csv1 + ";" + roundDigits(Median(values2), 2) + "\n"
            
                        i = i + 1

            try:            
                l = Label(frame, text="", relief=FLAT, bg="white")
                l.grid(row=i + 1, column=0, sticky=W)
        
                l = Label(frame, text="", relief=FLAT, bg="white")
                l.grid(row=i + 2, column=0, sticky=W)
            except Exception:
                pass

            i = i + 2
            
            self.tab2 = ""
            self.csv2 = ""
            
            show_merged_blocks = False
            
            for key in merged_blocks.keys():
                if(len(merged_blocks[key]) > 0):
                    show_merged_blocks = True

            self.stat_vars = []
                                    
            if(show_merged_blocks == True):
                if(len(merged_blocks) > 0):
                    try:
                        l = Label(frame, text="SEQ_ID", relief=FLAT, bg="white")
                        l.grid(row=i, column=0, sticky=W)
                        l.config(font=labelfont)   
                    except Exception:
                        pass
                    self.tab1 = self.tab1 + "SEQ_ID\tSTART\tSTOP\tLENGTH\tINTENSITY_AVG_MERGED_BLOCK\tINTENSITY_AVG_BLOCKS\tAREA_MERGED_BLOCKS\tAREA_BLOCKS\tCOVERAGE_OF_LONGEST_BLOCK_IN_PERC\tCOVERAGE_ALL_BLOCKS_IN_PERC\n"
                    self.csv1 = self.csv1 + "SEQ_ID;START;STOP;LENGTH;INTENSITY_AVG_MERGED_BLOCK;INTENSITY_AVG_BLOCKS;AREA_MERGED_BLOCKS;AREA_BLOCKS;COVERAGE_OF_LONGEST_BLOCK_IN_PERC;COVERAGE_ALL_BLOCKS_IN_PERC\n"
        
                    try:                        
                        l = Label(frame, text="START", relief=FLAT, bg="white")
                        l.grid(row=i, column=1, sticky=W)
                        l.config(font=labelfont)   
                            
                        l = Label(frame, text="STOP", relief=FLAT, bg="white")
                        l.grid(row=i, column=2, sticky=W)
                        l.config(font=labelfont)   
                        
                        l = Label(frame, text="LENGTH", relief=FLAT, bg="white")
                        l.grid(row=i, column=3, sticky=W)
                        l.config(font=labelfont)   
                        
                        l = Label(frame, text="INTENSITY_AVG_MERGED_BLOCK", relief=FLAT, bg="white")
                        l.grid(row=i, column=4, sticky=W)
                        l.config(font=labelfont)   
    
                        l = Label(frame, text="INTENSITY_AVG_BLOCKS", relief=FLAT, bg="white")
                        l.grid(row=i, column=6, sticky=W)
                        l.config(font=labelfont)   
    
                        l = Label(frame, text="AREA_MERGED_BLOCKS", relief=FLAT, bg="white")
                        l.grid(row=i, column=5, sticky=W)
                        l.config(font=labelfont)   
    
                        l = Label(frame, text="AREA_BLOCKS", relief=FLAT, bg="white")
                        l.grid(row=i, column=6, sticky=W)
                        l.config(font=labelfont)   
    
                        l = Label(frame, text="COVERAGE_OF_LONGEST_BLOCK_IN_PERC", relief=FLAT, bg="white")
                        l.grid(row=i, column=7, sticky=W)
                        l.config(font=labelfont)   
    
                        l = Label(frame, text="COVERAGE_ALL_BLOCKS_IN_PERC", relief=FLAT, bg="white")
                        l.grid(row=i, column=8, sticky=W)
                        l.config(font=labelfont)   
                    except Exception:
                        pass

                    element_keys = merged_blocks.keys()
                    element_keys.sort()
                    
                    
                    i = i + 1
                
                extracted_seq_ids = ""
                
                for key in element_keys:
                    elements = merged_blocks[key]
                    
                    for j in range(0, len(elements)):
                        
                        elements[j]["left"] = (elements[j]["left"] * shift_len) / 1000000.0
                        elements[j]["right"] = (elements[j]["right"] * shift_len) / 1000000.0

                        start = int(float(elements[j]["left"]) * 1000000.0)
                        stop = int(float(elements[j]["right"] + 1) * 1000000.0)
                        anno_id = set_id_A.split("shift__")[1]
                        anno_id = anno_id.replace("_relative", "")
                        import sqlite_methods
                        extracted_seq_ids = extracted_seq_ids + str(anno_table) + "_" + str(start) + "_" + str(stop) + "_" + str(seq_id) + "_" + str(anno_id) + "\n"
                        results = sqlite_methods.extract_seq_ids(db_file, anno_table, str(start), str(stop), seq_id, anno_id)
                        for result in results:
                            extracted_seq_ids = extracted_seq_ids + str(result[0]) + "\n"                  
                    
                        try:                      
                            l = Label(frame, text=(key), relief=FLAT, bg="white")
                            l.grid(row=i, column=0, sticky=W)
                            l.config(font=labelfont2) 
                        except Exception:
                            pass
                        
                        self.csv2 = self.csv2 + str(key)
                        self.tab2 = self.tab2 + str(key)

                        try:                                    
                            l = Label(frame, text=str(elements[j]["left"]), relief=FLAT, bg="white")
                            l.grid(row=i, column=1, sticky=W)
                            l.config(font=labelfont3) 
                        except Exception:
                            pass
                        self.csv2 = self.csv2 + ";" + str(elements[j]["left"])
                        self.tab2 = self.tab2 + "\t" + str(elements[j]["left"])
                                    
                        try:
                            l = Label(frame, text=str(elements[j]["right"]), relief=FLAT, bg="white")
                            l.grid(row=i, column=2, sticky=W)
                            l.config(font=labelfont3) 
                        except Exception:
                            pass
                        self.csv2 = self.csv2 + ";" + str(elements[j]["right"])
                        self.tab2 = self.tab2 + "\t" + str(elements[j]["right"])

                        try:    
                            l = Label(frame, text=str(elements[j]["right"] - elements[j]["left"] + shift_len / 1000000.0), relief=FLAT, bg="white")
                            l.grid(row=i, column=3, sticky=W)
                            l.config(font=labelfont3) 
                        except Exception:
                            pass
                        self.csv2 = self.csv2 + ";" + str(elements[j]["right"] - elements[j]["left"] + shift_len / 1000000.0)
                        self.tab2 = self.tab2 + "\t" + str(elements[j]["right"] - elements[j]["left"] + shift_len / 1000000.0)

                        try:    
                            l = Label(frame, text=str(int(elements[j]["avg"])), relief=FLAT, bg="white")
                            l.grid(row=i, column=4, sticky=W)
                            l.config(font=labelfont3) 
                        except Exception:
                            pass
                        self.csv2 = self.csv2 + ";" + str(int(elements[j]["avg"])) 
                        self.tab2 = self.tab2 + "\t" + str(int(elements[j]["avg"]))

                        try:                        
                            l = Label(frame, text=str(int(elements[j]["avg_rel"])), relief=FLAT, bg="white")
                            l.grid(row=i, column=5, sticky=W)
                            l.config(font=labelfont3) 
                        except Exception:
                            pass
                        self.csv2 = self.csv2 + ";" + str(int(elements[j]["avg_rel"])) 
                        self.tab2 = self.tab2 + "\t" + str(int(elements[j]["avg_rel"]))

                        area = float(elements[j]["avg"]) * (elements[j]["right"] - elements[j]["left"] + shift_len / 1000000.0)
                        try:
                            l = Label(frame, text=str(int(area)), relief=FLAT, bg="white")
                            l.grid(row=i, column=6, sticky=W)
                            l.config(font=labelfont3) 
                        except Exception:
                            pass
                        self.csv2 = self.csv2 + ";" + str(area)
                        self.tab2 = self.tab2 + "\t" + str(area)

                        a = float(elements[j]["all_element_len"])
                        b = (elements[j]["right"] - elements[j]["left"] + shift_len / 1000000.0)
                        c = float(elements[j]["avg_rel"])
                        area2 = a * b * c
                        
                        try:
                            l = Label(frame, text=str(area2), relief=FLAT, bg="white")
                            l.grid(row=i, column=7, sticky=W)
                            l.config(font=labelfont3) 
                        except Exception:
                            pass
                        self.csv2 = self.csv2 + ";" + str(area2)
                        self.tab2 = self.tab2 + "\t" + str(area2)

                        try:
                            l = Label(frame, text=str(int(elements[j]["max_element_len"])), relief=FLAT, bg="white")
                            l.grid(row=i, column=8, sticky=W)
                            l.config(font=labelfont3) 
                        except Exception:
                            pass
                        self.csv2 = self.csv2 + ";" + str(100.0 * float(elements[j]["max_element_len"]))
                        self.tab2 = self.tab2 + "\t" + str(100.0 * float(elements[j]["max_element_len"])) 

                        try:
                            l = Label(frame, text=str(int(elements[j]["all_element_len"])), relief=FLAT, bg="white")
                            l.grid(row=i, column=9, sticky=W)
                            l.config(font=labelfont3) 
                        except Exception:
                            pass
                        self.csv2 = self.csv2 + ";" + str(100.0 * float(elements[j]["all_element_len"])) + "\n" 
                        self.tab2 = self.tab2 + "\t" + str(100.0 * float(elements[j]["all_element_len"])) + "\n"

                        try:
                            var = IntVar()
                            w = Checkbutton(frame, relief=FLAT, bg="white", variable=var)
                            w.grid(row=i, column=10)                
                            self.stat_vars.append(var)
                        except Exception:
                            pass
                        i = i + 1
                    i = i + 1

            def downloadAsTAB(fileName=None):
                try:
                    filetypes = [('TAB', '*.tab')]
                    
                    export_all = True
                    if(fileName == None):
                        export_all = False
                    
                    if(fileName == None):
                        fileName = asksaveasfilename(filetypes=filetypes)
                    
                    fileName = str(fileName).replace(".tab", "")
                    fileName = str(fileName) + ".tab"
                    
                    f = open(fileName, 'w')
                    f.write(self.tab1)

                    var_nmb = self.tab2.split("\n")
                    
                    #print var_nmb
                    
                    try:
                        for i in range(0, len(var_nmb)):
                            f.write(var_nmb[i] + "\n")
                    except Exception:
                        print "downloadAsTAB", sys.exc_info()
                        pass

                    f.close()
                except Exception:
                    print "ERROR", "downloadAsTAB", "Tab Export failed", sys.exc_info()

            def destroyShowSeqs():
                master.destroy()
    
            def downloadAsCSV(fileName=None):
                try:
                    filetypes = [('CSV', '*.csv')]

                    export_all = True
                    if(fileName == None):
                        export_all = False

                    if(fileName == None):
                        fileName = asksaveasfilename(filetypes=filetypes)

                    fileName = str(fileName).replace(".csv", "")
                    fileName = str(fileName) + ".csv"

                    f = open(fileName, 'w')
                    f.write(self.csv1)

                    var_nmb = self.csv2.split("\n")
                    
                    for i in range(0, len(self.stat_vars)):
                        if(self.stat_vars[i].get() == 1 or export_all == True):
                            f.write(var_nmb[i] + "\n")

                    f.close()
                except Exception:
                    print "ERROR", "downloadAsCSV", "CSV Export failed", sys.exc_info()
                    
            def destroyShowSeqs():
                master.destroy()
                
            def extractIds():
                print "INFO", "extractIds", "extracting ids..."
                filetypes = [('TXT', '*.txt')]
                fileName = asksaveasfilename(filetypes=filetypes)
                f = open(fileName, "w")
                f.write(extracted_seq_ids)
                f.close()
                          
            try:  
                l = Button(frame, text="CSV", command=downloadAsCSV)
                l.grid(row=i + 1, column=1, sticky=W)
                l = Button(frame, text="TAB", command=downloadAsTAB)
                l.grid(row=i + 1, column=2, sticky=W)
                l2 = Button(frame, text="ID", command=extractIds)
                l2.grid(row=i + 1, column=3, sticky=W)
                l3 = Button(frame, image=self.quit, command=destroyShowSeqs)
                l3.grid(row=i + 1, column=4, sticky=W)

            except Exception:
                #print "ERROR", "statistics_window", sys.exc_info()
                pass

            try:
                canvas.create_window(0, 0, anchor=NW, window=frame)
    
                if(show == True):
                    frame.update_idletasks()
            except Exception:
                pass

            try:               
                canvas.config(scrollregion=canvas.bbox("all"))
            except Exception:
                pass
            
            if(block_export_file_path != None):
                downloadAsTAB(block_export_file_path)

        except Exception:
            print "ERROR", "AllTkinterWidgets", "Statistical information could not be loaded", sys.exc_info()
            
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
