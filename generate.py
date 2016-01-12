from Tkinter import *
import sys
import sqlite_methods

def GenerateHeatmap(self):
        try:
            self.root_heatmap.destroy()
        except Exception:
             pass

        self.root_heatmap = None
        
        if(self.root_heatmap == None):
            self.root_heatmap = Toplevel()
            self.root_heatmap.title("Select SetId for Heatmap Visualisation")
    
            canv = Canvas(self.root_heatmap, bg="white", relief=SUNKEN)
            canv.config(scrollregion=(0, 0, 300, 800))         
            canv.config(highlightthickness=0)    
     
            var1 = StringVar()
            var2 = StringVar()

            def close():
                try:
                    self.root_heatmap.destroy()
                except Exception:
                     pass
                self.root_heatmap = None
                
            def state():
                SetIdList = listbox.get(0, END)
                if(len(listbox.get(0, END)) != 0):
                    index=listbox.curselection()[0]
                    self.SetId.set(listbox.get(index))
                    self.ChangeSetId()
                    self.root_heatmap.destroy()
                    
            frame = Frame(self.root_heatmap, width=500, height=400, bd=1, bg='white')
            frame.pack()
            
            iframe21 = Frame(frame, bd=4, relief=RIDGE)
            t = StringVar()

            listbox = Listbox(iframe21)
            listbox.config(width=80)
            listbox.pack(side=LEFT, padx=5, fill=BOTH)
            
            try:
                for setId in sqlite_methods.getSetIds(self.db_file, self.density_table):

                    foundSeqId = 0
                    
                    for cSeqId in self.seq_ids:
                        if(cSeqId == setId[0]):
                            foundSeqId = 1
                            
                    if(foundSeqId == 0):
                        if(self.SequenceNameMap.get(setId[0]) == None):
                            listbox.insert(END, setId[0])
                        else:
                            listbox.insert(END, self.SequenceNameMap.get(setId[0]))
            except Exception:
                print "ERROR", "GenerateHeatmap", "No set id specified"
                      
            sbar = Scrollbar(iframe21)
            sbar.config(command=listbox.yview)                   
            sbar.pack(side=LEFT, pady=5, fill=BOTH)           
            listbox.config(yscrollcommand=sbar.set)   
            
            iframe21.pack(expand=1, fill=X, pady=10, padx=5)

            
            
            def destroyShowSeqs():
                try:
                    self.root_heatmap.destroy()
                except Exception:
                     pass
                 
                self.root_heatmap = None

            self.quit = PhotoImage(file=self.cwd + '/pix/quit.gif', master=self.root_heatmap)
            self.ok = PhotoImage(file=self.cwd + '/pix/ok.gif', master=self.root_heatmap)
            
            iframe3 = Frame(frame, bd=2, relief=RIDGE)
            button1 = Button(iframe3, image=self.ok, command=state)
            button1.pack(side=RIGHT, padx=5)

            t = StringVar()
            Button(iframe3, image=self.quit, command=destroyShowSeqs).pack(side=RIGHT, padx=5)
            iframe3.pack(expand=1, fill=X, pady=10, padx=5)
            
            self.root_heatmap.mainloop()


def GenerateLinechart(self):
        try:
            self.root_linechart.destroy()
        except Exception:
             pass
         
        self.root_linechart=None

        if(self.root_linechart == None):
            self.root_linechart = Toplevel()
            self.root_linechart.title("Select SetId for Linechart Visualisation")
    
            canv = Canvas(self.root_linechart, bg="white", relief=SUNKEN)
            canv.config(scrollregion=(0, 0, 300, 800))         
            canv.config(highlightthickness=0)    
     
            var1 = StringVar()
            var2 = StringVar()

            def close():
                try:
                    self.root_linechart.destroy()
                except Exception:
                     pass
                self.root_linechart = None
                
            def state():
                SetIdList = listbox.get(0, END)
                if(len(listbox.get(0, END)) != 0):
                    index=listbox.curselection()[0]
                    self.SetId.set(listbox.get(index))
                    self.CreateLineChart()
                    self.root_linechart.destroy()
                
            frame = Frame(self.root_linechart, width=500, height=400, bd=1, bg='white')
            frame.pack()
            
            iframe21 = Frame(frame, bd=4, relief=RIDGE)
            t = StringVar()

            listbox = Listbox(iframe21)
            listbox.config(width=80)
            listbox.pack(side=LEFT, padx=5, fill=BOTH)
            
            try:
                for setId in sqlite_methods.getSetIds(self.db_file, self.density_table):

                    foundSeqId = 0
                    
                    for cSeqId in self.seq_ids:
                        if(cSeqId == setId[0]):
                            foundSeqId = 1
                            
                    if(foundSeqId == 0):
                        if(self.SequenceNameMap.get(setId[0]) == None):
                            listbox.insert(END, setId[0])
                        else:
                            listbox.insert(END, self.SequenceNameMap.get(setId[0]))
            except Exception:
                print "ERROR", "GenerateLinechart", "No set id specified"
                      
            sbar = Scrollbar(iframe21)
            sbar.config(command=listbox.yview)                   
            sbar.pack(side=LEFT, pady=5, fill=BOTH)           
            listbox.config(yscrollcommand=sbar.set)   
            
            iframe21.pack(expand=1, fill=X, pady=10, padx=5)

            
            
            def destroyShowSeqs():
                try:
                    self.root_linechart.destroy()
                except Exception:
                     pass
                 
                self.root_linechart = None

            self.quit = PhotoImage(file=self.cwd + '/pix/quit.gif', master=self.root_linechart)
            self.ok = PhotoImage(file=self.cwd + '/pix/ok.gif', master=self.root_linechart)
            
            iframe3 = Frame(frame, bd=2, relief=RIDGE)
            button1 = Button(iframe3, image=self.ok, command=state)
            button1.pack(side=RIGHT, padx=5)

            t = StringVar()
            Button(iframe3, image=self.quit, command=destroyShowSeqs).pack(side=RIGHT, padx=5)
            iframe3.pack(expand=1, fill=X, pady=10, padx=5)
            
            self.root_linechart.mainloop()

