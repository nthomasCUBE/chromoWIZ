# -*- coding: utf-8 -*-
from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
from tkColorChooser import askcolor
from tkMessageBox import *
import math
import tkMessageBox
import tkSimpleDialog
import webbrowser
import statistics_window
import sqlite_methods
import calc_vis_elements
import methods
import generate
import sys
import os
import getopt
import tkFont
import redraw
import config_file_creator

##################################
# do not modify this
image_export_possible = True

try:
    sys.path.append("Imaging-1.1.6/build/lib.linux-x86_64-2.7/")
    #sys.path.append("Imaging-1.1.6/PIL")
    import Image
    import ImageDraw
except Exception:
    image_export_possible = False
    print "INFO", "IMAGE and IMAGEDRAW libraries does not exist"
    print "INFO", "Note, that these packages are necessary to produce high quality visualisations"
    print "INFO", "You can download it from:", "http://www.pythonware.com/products/pil/"    
    print ""
    pass
##################################

class DialogFenster2(tkSimpleDialog.Dialog):
    def body(self, master):  
        F1 = Frame(master)
        s = Scrollbar(F1)
        self.L = Listbox(F1)
        self.L.config(width=100)
        
        
        s.pack(side=RIGHT, fill=Y)
        self.L.pack(side=LEFT, fill=Y)
        
        s['command'] = self.L.yview
        self.L['yscrollcommand'] = s.set
        
        for value in self.master.values: 
           self.L.insert(END, value)

        if(len(self.master.values) > 0):
            self.L.selection_set(first=0)
        
        F1.pack(side=TOP)
        
        F2 = Frame(master)
        lab = Label(F2)

        def poll():
            lab.after(200, poll)
            sel = self.L.curselection()
            lab.config(text=str(sel))
            
    def apply(self):  
        if(len(self.L.curselection())):
            self.set_id_a = self.master.values[int(self.L.curselection()[0])]
        pass
    
class DialogFenster(tkSimpleDialog.Dialog):
    def body(self, master):  
        
        self.lab1 = Label(master, text="SQLite DB:", anchor=W)
        self.lab1.grid(row=0, sticky="W")
        
        self.master = master
        
        self.lab2 = Label(master, text="Density Table:")
        self.lab2.grid(row=1)
        
        self.lab3 = Label(master, text="")
        self.lab3.grid(row=2, sticky="W")

        self.e1 = Entry(master)
        self.e2 = Listbox(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        
        self.b1 = Button(master, text="...", command=self.GetDBFile)

        self.b1.grid(row=0, column=2)

        self.dbFile = ""
        self.densityTable = ""
        
        return self.e1
    
    def GetDBFile(self):
        
        filePath = askopenfilename(filetypes=[("Database", "*")])
        self.e1.delete(0, len(self.e1.get()))
        self.e1.insert(0, filePath)
        
        tableNames = sqlite_methods.getTableNames(filePath)

        self.e2.delete(0, END)

        if(len(tableNames) == 0):
            self.lab3.config(text="No density tables available")
        else:
            self.lab3.config(text="")
            
        self.dbFile = filePath
        index = 0
        self.tableNames = tableNames
        
        for tableName in tableNames:
            index = index + 1
            self.e2.insert(index, tableName)

        self.e2.selection_set(first=0)

    def apply(self):  
        
        if(len(self.e2.curselection())):
            self.densityTable = self.tableNames[int(self.e2.curselection()[0])][0]
        else:
            pass
           
class HeatMap:
    def click_1(self, event):
        x = event.x_root
        y = event.y_root
        
        if(len(self.vbar.get()) == 2):
            yadd = (self.psheight + 650) * self.vbar.get()[0]
        
        cur_y = y + yadd
        
        minDistance = None
        cur_position = None
        cDistance = None
        
        for key in self.positionHeatmaps.keys():
            if(minDistance == None):
                minDistance = abs(self.positionHeatmaps.get(key) - cur_y)
                cur_position = key
            else:
                cDistance = abs(self.positionHeatmaps.get(key) - cur_y)
                if(cDistance < minDistance):
                    minDistance = cDistance
                    cur_position = key
        self.cposition = cur_position 
            
        
    def add_canvas(self):
        canvas = Canvas(self.root, bg="white")
    
        self.vbar = Scrollbar(self.root)
        self.hbar = Scrollbar(self.root, orient='horizontal')
    
        self.vbar.pack(side=RIGHT, fill=Y)                 
        self.hbar.pack(side=BOTTOM, fill=X)
        canvas.pack(side=TOP, fill=BOTH, expand=YES)
    
        self.vbar.config(command=canvas.yview)            
        self.hbar.config(command=canvas.xview)
        canvas.config(yscrollcommand=self.vbar.set)   
        canvas.config(xscrollcommand=self.hbar.set)
    
        return canvas

    def searchStepSize(self, max_=None, min_=None, nmb_steps=10):
        max = -1
        min = -1
        if(max_ == None and min_ == None):
            try:
                max = self.scale.get() - self.minV
            except Exception:
                max = self.maxV - self.minV
        else:
            max = int(max_)
            min = int(min_)
            
        amount1 = max / 1
        if(amount1 >= 0 and amount1 < nmb_steps):
            return 1
        else:
            amount5 = max / 5
            if(amount5 >= 0 and amount5 < nmb_steps):
                return 5
            else:
                amount10 = max / 10
                if(amount10 >= 0 and amount10 < nmb_steps):
                    return 10
                else:
                    amount50 = max / 50
                    if(amount50 >= 1 and amount50 <= nmb_steps):
                        return 50            
                    else:
                        amount100 = max / 100
                        if(amount100 >= 1 and amount100 <= nmb_steps):
                            return 100
                        else:
                            amount1000 = max / 1000
                            if(amount1000 >= 1 and amount1000 <= nmb_steps):
                                return 1000
                            else:
                                amount5000 = max / 5000
                                if(amount5000 >= 1 and amount5000 <= nmb_steps):
                                    return 5000
                                else:
                                    amount10000 = max / 10000
                                    if(amount10000 >= 1 and amount10000 <= nmb_steps):
                                        return 10000
                                    else:
                                        amount50000 = max / 50000
                                        if(amount50000 >= 1 and amount50000 <= nmb_steps):
                                            return 50000
                                        else:
                                            amount100000 = max / 100000
                                            if(amount100000 >= 1 and amount100000 <= nmb_steps):
                                                return 100000
                                            else:
                                                amount1000000 = max / 1000000
                                                if(amount1000000 >= 1 and amount1000000 <= nmb_steps):
                                                    return 1000000
                                                else:
                                                    amount5000000 = max / 5000000
                                                    if(amount5000000 >= 1 and amount5000000 <= nmb_steps):
                                                        return 5000000
                                                    else:
                                                        amount10000000 = max / 10000000
                                                        if(amount10000000 >= 1 and amount10000000 <= nmb_steps):
                                                            return 10000000
                                                        else:
                                                            return 20000000
        
    def checkIfSizeIsOk(self, width, height):
        area = width * height
        
        if(width > self.image1Width or height > self.image1Height):
            
            msg = "Current Picture has " + str(height) + "x" + str(width) + " pixel but only " + str(self.image1Height) + "x" + str(self.image1Width) + " are supported\n"
            msg = msg + "Please reduce sequences"
            
            try:
                tkMessageBox.showerror("ERROR", msg)
            except Exception:
                pass
            
            print "ERROR", "checkIfSizeIsOk", msg
            return False
        else:
            return True
        
    def exportGUICanvas(self, filePath=None):
        try:
            filetypes = [('Postscript', '*.ps')]
            if(filePath == None):
                filePath = asksaveasfilename(filetypes=filetypes)
                filePath = str(filePath).strip()
                filePath = str(filePath).replace(".ps", "")
                filePath = str(filePath) + ".ps"

            width = int(self.pswidth) + 250
            height = int(self.psheight) + 300
            self.root.canvas.postscript(file=filePath, height=height, width=width)
        except Exception:
            print "ERROR", "exportGUICanvas failed", sys.exc_info()
            pass
        
    def export(self, filePath=None):
        try:
            filetypes = [('JPEG File Interchange Format', '*.jpeg'), ('Portable Network Graphics', '*.png'), ('Portable Document Format', '*.pdf'), ('Postscript', '*.ps')]
            if(filePath == None):
                filePath = asksaveasfilename(filetypes=filetypes)
                filePath = str(filePath).strip()
            
            width = int(self.pswidthExport) + 250
            height = int(self.psheight) + 300
            
            box = (0, 0, self.fontSizeFactor * (width), self.fontSizeFactor * (height))
            image2 = self.image1.crop(box)
            if(self.checkIfSizeIsOk(self.fontSizeFactor * width, self.fontSizeFactor * height) == True):
                image2.save(filePath)
        except Exception:
            print "ERROR", "export failed", sys.exc_info()
            
            
    def FileOpenMenu(self):
        try:
            NamenDialog = DialogFenster(self.root)
            
            if(len(NamenDialog.dbFile) > 0 and len(NamenDialog.densityTable) > 0):
                self.db_file = NamenDialog.dbFile
                self.density_table = NamenDialog.densityTable
                set_ids = sqlite_methods.getSetIds(self.db_file, self.density_table)
                
                values = []
                for set_id in set_ids:
                    values.append(set_id[0])
                
                self.root.values = values
                
                if(self.canvasDrawn == 0):
                    self.InitializeCanvas()
                    self.canvasDrawn = 1
                else:
                    self.root.canvas.delete('all') 
                    if(self.image_export_possible == True):
                        self.draw.rectangle((0, 0, self.image1Width, self.image1Height), fill="white")
                    self.seq_ids = []

                try:
                    dialogFenster2 = DialogFenster2(self.root)
                    if(len(dialogFenster2.set_id_a)):
                        self.set_id_A = dialogFenster2.set_id_a
                        self.SetId.set(self.set_id_A)
                        self.ChangeSetId()
                except Exception:
                    print "INFO", "FileOpenMenu", "Selecting set_id failed"

                redraw.RedrawHeatmap(self)
                self.createMenu(self.display)
        except Exception:
            print "ERROR", "FileOpenMenu", "Opening database failed"
            
    def showSeqId(self):
        seqIndex = 0
        newSeq_ids = []
        
        for item in self.mySeqList:
            newSeq_ids.append(item)
            seqIndex = seqIndex + 1
        self.seq_ids = newSeq_ids

        if(self.focusOnBarCharts == 1):
            redraw.RedrawBarChart(self, False)
        elif(self.focusOnBarCharts == 0):        
            redraw.RedrawHeatmap(self)
        elif(self.focusOnBarCharts == 2):
            redraw.RedrawStackedHeatmap(self)

    def ChangeFullLength(self):
        if(self.currFullLength != self.FullLength.get()):
            self.currFullLength = self.FullLength.get()
            
            self.maxV = 0
            self.minV = 999999
            
            if(self.focusOnBarCharts == 1):
                redraw.RedrawBarChart(self, False)
            else:  
                if(self.focusOnBarCharts == 0):        
                    redraw.RedrawHeatmap(self)
                else:
                    redraw.RedrawStackedHeatmap(self)
        else:
            print "INFO", "ChangeFullLength", "FullLength has not changed", self.currFullLength, self.FullLength.get()

    def ChangeNContent(self):
        if(int(self.currNContent) != int(self.NContent.get())):
            self.currNContent = self.NContent.get()
            
            self.maxV = 0
            self.minV = 999999
            
            if(self.focusOnBarCharts == 1):
                redraw.RedrawBarChart(self, False)
            else:  
                if(self.focusOnBarCharts == 0):        
                    redraw.RedrawHeatmap(self)
                elif(self.focusOnBarCharts == 2):
                    redraw.RedrawStackedHeatmap(self)

    def ChangeGapBetweenSequences(self):
        self.gapBetweenHeatmaps = self.GapBetweenSequences.get() + self.heatMapSize
        
        if(self.focusOnBarCharts == 1):
            redraw.RedrawBarChart(self, False)
        else:  
            if(self.focusOnBarCharts == 0):        
                redraw.RedrawHeatmap(self)
            else:
                redraw.RedrawStackedHeatmap(self)
            
    def ChangeColor(self):
        (rgb, hexval) = askcolor()
        
        if(hexval != None):
            self.colorToSetIdMap[self.SetId2.get()] = str(hexval).upper()
            self.createMenu(self.display)
            if(self.focusOnBarCharts == 1):
                redraw.RedrawBarChart(self, False)
            
    def ChangeSetId(self, _lineChart=False):
        self.set_id_A = self.SetId.get()
        
        if(self.set_id_A.find("GC_percent") > 0 or
           self.set_id_A.find("TALLYMER") > 0):
            self.button5["state"] = DISABLED
        else:
            self.button5["state"] = NORMAL
            
        self.focusOnBarCharts = 0
        self.ShowConfigFile = True
        self.lineChart = _lineChart
        
        if(self.set_id_A.find("TALLYMER") >= 0):
            self.disablePercentMode = True
            self.disableAbsoluteMode = False
            self.display = "# per Mb"
        else:
            self.disableAbsoluteMode = False
            self.disablePercentMode = False
        
        if(self.set_id_A.find("__GC") >= 0):
            self.disableAbsoluteMode = True
            self.disableShowConfig = True
            self.display = "% bp"
        else:
            self.disableShowConfig = False
            
        self.elementList = {}
        self.NList = {}
        self.WindowLengthList = {}
        
        if(self.root_showSequences != None):
            try:
                self.root_showSequences.destroy()
            except Exception:
                pass                
        if(self.root_renameSequences != None):
            try:
                self.root_renameSequences.destroy()
            except Exception:
                pass

        if(len(self.seq_ids) == 0):
            self.seq_ids = []
            
            seqs = sqlite_methods.getSeqIds(self.db_file, self.density_table, self.set_id_A)
            for seq in seqs:
                self.seq_ids.append(seq[0])
            self.seq_ids = methods.sort_seq_ids(self.seq_ids)
                                 
            self.psheight = self.gapBetweenHeatmaps * (len(self.seq_ids) + 1)

            self.width = 1000
            
            if(len(self.seq_ids) > 0):
                if(self.pswidth < 1000):
                    self.pswidth = 1000
            else:
                self.pswidth = 500
        
            self.ChangeSize()
            
            self.createMenu(self.display)

        self.AddButton()
            
        self.maxV = 0
        self.minV = 999999
        
        self.getMaxValue()
        self.scale["to"] = math.ceil(self.maxV)
        self.scale["from"] = math.ceil(self.minV)

        self.scale.set(self.maxV)
        self.createMenu(self.display)
        redraw.RedrawHeatmap(self)
        
    def ChangeMode(self):
        
        self.elementList = {}
        self.NList = {}
        self.WindowLengthList = {}
        
        if(self.display != self.ModeId.get()):
            
            self.maxV = 0
            self.minV = 999999
            
            self.display = self.ModeId.get()
            
            self.ModeId.set(self.display)
            self.getMaxValue()
  
            if(self.scale != None):
                self.scale["to"] = math.ceil(self.maxV)
                self.scale["from"] = math.ceil(self.minV)

                self.scale.set(self.maxV)
                redraw.RedrawHeatmap(self)
        
        if(self.focusOnBarCharts == 2):
            redraw.RedrawStackedHeatmap(self)
    def Forward(self):
        self.MoveForward()

    def Backward(self):
        self.MoveBackward()
    
    def GetStatistics(self, show=True, block_export_file_path=None):
        
        if(self.focusOnBarCharts == 0):
            try:
                if(self.root_information != None):
                    self.root_information.destroy()
            except Exception:
                pass
            
            try:
                self.root_information = Toplevel()
            except Exception:
                pass
            
            label = "Statistics"

            nContent = 60
            fLength = 20
            ok = None
            quit = None
            try:
                nContent = self.NContent.get()
                fLength = self.FullLength.get()
                ok = self.ok
                quit = self.quit
            except Exception:
                pass
            
            all = statistics_window.AllTkinterWidgets(self.root_information, self.elementList, self.seq_ids, self.NList, nContent, self.WindowLengthList, fLength, ok, quit, self.merged_blocks, show, self.set_id_A, block_export_file_path, self.db_file, self.density_table)
            
            if(show == True):
                
                self.root_information.title(label)
                self.root_information.mainloop()
        
    def getItensity(self, percent, intensityFactor):
        if(self.maxV == 0 or self.maxV == self.minV):
            return 1
        
        if(self.minV!=-1):
            self.minV=0
        elif(percent==-1):
            return -1
        
        intensity = (((percent - self.minV) * 255) / (self.maxV - self.minV)) * (intensityFactor)
        
        if(intensity >= 255):
            return 255

        return intensity

    def getMax2(self, seq_ids=None):
        mode = self.display
        
        NContent = None
        FullLength = None
        try:
            NContent = self.NContent.get()
            FullLength = self.FullLength.get()
        except Exception:
            NContent = 60
            FullLength = 20
        
        if(seq_ids == None):
            seq_ids = self.seq_ids

        
        for seq_id in seq_ids:
            if(self.elementList.get(seq_id) == None):
                self.getMaxValue()
            for countValues in range(0, len(self.elementList.get(seq_id))):
                if(mode == "% bp"):
                    try:
                        if(self.NList[seq_id][countValues] <= NContent and self.WindowLengthList[seq_id][countValues] >= int(FullLength) * int(self.WindowLengthList[seq_id][0]) / 100.0):
                            if(self.maxV < self.elementList[seq_id][countValues]):
                                self.maxV = self.elementList[seq_id][countValues]
                            if(self.minV > self.elementList[seq_id][countValues]):
                                self.minV = self.elementList[seq_id][countValues]
                    except Exception:
                        print "ERROR", "getMax2", "Entry not used"
                        print "ERROR", "getMax2", sys.exc_info()[1]
                else:
                    if(mode == "# per Mb"):
                        try:
                            if(self.NList[seq_id][countValues] <= NContent and self.WindowLengthList[seq_id][countValues] >= int(FullLength) * int(self.WindowLengthList[seq_id][0]) / 100.0):
                                if(self.maxV < self.elementList[seq_id][countValues]):
                                    self.maxV = self.elementList[seq_id][countValues]
                                if(self.minV > self.elementList[seq_id][countValues]):
                                    self.minV = self.elementList[seq_id][countValues]
                        except Exception:
                            print "ERROR", "getMax2", "Entry not used"
                            print "ERROR", "getMax2", sys.exc_info()[1]

    
    def getElementsFromDatabase(self, seq_id, set_id, density_table, db_file, bin_start=None, bin_stop=None):
        values = sqlite_methods.getValuesFromDatabase(db_file, density_table, set_id, seq_id, bin_start, bin_stop)
        #
        elementsList = []
        windowLengthList = []
        nList = []
        
        maxWindowSize = set_id.split("_win")[0]
        
        mode = self.display
        
        countValues = 0
        
        self.NList[seq_id] = []
        self.WindowLengthList[seq_id] = []
        
        for value in values:
            c_length = (int(value[5]))
            windowLengthList.append(c_length)
            nList.append(float(value[10]))
            
            try:
                self.NList[seq_id].append(float(value[10]))
            except Exception:
                print "ERROR", "getElementsFromDatabase", "N values missing for calculations"
                sys.exit()
            try:
                self.WindowLengthList[seq_id].append(int(value[5]))
            except Exception:
                print "ERROR", "getElementsFromDatabase", "WINDOW size not specified"

            if(mode == "% bp"):
                try:
                    nContent = 60
                    fullLength = 20
                    try:
                        nContent = self.NContent.get()
                        fullLength = self.FullLength.get()
                    except Exception:
                        pass
                    if(self.NList[seq_id][countValues] <= nContent and self.WindowLengthList[seq_id][countValues] >= int(fullLength) * int(maxWindowSize) / 100.0):
                        elementsList.append(float(value[9]))
                        if(self.maxV < float(value[9])):
                            self.maxV = float(value[9])
                        if(self.minV > float(value[9])):
                            self.minV = float(value[9])
                    else:
                        elementsList.append(-1)
                except Exception:
                    print "INFO", "getElementsFromDatabase", sys.exc_info()
                    sys.exit()
            else:
                if(mode == "# per Mb"):
                    try:
                        
                        nContent = 60
                        fullLength = 20
                        try:
                            nContent = self.NContent.get()
                            fullLength = self.FullLength.get()
                        except Exception:
                            pass
                        if(self.NList[seq_id][countValues] <= nContent and self.WindowLengthList[seq_id][countValues] >= int(fullLength) * int(maxWindowSize) / 100.0):
                            elementsList.append(float(value[7]))
                            if(self.maxV < float(value[7])):
                                self.maxV = float(value[7])
                            if(self.minV > float(value[7])):
                                self.minV = float(value[7])
                        else:
				elementsList.append(-1);
                    except Exception:
                        print "ERROR", "getElementsFromDatabase", sys.exc_info()
                        sys.exit()
            countValues = countValues + 1
        return (elementsList, windowLengthList, nList)
    
    def getMaxValue(self):
        mode = self.display
            
        for seq_id in self.seq_ids:
            if(self.elementList.get(seq_id) == None):
                elements = self.getElementsFromDatabase(seq_id, self.set_id_A, self.density_table, self.db_file)[0]
                self.elementList[seq_id] = elements
                
    def AdaptMaxLabelSize(self):
        try:
            if(self.focusOnBarCharts == 2 or self.focusOnBarCharts == 0):
                self.maxLabelSize = 0
                self.maxLabelSizeExport = 0
                for seq_id in self.seq_ids:
                    if(len(self.anno_ids) == 0):
                        if(self.SequenceNameMap.get(seq_id) != None):
                            if(((len(self.SequenceNameMap.get(seq_id)) + 1) * self.guiFontSizeSetid) > self.maxLabelSize):
                                self.maxLabelSize = (len(self.SequenceNameMap.get(seq_id)) + 1) * self.guiFontSizeSetid
                        else:
                            if(((len(seq_id) + 1) * self.guiFontSizeSetid) > self.maxLabelSize):
                                self.maxLabelSize = (len(seq_id) + 1) * self.guiFontSizeSetid
                    for anno_id in self.anno_ids:
                        anno_id = str(anno_id).split("__")[1]
                        if(self.SequenceNameMap.get(seq_id) != None):
                            if((len(anno_id) + 1 + len(self.SequenceNameMap.get(seq_id))) * self.fontSize > self.maxLabelSize): # 1 because of additional whitespace
                                self.maxLabelSize = (len(anno_id) + 1 + len(self.SequenceNameMap.get(seq_id))) * self.guiFontSizeSetid
                                self.maxLabelSizeExport = (len(anno_id) + 1 + len(self.SequenceNameMap.get(seq_id))) * self.fontSizeSetId
                        elif(((len(anno_id) + 1 + len(seq_id))) * self.fontSize > self.maxLabelSize):
                                self.maxLabelSize = (len(anno_id) + 1 + len(seq_id)) * self.guiFontSizeSetid
                                self.maxLabelSizeExport = (len(anno_id) + 1 + len(seq_id)) * self.fontSizeSetId
            else:
                self.maxLabelSize = 0
                self.maxLabelSizeExport = 0
                for seq_id in self.seq_ids:
                    if(self.SequenceNameMap.get(seq_id) != None):
                        if((len(self.SequenceNameMap.get(seq_id)) * self.fontSize) > self.maxLabelSize):
                            self.maxLabelSize = len(self.SequenceNameMap.get(seq_id)) * self.guiFontSizeSetid
                            self.maxLabelSizeExport = len(self.SequenceNameMap.get(seq_id)) * self.fontSizeSetId
                    elif(((len(seq_id)) * self.fontSize) > self.maxLabelSize):
                        self.maxLabelSize = (len(seq_id)) * self.guiFontSizeSetid
                        self.maxLabelSizeExport = (len(seq_id)) * self.fontSizeSetId
        except Exception:
            print "ERROR", "AdaptMaxLabelSize", "AdaptMaxLabelSize failed"
    
    def ChangeSize(self):
        try:
	        size = str(int(self.pswidth) + 250) + "x" + str(int(self.psheight))
	        size = str(int(self.pswidth) + 250) + "x" + str(int(self.psheight))
	        self.root.geometry(size)
	
	        self.root.canvas.config(width=self.pswidth + 250, height=self.psheight)                
	        self.root.canvas.config(scrollregion=(0, 0, self.pswidth + 2000, self.psheight + 1000))         
	        self.root.canvas.config(highlightthickness=0)    
        except Exception:
	        self.setFullScreen()
        
    def onPress(self, i):                       
        self.mySeqList[i] = not self.mySeqList[i]   
        
    def find_min_max(self, elements):
        max = elements[0]
        min = elements[0]
        for element in elements:
            if(float(element) > max):
                max = element
            if(float(element) < min):
                min = float(element)
        return min, max
            
    def calculateMinAndMax(self):
        for anno_id in self.anno_ids:
            minV = None
            maxV = None
            
            seq_id_list = []
            
            for seq_id in self.seq_ids:
                
                elements = []
                windowLengthList = []
                nList = []
                
                seq_id_list.append(seq_id + "_" + anno_id)
                
                if(self.elementList.get(seq_id + "_" + anno_id) == None):
                    (elements, windowLengthList, nList) = self.getElementsFromDatabase(seq_id, anno_id, self.density_table, self.db_file)
                else:
                    elements = self.elementList.get(seq_id + "_" + anno_id)
                    windowLengthList = self.WindowLengthList.get(seq_id + "_" + anno_id)
                    nList = self.NList.get(seq_id + "_" + anno_id)
                
                self.elementList[seq_id + "_" + anno_id] = elements
                self.NList[seq_id + "_" + anno_id] = nList
                self.WindowLengthList[seq_id + "_" + anno_id] = windowLengthList

                if(minV == None):
                    (minV, maxV) = self.find_min_max(elements)
                else:
                    (minE, maxE) = self.find_min_max(elements)

                    if(minV > minE):
                        minV = minE
                    if(maxV < maxE):
                        maxV = maxE
            if(self.anno_ids_mItensities.get(anno_id) == None):
                self.anno_ids_mItensities[anno_id] = {}

            self.getMax2(seq_id_list)
            self.anno_ids_mItensities[anno_id]["min"] = minV
            if(minV==-1):
           	 self.anno_ids_mItensities[anno_id]["min"] = 0
            self.anno_ids_mItensities[anno_id]["max"] = maxV
            
            seq_id_list = []
            self.maxV = 0
            self.minV = 999999

    def CreateRootSelectMaxIntensity(self):
        try:
            self.root_chooseMaximumIntensities.destroy()
        except Exception:
             pass
         
        self.root_chooseMaximumIntensities = None
        
        if(self.root_chooseMaximumIntensities == None):
            self.root_chooseMaximumIntensities = Toplevel()
            self.root_chooseMaximumIntensities.title("Choose maximum intensities for genomic elements")
            
            self.scales = []
    
            for i in range(0, len(self.anno_ids)):
                F1 = Frame(self.root_chooseMaximumIntensities, relief=SUNKEN, bd=3)
                
                self.calculateMinAndMax()
                
                self.label = Label(F1)
                self.label.config(text=self.anno_ids[i])
                self.label.pack()
                
                minV = self.anno_ids_mItensities[self.anno_ids[i]]["min"]
                maxV = self.anno_ids_mItensities[self.anno_ids[i]]["max"]
                
                self.control = Scale(F1, from_=int(math.floor(minV)), to=int(math.ceil(maxV)), length=500, orient=HORIZONTAL, showvalue=True, bg="white")
                self.control.pack()
                
                self.scales.append(self.control)
    
                F1.pack()
            F2 = Frame(self.root_chooseMaximumIntensities, relief=SUNKEN, bd=0)

            def close():
                try:
                    self.root_chooseMaximumIntensities.destroy()
                except Exception:
                    pass
                
            def state():
                assert(len(self.scales) == len(self.anno_ids))

                i = 0
                for scale in self.scales:
                    self.anno_ids_mItensities[self.anno_ids[i]]["cur"] = (scale.get())
                    
                    i = i + 1
                    
                pass
            
                redraw.RedrawStackedHeatmap(self)
    
            button1 = Button(F2, image=self.ok, command=state)
            button1.pack(side=RIGHT, padx=5)
    
            button1 = Button(F2, image=self.quit, command=close)
            button1.pack(side=RIGHT, padx=5)
            
            F2.pack()
        
    def GenerateStackedHeatmap(self):
        try:
            self.root_selectSetIdsAndSeqIds.destroy()
        except Exception:
             pass
         
        self.root_selectSetIdsAndSeqIds = None
        
        if(self.root_selectSetIdsAndSeqIds == None):
            self.root_selectSetIdsAndSeqIds = Toplevel()
            self.root_selectSetIdsAndSeqIds.title("Select SetIds for Stacked Heatmaps")
    
            canv = Canvas(self.root_selectSetIdsAndSeqIds, bg="white", relief=SUNKEN)
            canv.config(scrollregion=(0, 0, 300, 800))         
            canv.config(highlightthickness=0)    
     
            var1 = StringVar()
            var2 = StringVar()

            def close():
                try:
                    self.root_selectSetIdsAndSeqIds.destroy()
                except Exception:
                     pass
                self.root_selectSetIdsAndSeqIds = None
                
            def state():
                self.focusOnBarCharts = 2

                anno_ids = listbox2.get(0, END)
                
                if(len(anno_ids) > 0):
                    self.anno_ids = anno_ids
                    self.set_id_A = anno_ids[0]
                    
                    self.createMenu(self.display)
                    redraw.RedrawStackedHeatmap(self)
                    self.ChangeSize()
                    
                    close()
                            
            def List1ToList2():
                if(listbox2.selection_get() != None and
                   len(listbox2.curselection()) > 0):
                    values = listbox2.selection_get().split("\n")
                    indexes = listbox2.curselection()
                    for i in range(0, len(indexes)):
                        listbox.insert(END, values[i])
                        listbox2.delete(indexes[len(indexes) - 1 - i], indexes[len(indexes) - 1 - i])
                
            def List2ToList1():
                if(listbox.selection_get() != None and
                   len(listbox.curselection()) > 0):
                    values = listbox.selection_get().split("\n")
                    indexes = listbox.curselection()
                    for i in range(0, len(indexes)):
                        listbox2.insert(END, values[i])
                        listbox.delete(indexes[len(indexes) - 1 - i], indexes[len(indexes) - 1 - i])

                
            frame = Frame(self.root_selectSetIdsAndSeqIds, width=800, height=400, bd=1, bg='white')
            frame.pack()
            
            iframe21 = Frame(frame, bd=4, relief=RIDGE)
            t = StringVar()

            listbox = Listbox(iframe21, selectmode=EXTENDED)
            listbox.config(width=48)
            listbox.pack(side=LEFT, padx=5, fill=BOTH)
            
            listbox2 = Listbox(iframe21, selectmode=EXTENDED)
            listbox2.config(width=48)
            listbox2.pack(side=RIGHT, padx=5, fill=BOTH)
            
            try:
                for setId in sqlite_methods.getSetIds(self.db_file, self.density_table):
                    if(self.SequenceNameMap.get(setId[0]) == None):
                        listbox.insert(END, setId[0])
                    else:
                        listbox.insert(END, self.SequenceNameMap.get(setId[0]))
            except Exception:
                print "ERROR", "RedrawStackedHeatmap", "No set id specified"
                      
            sbar = Scrollbar(iframe21)
            sbar.config(command=listbox.yview)                   
            sbar.pack(side=LEFT, pady=5, fill=BOTH)           
            listbox.config(yscrollcommand=sbar.set)   
            
            sbar = Scrollbar(iframe21)
            sbar.config(command=listbox2.yview)                   
            sbar.pack(side=RIGHT, pady=5, fill=BOTH)           
            listbox2.config(yscrollcommand=sbar.set)   
            
            iframe21.pack(expand=1, fill=X, pady=10, padx=5)

            but1 = Button(iframe21, image=self.backward, command=List1ToList2)
            but1.pack(side=BOTTOM)
            but2 = Button(iframe21, image=self.forward, command=List2ToList1)
            but2.pack(side=BOTTOM)
            
            
            def destroyShowSeqs():
                try:
                    self.root_selectSetIdsAndSeqIds.destroy()
                except Exception:
                     pass
                 
                self.root_selectSetIdsAndSeqIds = None
            
            iframe3 = Frame(frame, bd=2, relief=RIDGE)
            button1 = Button(iframe3, image=self.ok, command=state)
            button1.pack(side=RIGHT, padx=5)

            iframe22 = Frame(frame, bd=4, relief=RIDGE)

            t = StringVar()
            Button(iframe3, image=self.quit, command=destroyShowSeqs).pack(side=RIGHT, padx=5)
            iframe3.pack(expand=1, fill=X, pady=10, padx=5)
            
            iframe4 = Frame(frame, bd=2)
            Label(iframe4, text='').pack()   
            iframe4.pack(expand=2, fill=X, pady=10, padx=5)
                                  
    def GenerateBarchart(self):
        
        try:
            self.root_selectSetIds.destroy()
        except Exception:
             pass
         
        self.root_selectSetIds = None
        
        if(self.root_selectSetIds == None):
            self.root_selectSetIds = Toplevel()
            self.root_selectSetIds.title("Select SetIds for Stacked Barcharts")
    
            canv = Canvas(self.root_selectSetIds, bg="white", relief=SUNKEN)
            canv.config(scrollregion=(0, 0, 300, 800))         
            canv.config(highlightthickness=0)    
     
            var1 = StringVar()
            var2 = StringVar()

            def close():
                try:
                    self.root_selectSetIds.destroy()
                except Exception:
                     pass
                self.root_selectSetIds = None
                
            def state():
                self.SetIdList = listbox2.get(0, END)
                if(len(listbox2.get(0, END)) != 0):
                    redraw.RedrawBarChart(self, True)
                    self.createMenu(self.display)
                    destroyShowSeqs()
                    self.focusOnBarCharts = 1
                            
            def List1ToList2():
                if(listbox2.selection_get() != None and
                       len(listbox2.curselection()) > 0):
                        values = listbox2.selection_get().split("\n")
                        indexes = listbox2.curselection()
                        for i in range(0, len(indexes)):
                            listbox.insert(END, values[i])
                            listbox2.delete(indexes[len(indexes) - 1 - i], indexes[len(indexes) - 1 - i])

                
            def List2ToList1():
                if(listbox.selection_get() != None and

                       len(listbox.curselection()) > 0):
                        values = listbox.selection_get().split("\n")
                        indexes = listbox.curselection()
                        for i in range(0, len(indexes)):
                            listbox2.insert(END, values[i])
                            listbox.delete(indexes[len(indexes) - 1 - i], indexes[len(indexes) - 1 - i])
                
            frame = Frame(self.root_selectSetIds, width=800, height=400, bd=1, bg='white')
            frame.pack()
            
            iframe21 = Frame(frame, bd=4, relief=RIDGE)
            t = StringVar()

            listbox = Listbox(iframe21, selectmode=EXTENDED)
            listbox.config(width=48)
            listbox.pack(side=LEFT, padx=5, fill=BOTH)
            
            listbox2 = Listbox(iframe21, selectmode=EXTENDED)
            listbox2.config(width=48)
            listbox2.pack(side=RIGHT, padx=5, fill=BOTH)
            
            try:
                for setId in sqlite_methods.getSetIds(self.db_file, self.density_table):

                    foundSeqId = 0
                    
                    if(str(setId[0]).find("TALLYMER") == -1 and
                       str(setId[0]).find("GC_percent") == -1):
                        for cSeqId in self.seq_ids:
                            if(cSeqId == setId[0]):
                                foundSeqId = 1
                            
                        if(foundSeqId == 0):
                            if(self.SequenceNameMap.get(setId[0]) == None):
                                listbox.insert(END, setId[0])
                            else:
                                listbox.insert(END, self.SequenceNameMap.get(setId[0]))
                        else:
                            if(self.SequenceNameMap.get(setId[0]) == None):
                                listbox2.insert(END, setId[0])
                            else:
                                listbox2.insert(END, self.SequenceNameMap.get(setId[0]))

            except Exception:
                print "ERROR", "GenerateBarchart", "No set id specified"
                      
            sbar = Scrollbar(iframe21)
            sbar.config(command=listbox.yview)                   
            sbar.pack(side=LEFT, pady=5, fill=BOTH)           
            listbox.config(yscrollcommand=sbar.set)   
            
            sbar = Scrollbar(iframe21)
            sbar.config(command=listbox2.yview)                   
            sbar.pack(side=RIGHT, pady=5, fill=BOTH)           
            listbox2.config(yscrollcommand=sbar.set)   
            
            iframe21.pack(expand=1, fill=X, pady=10, padx=5)

            but1 = Button(iframe21, image=self.backward, command=List1ToList2)
            but1.pack(side=BOTTOM)
            but2 = Button(iframe21, image=self.forward, command=List2ToList1)
            but2.pack(side=BOTTOM)
            
            
            def destroyShowSeqs():
                try:
                    self.root_selectSetIds.destroy()
                except Exception:
                     pass
                 
                self.root_selectSetIds = None
            
            iframe3 = Frame(frame, bd=2, relief=RIDGE)
            button1 = Button(iframe3, image=self.ok, command=state)
            button1.pack(side=RIGHT, padx=5)

            t = StringVar()
            Button(iframe3, image=self.quit, command=destroyShowSeqs).pack(side=RIGHT, padx=5)
            iframe3.pack(expand=1, fill=X, pady=10, padx=5)
            
    def CreateRootShowSequences(self):
        try:
            self.root_showSequences.destroy()
        except Exception:
             pass
                     
        self.root_showSequences = None
        
        if(self.root_showSequences == None):
            self.root_showSequences = Toplevel()
            self.root_showSequences.title("Show Seq_ids")
    
            canv = Canvas(self.root_showSequences, bg="white", relief=SUNKEN)
            canv.config(width=300, height=200)                
            canv.config(scrollregion=(0, 0, 300, 1000))         
            canv.config(highlightthickness=0)    
     
            var1 = StringVar()
            var2 = StringVar()
            
            def close():
                try:
                    self.root_showSequences.destroy()
                except Exception:
                    pass
                self.root_showSequences = None
                
            def state():
                values = listbox2.get(0, END)

                if(len(values) > 0):
                    self.mySeqList = []
                    for value in values:
                        self.mySeqList.append(value)
                    
                    self.ChangeNContent()
                    self.ChangeFullLength()
    
                    self.maxV = 0
                    self.minV = 999999
                       
                    self.showSeqId()                
                    destroyShowSeqs()
                    
                    if(self.focusOnBarCharts == 0):
                        redraw.RedrawHeatmap(self)
                    else:
                        print "INFO", "CreateRootShowSequences", "Only supported in creating heatmaps"
                
            def List1ToList2():
                if(listbox2.selection_get() != None and
                   len(listbox2.curselection()) > 0):
                    values = listbox2.selection_get().split("\n")
                    indexes = listbox2.curselection()
                    for i in range(0, len(indexes)):
                        listbox.insert(END, values[i])
                        listbox2.delete(indexes[len(indexes) - 1 - i], indexes[len(indexes) - 1 - i])
                        
            def List2ToList1():
                if(listbox.selection_get() != None and
                   len(listbox.curselection()) > 0):
                    values = listbox.selection_get().split("\n")
                    indexes = listbox.curselection()
                    for i in range(0, len(indexes)):
                        listbox2.insert(END, values[i])
                        listbox.delete(indexes[len(indexes) - 1 - i], indexes[len(indexes) - 1 - i])
                
            frame = Frame(self.root_showSequences, width=500, height=400, bd=1, bg='white')
            frame.pack()
            
            iframe21 = Frame(frame, bd=4, relief=RIDGE)
            t = StringVar()

            listbox = Listbox(iframe21, selectmode=EXTENDED)
            listbox.pack(side=LEFT, padx=5)
            
            listbox2 = Listbox(iframe21, selectmode=EXTENDED)
            listbox2.pack(side=RIGHT, padx=5)
            
            seqs = sqlite_methods.getSeqIds(self.db_file, self.density_table, self.set_id_A)
            seqs_ordered = []
            for seq in seqs:
                seqs_ordered.append(seq[0])
            seqs_ordered = methods.sort_seq_ids(seqs_ordered)
            
            try:
                for seqId in seqs_ordered:

                    foundSeqId = 0
                    
                    for cSeqId in self.seq_ids:
                        if(cSeqId == seqId):
                            foundSeqId = 1
                        
                    if(foundSeqId == 0):
                        if(self.SequenceNameMap.get(seqId) == None):
                            listbox.insert(END, seqId)
                        else:
                            listbox.insert(END, self.SequenceNameMap.get(seqId))
                    else:
                        if(self.SequenceNameMap.get(seqId) == None):
                            listbox2.insert(END, seqId)
                        else:
                            listbox2.insert(END, self.SequenceNameMap.get(seqId))

            except Exception:
                print "ERROR", "CreateRootShowSequences", "No set id specified"
                      
            sbar = Scrollbar(iframe21)
            sbar.config(command=listbox.yview)                   
            sbar.pack(side=LEFT, pady=5, fill=BOTH)           
            listbox.config(yscrollcommand=sbar.set)   
            
            sbar = Scrollbar(iframe21)
            sbar.config(command=listbox2.yview)                   
            sbar.pack(side=RIGHT, pady=5, fill=BOTH)           
            listbox2.config(yscrollcommand=sbar.set)   
            
            iframe21.pack(expand=1, fill=X, pady=10, padx=5)

            but1 = Button(iframe21, image=self.backward, command=List1ToList2)
            but1.pack(side=BOTTOM)
            but2 = Button(iframe21, image=self.forward, command=List2ToList1)
            but2.pack(side=BOTTOM)
            
            
            def destroyShowSeqs():
                try:
                    self.root_showSequences.destroy()
                except Exception:
                    pass
                    
                self.root_showSequences = None
            
            iframe3 = Frame(frame, bd=2, relief=RIDGE)
            button1 = Button(iframe3, image=self.ok, command=state)
            button1.pack(side=RIGHT, padx=5)

            t = StringVar()
            Button(iframe3, image=self.quit, command=destroyShowSeqs).pack(side=RIGHT, padx=5)
            iframe3.pack(expand=1, fill=X, pady=10, padx=5)
            
            iframe4 = Frame(frame, bd=2)
            Label(iframe4, text='Seq_ids in the right box are displayed').pack()   
            iframe4.pack(expand=2, fill=X, pady=10, padx=5)

    def ShowSeqIds(self):
        
        self.CreateRootShowSequences()
                        
            
    def RenameSetId(self):
        try:
            self.root_renameSetId.destroy()
        except Exception:
            pass
            
        if(self.root_renameSetId == None):
            
            self.root_renameSetId = Toplevel()
            self.root_renameSetId.title("Rename Set_id")
    
            var1 = StringVar()
            var2 = StringVar()
            
            def state(): 
                newSetId = entry.get()
                newSetId = str(newSetId).strip()
                
                if(len(newSetId) > 0):
                    self.SetIdMap[self.set_id_A] = newSetId
                    if(self.focusOnBarCharts == 1):
                        redraw.RedrawBarChart(self, False)
                    else:        
                        redraw.RedrawHeatmap(self)
                destroyRenameSetId()
                
            frame = Frame(self.root_renameSetId, width=500, height=400, bd=1, bg="white")
            frame.pack()
            
            iframe21 = Frame(frame, bd=3, relief=RIDGE)
            Label(iframe21, text='Set_id:').pack(side=LEFT, padx=5)
            label1 = Label(iframe21, text=self.set_id_A).pack(side=LEFT, padx=5)
            iframe21.pack(expand=1, fill=X, pady=10, padx=5)
            
            iframe2 = Frame(frame, bd=2, relief=RIDGE)
            Label(iframe2, text='replace with:').pack(side=LEFT, padx=5)
            t = StringVar()
            entry = Entry(iframe2, textvariable=t, bg='white')
            
            if(self.SetIdMap.get(self.set_id_A) != None):
                entry.insert(0, self.SetIdMap.get(self.set_id_A))
            else:
                entry.insert(0, self.set_id_A)
            
            entry.pack(side=RIGHT, padx=5)
            iframe2.pack(expand=1, fill=X, pady=10, padx=5)
            
            def destroyRenameSetId():
                try:
                    self.root_renameSetId.destroy()
                except Exception:
                    pass
                self.root_renameSetId = None
            
            iframe3 = Frame(frame, bd=2, relief=RIDGE)
            Button(iframe3, image=self.ok, command=state).pack(side=RIGHT, padx=5)
            t = StringVar()
            Button(iframe3, image=self.quit, command=destroyRenameSetId).pack(side=RIGHT, padx=5)
            iframe3.pack(expand=1, fill=X, pady=10, padx=5)
        
    
    def RenameSeqIds(self):
        try:
            self.root_renameSequences.destroy()
        except Exception:
            pass
            
        if(self.root_renameSequences == None):
            
            self.root_renameSequences = Toplevel()
            self.root_renameSequences.title("Rename Seq_id")
    
            var1 = StringVar()
            var2 = StringVar()
            
            def state(): 
                newSeqId = entry.get()
                newSeqId = str(newSeqId).strip()
                
                if(len(newSeqId) > 0):
                    cSeqId = listbox.selection_get()
                    if(len(cSeqId) > 0):
                        for value in self.seq_ids:
                            if(value == cSeqId):
                                self.SequenceNameMap[value] = newSeqId
                            if(self.SequenceNameMap.get(value) == cSeqId):
                                self.SequenceNameMap[value] = newSeqId
                if(self.focusOnBarCharts == 1):
                    redraw.RedrawBarChart(self, False)
                elif(self.focusOnBarCharts == 0):     
                    redraw.RedrawHeatmap(self)
                else:
                    redraw.RedrawStackedHeatmap(self)
                destroyRenameSeqs()
                
            frame = Frame(self.root_renameSequences, width=500, height=400, bd=1, bg="white")
            frame.pack()
            
            iframe21 = Frame(frame, bd=3, relief=RIDGE)
            Label(iframe21, text='seq_id:').pack(side=LEFT, padx=5)
            t = StringVar()
            listbox = Listbox(iframe21)
            listbox.pack(side=LEFT, padx=5)
            
            for seqId in self.seq_ids:
                if(self.SequenceNameMap.get(seqId) == None):
                    listbox.insert(END, seqId)
                else:
                    listbox.insert(END, self.SequenceNameMap.get(seqId))
                    
            if(len(self.seq_ids) > 0):
                listbox.selection_set(first=0)
    
            iframe21.pack(expand=1, fill=X, pady=10, padx=5)
            
            iframe2 = Frame(frame, bd=2, relief=RIDGE)
            Label(iframe2, text='replace with:').pack(side=LEFT, padx=5)
            t = StringVar()
            entry = Entry(iframe2, textvariable=t, bg='white')
            entry.pack(side=RIGHT, padx=5)
            iframe2.pack(expand=1, fill=X, pady=10, padx=5)
            
            def destroyRenameSeqs():
                try:
                    self.root_renameSequences.destroy()
                except Exception:
                    pass
                    
                self.root_renameSequences = None
            
            iframe3 = Frame(frame, bd=2, relief=RIDGE)
            Button(iframe3, image=self.ok, command=state).pack(side=RIGHT, padx=5)
            t = StringVar()
            Button(iframe3, image=self.quit, command=destroyRenameSeqs).pack(side=RIGHT, padx=5)
            iframe3.pack(expand=1, fill=X, pady=10, padx=5)
        
            sbar = Scrollbar(iframe21)
            sbar.config(command=listbox.yview)                   
            sbar.pack(side=RIGHT, pady=5, fill=BOTH)             
            listbox.config(yscrollcommand=sbar.set)   

    def ShowAbout(self):
        
        try:
            self.root_about.destroy()
        except Exception:
            pass
            
        self.root_about = Toplevel()
        self.root_about.title("About")
        
        p = PhotoImage(file=self.cwd + "/pix/logo.GIF")
            
        def openWeb():
            webbrowser.open("http://mips.helmholtz-muenchen.de/plant/index.jsp")
            
        b = Button(self.root_about, width=320, height=206, image=p, command=openWeb)
        
        b.pack(side=LEFT, padx=2, pady=2)
        
        self.root_about.mainloop()

    def MoveForward(self, event):
        self.click_1(event)
        
        if(self.heatmapsToMove.get(self.cposition) != None):
            for item in self.heatmapsToMove.get(self.cposition):
                self.root.canvas.move(item, 10, 0)

            if(self.moveNPixelMap.get(self.cposition) != None):
                self.moveNPixelMap[self.cposition] = self.moveNPixelMap[self.cposition] + 10
            else:
                self.moveNPixelMap[self.cposition] = 10
            
            max = 0
            positionMax = 0
            position = 1
            for seq_id in self.seq_ids:
                if(self.elementList.get(seq_id) == None):
                    elements = self.getElementsFromDatabase(seq_id, self.set_id_A, self.density_table, self.db_file)[0]                  
                    self.elementList[seq_id] = elements
                else:
                    elements = self.elementList.get(seq_id)
                
                pixelToAdd = 0
                if(self.moveNPixelMap.get(position) != None):
                    pixelToAdd = self.moveNPixelMap[position]
                
                if(max < ((len(elements) + pixelToAdd))):
                   max = len(elements) + pixelToAdd
                   positionMax = position
                   
                position = position + 1
                
            if(self.cposition == positionMax):
                
                if(self.moveNPixelCanvas != None):
                    self.moveNPixelCanvas = self.moveNPixelCanvas + 10
                else:
                    self.moveNPixelCanvas = 10

                for item in self.colorBarToMove:
                    self.root.canvas.move(item, 10, 0)
                for item in self.barCodeLegendToMove:
                    self.root.canvas.move(item, 10, 0)
    
    def MoveBegin(self, event):
        self.click_1(event)
        
        if(self.heatmapsToMove.get(self.cposition) != None):
            if(self.moveNPixelMap.get(self.cposition) == None):
                self.moveNPixelMap[self.cposition] = 0
            for item in self.heatmapsToMove.get(self.cposition):
                self.root.canvas.move(item, -self.moveNPixelMap[self.cposition], 0)
        
        max = 0
        positionMax = 0
        position = 1

        for seq_id in self.seq_ids:
            if(self.elementList.get(seq_id) == None):
                elements = self.getElementsFromDatabase(seq_id, self.set_id_A, self.density_table, self.db_file)[0]
                self.elementList[seq_id] = elements
            else:
                elements = self.elementList.get(seq_id)
                
            pixelToAdd = 0
            if(self.moveNPixelMap.get(position) != None):
                pixelToAdd = self.moveNPixelMap[position]
                
            if(max < ((len(elements) + pixelToAdd))):
                max = len(elements) + pixelToAdd
                positionMax = position
                   
            position = position + 1
                
        if(self.cposition == positionMax):


            for item in self.colorBarToMove:
                self.root.canvas.move(item, -self.moveNPixelCanvas, 0)
            for item in self.barCodeLegendToMove:
                self.root.canvas.move(item, -self.moveNPixelCanvas, 0)
            self.moveNPixelCanvas = 0
            
        self.moveNPixelMap[self.cposition] = 0
        
    def MoveBackward(self, event):
        self.click_1(event)
        
        if(self.heatmapsToMove.get(self.cposition) != None):
            for item in self.heatmapsToMove.get(self.cposition):
                self.root.canvas.move(item, -10, 0)
            if(self.moveNPixelMap.get(self.cposition) != None):
                self.moveNPixelMap[self.cposition] = self.moveNPixelMap[self.cposition] - 10
            else:
                self.moveNPixelMap[self.cposition] = -10

        max = 0
        positionMax = 0
        position = 1

        for seq_id in self.seq_ids:
            if(self.elementList.get(seq_id) == None):
                elements = self.getElementsFromDatabase(seq_id, self.set_id_A, self.density_table, self.db_file)[0]            
                self.elementList[seq_id] = elements
            else:
                elements = self.elementList.get(seq_id)
                
            pixelToAdd = 0
            if(self.moveNPixelMap.get(position) != None):
                pixelToAdd = self.moveNPixelMap[position]
                
            if(max < ((len(elements) + pixelToAdd))):
                max = len(elements) + pixelToAdd
                positionMax = position
                   
            position = position + 1
                
        if(self.cposition == positionMax):
            if(self.moveNPixelCanvas != None):
                self.moveNPixelCanvas = self.moveNPixelCanvas - 10
            else:
                self.moveNPixelCanvas = -10

            for item in self.colorBarToMove:
                self.root.canvas.move(item, -10, 0)
            for item in self.barCodeLegendToMove:
                self.root.canvas.move(item, -10, 0)

    def ZoomOut(self):
        if(self.zoomMinusFactor < 1.2):
            self.zoomMinusFactor = self.zoomMinusFactor * 1.1
            self.fontSize = int(math.ceil(self.fontSize / self.zoomMinusFactor))
            redraw.RedrawHeatmap(self)
            self.root.canvas.scale('all', 100, 100, 1 / float(self.zoomMinusFactor), 1 / float(self.zoomMinusFactor))
        
    def ZoomIn(self):
        if(self.zoomMinusFactor > 0.8):
            self.zoomMinusFactor = self.zoomMinusFactor / 1.1
            self.fontSize = int(math.ceil(self.fontSize / self.zoomMinusFactor))
            redraw.RedrawHeatmap(self)
            self.root.canvas.scale('all', 100, 100, 1 / float(self.zoomMinusFactor), 1 / float(self.zoomMinusFactor))
        
    def select1(self, event):
        self.root.canvas.delete("popup")
        self.root.canvas.create_rectangle(self.root.canvas.canvasx(event.x), self.root.canvas.canvasy(event.y), \
                                                  self.root.canvas.canvasx(event.x) + 100, self.root.canvas.canvasy(event.y) + 50, tag=("popup"), width=0, fill="yellow")
        self.root.canvas.create_text(self.root.canvas.canvasx(event.x), self.root.canvas.canvasy(event.y) + 20, font=("Helvetica", 8), \
                                              text="This is a test\nmaybe this functionality\ncan be used", tag="popup", justify="left", anchor="w")
        
    def ShowToolTip(self):
        self.root.canvas.bind ("<Button-1>", self.select1)

        
    def CreateLineChart(self):
        self.ChangeSetId(True)
        redraw.RedrawLineChart(self)

    def DoCreateLineChart(self):
        generate.GenerateLinechart(self) 
               
    def DoCreateHeatmap(self):
        generate.GenerateHeatmap(self)

    def openManual(self):
        try:
            # WINDOWS supported
            try:
                os.startfile(self.cwd + "/doc/ChromoWIZ_Manual.pdf")    
            except Exception:
                pass
            
            # LINUX supported
            try:
                os.system("acroread " + self.cwd + "/doc/ChromoWIZ_Manual.pdf") 
            except Exception:
                pass

        except Exception:
            print "ERROR", "openManual", "unable to open MANUAL"

    def DoQuit(self):
        if askyesno('Closing ChromoWIZ', 'Are you sure you want to quit?'):
            self.root.destroy()

    def DoChangeMode(self):
        if(self.focusOnBarCharts == 1):
            return
        
        if(self.button5["text"] == "# per Mb"):
            self.button5["text"] = "% bp"
            self.ModeId.set("# per Mb")
        else:
            self.button5["text"] = "# per Mb"
            self.ModeId.set("% bp")
        self.ChangeMode()
        
            
    def createMenu(self, mode):
        menubar = Menu(self.root)
        
        if(self.init == True):
            toolbar = Frame(self.root, cursor='hand2', relief=SUNKEN, bd=2)
            toolbar.pack(side=TOP, fill=X)
            self.button1 = Button(toolbar, text='Quit', image=self.b1, command=self.DoCreateLineChart)

            self.button1.pack(side=LEFT)
            config_file_creator.createToolTip(self.button1, "Generate Linechart")

            self.button4 = Button(toolbar, text='Hello', image=self.b4, command=self.GenerateBarchart)
            self.button4.pack(side=LEFT)
            config_file_creator.createToolTip(self.button4, "Generate Barchart")
            
            self.button2 = Button(toolbar, text='Hello', image=self.b2, command=self.DoCreateHeatmap)
            self.button2.pack(side=LEFT)
            config_file_creator.createToolTip(self.button2, "Generate Heatmap")
            
            self.button3 = Button(toolbar, text='Hello', image=self.b3, command=self.GenerateStackedHeatmap)
            self.button3.pack(side=LEFT)
            config_file_creator.createToolTip(self.button3, "Generate Stacked Heatmap")

            _state = NORMAL
            if(len(self.set_id_A) == 0):
                _state = DISABLED
                
            self.button5 = Button(toolbar, bg="lightblue", command=self.DoChangeMode, state=_state, height=2)
                
            if(self.display == "% bp"):
                self.button5["text"] = "# per Mb"
            else:
                self.button5["% bp"]
            self.button5.pack(side=LEFT)
                
            config_file_creator.createToolTip(self.button5, "")

            self.toolbar2 = Frame(self.root, cursor='hand2', relief=SUNKEN, bd=2)

            DEFAULT_FONT = {'family':"helvetica", 'weight':'normal', 'size':12}
            defaultFont = tkFont.Font(**DEFAULT_FONT)
            self.button7 = Button(toolbar, text='Manual', font=defaultFont, command=self.openManual)
            self.button7.pack(side=RIGHT)

            self.button6 = Button(self.toolbar2, text='Hello', image=self.wizard).pack(side=TOP)
            self.toolbar2.pack(side=TOP, fill=X)
            
            self.button1["state"] = DISABLED
            self.button2["state"] = DISABLED
            self.button3["state"] = DISABLED
            self.button4["state"] = DISABLED
        else:
            self.toolbar2.destroy()
            self.button1["state"] = NORMAL
            self.button2["state"] = NORMAL
            self.button3["state"] = NORMAL
            self.button4["state"] = NORMAL
            
        self.init = False
        
        saveAsMenu = Menu(menubar)
        state_export_image = NORMAL
        if(self.image_export_possible == False):
            state_export_image = DISABLED

        saveAsMenu.add_command(label="PS", command=self.exportGUICanvas, underline=1)
        
        filemenu = Menu(menubar)
        filemenu.add_command(label="Open...", command=self.FileOpenMenu, underline=0)
        filemenu.add_separator()

        state_saveAsMenu = NORMAL
        if(self.density_table == ""):
            state_saveAsMenu = DISABLED
        filemenu.add_command(label="Save as", command=self.export, underline=0, state=state_saveAsMenu)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.DoQuit, underline=0) 
        menubar.add_cascade(label="File", menu=filemenu, underline=0)

        if(len(self.db_file) == 0 and len(self.set_id_A) == 0):
            state = DISABLED
        else:
            state = NORMAL

        if(self.focusOnBarCharts == 0):
            state0 = NORMAL
            state1 = DISABLED
            state2 = DISABLED
        elif(self.focusOnBarCharts == 1):
            state0 = DISABLED
            state1 = NORMAL
            state2 = DISABLED
        else:
            state0 = NORMAL
            state1 = DISABLED
            state2 = NORMAL

        
        editmenu = Menu(menubar)
        
        editmenu.add_command(label="Rename seq_ids", command=self.RenameSeqIds, underline=0)
        
        if(self.focusOnBarCharts == 0):
            editmenu.add_command(label="Rename set_id", command=self.RenameSetId, underline=0)
        
        editmenu.add_command(label="Choose seq_ids", command=self.ShowSeqIds)
        editmenu.add_separator()

        self.NContent = DoubleVar()
        self.NContent.set(self.currNContent)
        
        NMaxPercentMenu = Menu(editmenu)
        NMaxPercentMenu.add_radiobutton(label="10", variable=self.NContent, value=10, command=self.ChangeNContent)
        NMaxPercentMenu.add_radiobutton(label="20", variable=self.NContent, value=20, command=self.ChangeNContent)
        NMaxPercentMenu.add_radiobutton(label="30", variable=self.NContent, value=30, command=self.ChangeNContent)
        NMaxPercentMenu.add_radiobutton(label="40", variable=self.NContent, value=40, command=self.ChangeNContent)
        NMaxPercentMenu.add_radiobutton(label="50", variable=self.NContent, value=50, command=self.ChangeNContent)
        NMaxPercentMenu.add_radiobutton(label="60", variable=self.NContent, value=60, command=self.ChangeNContent)
        NMaxPercentMenu.add_radiobutton(label="70", variable=self.NContent, value=70, command=self.ChangeNContent)
        NMaxPercentMenu.add_radiobutton(label="80", variable=self.NContent, value=80, command=self.ChangeNContent)
        NMaxPercentMenu.add_radiobutton(label="90", variable=self.NContent, value=90, command=self.ChangeNContent)
        NMaxPercentMenu.add_radiobutton(label="100", variable=self.NContent, value=100, command=self.ChangeNContent)
        #editmenu.add_cascade(label="maximum N content (% of window size)", menu=NMaxPercentMenu)
        
        terminatingEndsMenu = Menu(editmenu)
        self.FullLength = StringVar()
        self.FullLength.set(self.currFullLength)
        terminatingEndsMenu.add_radiobutton(label="0", variable=self.FullLength, value=0, command=self.ChangeFullLength)
        terminatingEndsMenu.add_radiobutton(label="10", variable=self.FullLength, value=10, command=self.ChangeFullLength)
        terminatingEndsMenu.add_radiobutton(label="20", variable=self.FullLength, value=20, command=self.ChangeFullLength)
        terminatingEndsMenu.add_radiobutton(label="30", variable=self.FullLength, value=30, command=self.ChangeFullLength)
        terminatingEndsMenu.add_radiobutton(label="40", variable=self.FullLength, value=40, command=self.ChangeFullLength)
        terminatingEndsMenu.add_radiobutton(label="50", variable=self.FullLength, value=50, command=self.ChangeFullLength)
        terminatingEndsMenu.add_radiobutton(label="60", variable=self.FullLength, value=60, command=self.ChangeFullLength)
        terminatingEndsMenu.add_radiobutton(label="70", variable=self.FullLength, value=70, command=self.ChangeFullLength)
        terminatingEndsMenu.add_radiobutton(label="80", variable=self.FullLength, value=80, command=self.ChangeFullLength)
        terminatingEndsMenu.add_radiobutton(label="90", variable=self.FullLength, value=90, command=self.ChangeFullLength)
        terminatingEndsMenu.add_radiobutton(label="100", variable=self.FullLength, value=100, command=self.ChangeFullLength)
        #editmenu.add_cascade(label="minimum window size (% of maximum window size)", menu=terminatingEndsMenu)

        GapBetweenHeatmapsMenu = Menu(editmenu)
        self.GapBetweenSequences = DoubleVar()
        self.GapBetweenSequences.set(70)
        GapBetweenHeatmapsMenu.add_radiobutton(label="0", variable=self.GapBetweenSequences, value=0, command=self.ChangeGapBetweenSequences)
        GapBetweenHeatmapsMenu.add_radiobutton(label="10", variable=self.GapBetweenSequences, value=10, command=self.ChangeGapBetweenSequences)
        GapBetweenHeatmapsMenu.add_radiobutton(label="20", variable=self.GapBetweenSequences, value=20, command=self.ChangeGapBetweenSequences)
        GapBetweenHeatmapsMenu.add_radiobutton(label="30", variable=self.GapBetweenSequences, value=30, command=self.ChangeGapBetweenSequences)
        GapBetweenHeatmapsMenu.add_radiobutton(label="40", variable=self.GapBetweenSequences, value=40, command=self.ChangeGapBetweenSequences)
        GapBetweenHeatmapsMenu.add_radiobutton(label="50", variable=self.GapBetweenSequences, value=50, command=self.ChangeGapBetweenSequences)
        GapBetweenHeatmapsMenu.add_radiobutton(label="60", variable=self.GapBetweenSequences, value=60, command=self.ChangeGapBetweenSequences)
        GapBetweenHeatmapsMenu.add_radiobutton(label="70", variable=self.GapBetweenSequences, value=70, command=self.ChangeGapBetweenSequences)
        GapBetweenHeatmapsMenu.add_radiobutton(label="80", variable=self.GapBetweenSequences, value=80, command=self.ChangeGapBetweenSequences)
        GapBetweenHeatmapsMenu.add_radiobutton(label="90", variable=self.GapBetweenSequences, value=90, command=self.ChangeGapBetweenSequences)
        editmenu.add_cascade(label="gap between sequences (in pixel)", menu=GapBetweenHeatmapsMenu)

        visualisationModeMenu = Menu(editmenu)
        self.ModeId = StringVar()
        self.ModeId.set(self.display)
        
        if(self.focusOnBarCharts == 2):
            self.disableAbsoluteMode = False
            self.disablePercentMode = False

        if(self.focusOnBarCharts != 1):
            state_disablePercentMode = NORMAL
            if(self.disablePercentMode == True):
                state_disablePercentMode = DISABLED
            
            visualisationModeMenu.add_radiobutton(label="% bp", variable=self.ModeId, value="% bp", command=self.ChangeMode, state=state_disablePercentMode)
    
            state_disableAbsoluteMode = NORMAL
            if(self.disableAbsoluteMode == True):
                state_disableAbsoluteMode = DISABLED
            
            if(self.disableAbsoluteMode == True):
                state_disableAbsoluteMode = DISABLED
            else:
                state_disableAbsoluteMode = NORMAL
            
            visualisationModeMenu.add_radiobutton(label="# per Mb", variable=self.ModeId, value="# per Mb", command=self.ChangeMode, state=state_disableAbsoluteMode)
       
        menubar.add_cascade(label="Edit", menu=editmenu, underline=0, state=state)

        displayMenu = Menu(menubar)
        heatmapMenu = Menu(displayMenu)
        barStackMenu = Menu(displayMenu)
        stackedHeatmapMenu = Menu(displayMenu)
        lineChartMenu = Menu(displayMenu)
        colorMenu = Menu(barStackMenu)
        
        SetIdMenu2 = Menu(colorMenu)
        setIds = self.SetIdList
        self.SetId2 = StringVar()
        for setId in setIds:
            self.SetId2.set(setId)
            if(self.colorToSetIdMap.get(setId) == None):
                Color = "grey"
            else:
                Color = self.colorToSetIdMap.get(setId)
            SetIdMenu2.add_radiobutton(label=setId, variable=self.SetId2, value=setId, command=self.ChangeColor, background=Color)
        
        barStackMenu.add_command(label="Generate Barchart", underline=0, command=self.GenerateBarchart)
        barStackMenu.add_cascade(label="Change Colors", menu=SetIdMenu2, state=state1)
        menubar.add_cascade(label="Display", menu=displayMenu, state=state, underline=0)
        
        stackedHeatmapMenu.add_command(label="Generate Stacked Heatmaps", underline=0, command=self.GenerateStackedHeatmap)
        stackedHeatmapMenu.add_command(label="Change max intensity", underline=0, command=self.CreateRootSelectMaxIntensity, state=state2)

        SetIdMenuHeatmap = Menu(heatmapMenu)
        SetIdMenuLine = Menu(lineChartMenu)
        
        setIds = sqlite_methods.getSetIds(self.db_file, self.density_table)
        self.SetId = StringVar()
        self.SetId.set(self.set_id_A)
        for setId in setIds:
            SetIdMenuHeatmap.add_radiobutton(label=setId[0], variable=self.SetId, value=setId[0], command=self.ChangeSetId)
            SetIdMenuLine.add_radiobutton(label=setId[0], variable=self.SetId, value=setId[0], command=self.CreateLineChart)

        helpmenu = Menu(menubar)
        helpmenu.add_command(label="About", underline=0, command=self.ShowAbout)
        menubar.add_cascade(label="Help", menu=helpmenu, underline=0)

        heatmapMenu.add_cascade(label="Set_ids", menu=SetIdMenuHeatmap)
        lineChartMenu.add_cascade(label="Set_ids", menu=SetIdMenuLine)
        lineChartMenu.add_separator()
        
        state_lineChart = NORMAL
        if(self.lineChart == False):
            state_lineChart = DISABLED
            
        RelAllowedGapMenu = Menu(lineChartMenu)
        RelAllowedGapMenu.add_radiobutton(label="0", variable=self.rel_allowed_gap, value=0, command=self.CreateLineChart)
        RelAllowedGapMenu.add_radiobutton(label="10", variable=self.rel_allowed_gap, value=10, command=self.CreateLineChart)
        RelAllowedGapMenu.add_radiobutton(label="20", variable=self.rel_allowed_gap, value=20, command=self.CreateLineChart)
        RelAllowedGapMenu.add_radiobutton(label="30", variable=self.rel_allowed_gap, value=30, command=self.CreateLineChart)
        RelAllowedGapMenu.add_radiobutton(label="40", variable=self.rel_allowed_gap, value=40, command=self.CreateLineChart)
        RelAllowedGapMenu.add_radiobutton(label="50", variable=self.rel_allowed_gap, value=50, command=self.CreateLineChart)
        RelAllowedGapMenu.add_radiobutton(label="60", variable=self.rel_allowed_gap, value=60, command=self.CreateLineChart)
        RelAllowedGapMenu.add_radiobutton(label="70", variable=self.rel_allowed_gap, value=70, command=self.CreateLineChart)
        RelAllowedGapMenu.add_radiobutton(label="80", variable=self.rel_allowed_gap, value=80, command=self.CreateLineChart)
        RelAllowedGapMenu.add_radiobutton(label="90", variable=self.rel_allowed_gap, value=90, command=self.CreateLineChart)
        lineChartMenu.add_cascade(label="Gap allowed in bp", menu=RelAllowedGapMenu, state=state_lineChart)

        RelSynValueMenu = Menu(lineChartMenu)
        RelSynValueMenu.add_radiobutton(label="0", variable=self.rel_syn_value, value=0, command=self.CreateLineChart)
        RelSynValueMenu.add_radiobutton(label="10", variable=self.rel_syn_value, value=10, command=self.CreateLineChart)
        RelSynValueMenu.add_radiobutton(label="20", variable=self.rel_syn_value, value=20, command=self.CreateLineChart)
        RelSynValueMenu.add_radiobutton(label="30", variable=self.rel_syn_value, value=30, command=self.CreateLineChart)
        RelSynValueMenu.add_radiobutton(label="40", variable=self.rel_syn_value, value=40, command=self.CreateLineChart)
        RelSynValueMenu.add_radiobutton(label="50", variable=self.rel_syn_value, value=50, command=self.CreateLineChart)
        RelSynValueMenu.add_radiobutton(label="60", variable=self.rel_syn_value, value=60, command=self.CreateLineChart)
        RelSynValueMenu.add_radiobutton(label="70", variable=self.rel_syn_value, value=70, command=self.CreateLineChart)
        RelSynValueMenu.add_radiobutton(label="80", variable=self.rel_syn_value, value=80, command=self.CreateLineChart)
        RelSynValueMenu.add_radiobutton(label="90", variable=self.rel_syn_value, value=90, command=self.CreateLineChart)
        lineChartMenu.add_cascade(label="Minimal Intensity", menu=RelSynValueMenu, state=state_lineChart)

        heatmapMenu.add_separator()
        displayMenu.add_cascade(label="Linechart", menu=lineChartMenu)
        displayMenu.add_cascade(label="Heatmap", menu=heatmapMenu)
        displayMenu.add_cascade(label="Stacked Heatmap", menu=stackedHeatmapMenu)
        displayMenu.add_cascade(label="Stacked Barcharts", menu=barStackMenu)
        displayMenu.add_separator()

        if(self.focusOnBarCharts != 0):
            state = DISABLED
        else:
            state = NORMAL
            
        displayMenu.add_command(label="Statistics", command=self.GetStatistics, state=state)
        
        
        self.root.config(menu=menubar)

        SeqIdMenu = Menu(displayMenu, tearoff=True)
        
        self.mySeqList = []
              
        curSeq = 0

        SeqIdMenu.add_separator()
        SeqIdMenu.add_command(label="Update", command=self.showSeqId)
        self.root.config(menu=menubar)

        if(self.focusOnBarCharts != 0 or self.disableShowConfig == True):
            state = DISABLED
        else:
            state = NORMAL
            
        heatmapMenu.add_command(label="Show Config File", command=self.ShowConfigFile, state=state)
        
    def ShowConfigFile(self):
        config_file = sqlite_methods.get_conf_file(self.db_file, self.set_id_A)
        self.show_config_file(config_file)
            
    def show_config_file(self, config_file):
        root = Tk()
        root.title("Configuration file")
        s = Scrollbar(root)
        T = Text(root)
        
        T.focus_set()
        s.pack(side=RIGHT, fill=Y)
        T.pack(side=LEFT, fill=Y)
        s.config(command=T.yview)
        T.config(yscrollcommand=s.set)
        
        T.insert(END, config_file)
        T.yview(MOVETO, 1.0)
        
        root.mainloop()
        
    def CreateHeatmap(self):
        redraw.RedrawHeatmap(self)
        
    def AddButton(self):
        if(self.scale == None):
            self.scale = Scale(self.root.canvas, from_=1, to=100, length=500, orient=HORIZONTAL, showvalue=True, bg="white")
            self.scale.pack()
            self.scale.set(100)
            self.scale["to"] = math.ceil(self.maxV)
            self.scale["from"] = math.ceil(self.minV)

        if(self.button == None):
            self.button = Button(self.root.canvas, text="REDRAW", command=self.CreateHeatmap, bg="white")
            self.button.pack(pady=5, side=TOP)
            self.button["fg"] = "red"
            self.button.config(bd=2, relief=RAISED)
            self.button.config(font=('Courier New', 10, 'bold'))
        
    def InitializeCanvas(self):
            canvas = self.add_canvas()
            
            self.root.canvas = canvas
            
            self.psheight = self.gapBetweenHeatmaps * (len(self.seq_ids) + 1)

            if(len(self.seq_ids) > 0):
                if(self.pswidth < 1000):
                    self.pswidth = 1000
                    self.pswidthExport = 1000
            else:
                self.pswidth = 500
                self.pswidthExport = 500
     
            position = 1
    
            self.maxLabelSize = 0
            self.maxLabelSizeExport = 0
            self.AdaptMaxLabelSize()

            nmb_max = sqlite_methods.get_max_nmb_elements_per_seq_id(self.db_file, self.density_table, self.set_id_A, self.seq_ids)
            self.nmb_max = nmb_max
            
            for seq_id in self.seq_ids:
                elements = []
                if(self.elementList.get(seq_id) == None):
                    elements = self.getElementsFromDatabase(seq_id, self.set_id_A, self.density_table, self.db_file)[0]
                    self.elementList[seq_id] = elements
                else:
                    elements = self.elementList.get(seq_id)
                
                calc_vis_elements.calc_vis_elements(self, elements, seq_id, position, 1, False, False, False, "", None, None)
                position = position + 1   
            
            self.ChangeSize()
        
    def setFullScreen(self):
        try:
            self.root.state('zoomed')
        except Exception:
            pass
            
        try:
            w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry("%dx%d+0+0" % (w, h))
        except Exception:
            pass
            
    def keyEvent(self, event):
        pass
        
    def __init__(self, set_id_A, density_table, db_file) :
        index = str(sys.argv[0]).rfind("/")
        if(index == -1):
            index = str(sys.argv[0]).rfind("\\")
        
        if(sys.argv[0][index - 1] != "/"):
            self.cwd = sys.argv[0][0:index] + "/"
        else:
            self.cwd = sys.argv[0][0:index]
            
        try:
            self.root = Tk()
            self.root["bg"] = "white"
        except Exception:
            pass
        self.set_id_A = set_id_A
        self.density_table = density_table
        self.cmd_line = False
        
        
        self.image_export_possible = image_export_possible

        self.fontSize = 1 
        self.fontSizeLabel = 30

        self.fontSizeSetId = 30
        self.fontSizeAxis = 20
        
        self.guiFontSize = 1 
        self.guiFontSizeLabel = 15
        self.guiFontSizeSetid = 15
        self.guiFontSizeAxis = 10
        
        self.fontSizeFactor = 2                                     # magnification factor, default: 3
        self.gapBetweenLabelAndHeatmap = 0                          # gap between seq_id/scaffold_id and heatmap start, default:0
        self.gapBetweenHeatmaps = 140                               # bounding box for heatmaps, default: 140
        self.heatMapSize = 60                                       # size of the heatmaps [0, self.gapBetweenHeatmaps], default:50
        self.startLabel = 50                                        # start position for drawing seq_id/scaffold_id
        self.image1Width = 15000                                    # size of background image
        self.image1Height = 30000                                   # size of background image
        self.colors = ["#458B74", "#DB7093", "#4e91c9", "#EEE8AA"]  # default colors for stacked barcharts
        self.colorBackGround = "#D3D3D3"                            # background for interspace 
        self.db_file = db_file
        self.currNContent = 60                                      # default value for N Content max
        self.currFullLength = 20                                    # default value for Block Size min
        self.display = "% bp"                                       # "% bp" or "# per Mb"
        self.toolbar2 = None

        try:
            self.rel_syn_value = DoubleVar()
            self.rel_syn_value.set(30)
            self.rel_allowed_gap = DoubleVar()
            self.rel_allowed_gap.set(30)
            self.rel_line_len = IntVar()
            self.rel_line_len.set(1)
        except Exception:   
            self.rel_allowed_gap_var = 30
            self.rel_syn_value_var = 30
            self.rel_line_len_var = 1
        self.bin_start = None
        self.bin_stop = None
        self.merged_blocks = {}
        self.nmb_max = None
        
        # not changeable parameter
        self.focusOnBarCharts = 0                       
        self.sbar = None
        self.heatmapsToMove = {}
        self.cposition = -1
        self.moveNPixelMap = {}
        self.moveNPixelCanvas = None
        self.colorBarToMove = []
        self.barCodeLegendToMove = []
        self.zoomMinusFactor = 1.0
        self.disablePercentMode = False
        self.disableAbsoluteMode = False
        self.disableShowConfig = False
        self.colorMap = {}
        self.root_information = None
        self.seq_ids = []
        self.root_showSequences = None
        self.root_renameSequences = None
        self.root_about = None
        self.root_renameSetId = None
        self.root_selectSetIds = None
        self.root_inverse_set_ids = None
        self.root_inverseSetIds = None
        self.colorToSetIdMap = {}
        self.root_selectSetIdsAndSeqIds = None
        self.root_relativeSetIds = None
        self.root_linechart = None
        self.root_heatmap = None
        self.root_chooseMaximumIntensities = None
        self.label_to_display = None
        self.anno_ids = []
        self.anno_ids_mItensities = {}
        self.elementList = {}
        self.SetIdList = []
        self.NList = {}
        self.WindowLengthList = {}
        self.SequenceNameMap = {}
        self.SetIdMap = {}
        self.maxV = 0
        self.minV = 999999
        self.canvasDrawn = 0
        self.positionHeatmaps = {}
        try:
            self.backward = PhotoImage(file=self.cwd + "/pix/backward.gif", master=self.root)
            self.forward = PhotoImage(file=self.cwd + "/pix/forward.gif", master=self.root)
            self.quit = PhotoImage(file=self.cwd + "/pix/quit.gif", master=self.root)
            self.ok = PhotoImage(file=self.cwd + "/pix/ok.gif", master=self.root)
            self.b1 = PhotoImage(file=self.cwd + "/pix/linechart.gif", master=self.root)
            self.b2 = PhotoImage(file=self.cwd + "/pix/heatmap.gif", master=self.root)
            self.b3 = PhotoImage(file=self.cwd + "/pix/stacked.gif", master=self.root)
            self.b4 = PhotoImage(file=self.cwd + "/pix/barchart.gif", master=self.root)
            self.wizard = PhotoImage(file=self.cwd + "/pix/chromoWIZ_logo_vt1_2.gif", master=self.root)
        except Exception:
            pass
        self.button1 = None
        self.button2 = None
        self.button3 = None
        self.button4 = None
        try:
            self.root.title("CHROMOWIZ v0.4") 
        except Exception:
            pass
        self.scale = None
        self.button = None
        try:
            self.root.bind("<Key>", self.keyEvent)
        except Exception:
            pass
        if(self.image_export_possible == True):
            self.image1 = Image.new("RGB", (self.image1Width, self.image1Height), (255, 255, 255))
            self.draw = ImageDraw.Draw(self.image1)
        try:
            self.root.option_add('*tearOff', FALSE)
        except Exception:
            pass
        self.lineChart = False
        self.init = True
        try:
            self.createMenu(self.display)
            self.setFullScreen()
        except Exception:
            pass
# **********************************************************************************************
#   
def check_m(m):
    try:
        assert(m == "% bp" or m == "# per Mb")
    except AssertionError:
        print "ERROR", "check_m", "only '% bp' and '# per Mb' are possible for parameter 'm'"
        sys.exit(-1)
        
def check_d(d):
    try:
        assert(os.path.exists(d))
    except AssertionError:
        print "ERROR", "check_d", "directory does not exist", sys.exc_info()
        sys.exit(-1)

def check_o(o):
    #assert(os.path.exists(o))
    pass

def check_t(t, d):
    tables = sqlite_methods.getAllTableNames(d)
    t_found = False
    for table in tables:
        if t == table[0]:
            t_found = True
    try:
        assert(t_found == True)
    except AssertionError:
        print "ERROR", "check_t", "table " + d + " does not exist"
        sys.exit(-1)

def check_x(d, t, c, m, x):
    x = str(x).split(",")

    try:
        assert(len(x) == len(c))
    except AssertionError:
        print "ERROR", "check_x", "number of max values has to be identical with the amount of calculation identifier e.g. '-x 10,20' and '-c X,Y'"
        sys.exit(-1)
    nmb_c = len(c)
    
    for i in range(0, nmb_c):
        max = sqlite_methods.getMaxValueFromDatabase(d, t, c[i], m)
        if(x[i] != "999999"):
            try:
                assert(float(x[i]) <= float(max))
            except AssertionError:
                print "ERROR", "check_x", "specified max value '-x ' has to be lower than max value of all values for the specified calculation identifier", x[i], max
                sys.exit(-1)
def check_c_s(c, t, d, s):
    for c_cur in c:
        set_ids = sqlite_methods.getSetIds(d, t)
        c_found = False
        for set_id in set_ids:
            if c_cur == set_id[0]:
                c_found = True
        if((c_cur.find("N_percent") == -1)):
            if(c_cur != "all"):
                assert(c_found == True)
            for s_cur in s:
                if(s_cur != "all" and s_cur[0] != "all"):
                    seq_ids = sqlite_methods.getSeqIds(d, t, set_id[0])
                    s_found = False
                    for seq_id in seq_ids:
                        if(s_cur == seq_id[0]):
                            s_found = True
                    try:
                        assert(s_found == True)
                    except AssertionError:
                        "ERROR", "check_c_s", "sequence ", s_cur, "does not exist"
                        sys.exit(-1)

def check_heatmaps(m, d, o, t, c, s, x):
    check_m(m)
    check_d(d)
    check_o(o)
    check_t(t, d)
    check_c_s(c, t, d, s)
    #check_x(d, t, c, m, x)

def check_stacked(m, d, o, t, c, s):
    check_m(m)
    check_d(d)
    check_o(o)
    check_t(t, d)
#    check_c_s(c, t, d, s)
    
def check_linecharts(m, d, o, t, c, s, x):
    check_m(m)
    check_d(d)
    check_o(o)
    check_t(t, d)
    check_c_s(c, t, d, s)
    #check_x(d, t, c, m, x)
    
def check_barcharts(d, o, t, c, s):
    check_d(d)
    check_o(o)
    check_t(t, d)
    check_c_s(c, t, d, s)

def check_display_mode(m, d, o, t, c, s, x, v):
    assert(v == "heatmap" or v == "stacked" or v == "linechart" or v == "barchart")
    if(v == "heatmap"):
        check_heatmaps(m, d, o, t, c, s, x)
    elif(v == "stacked"):
        check_stacked(m, d, o, t, c, s)
    elif(v == "linechart"):
        check_linecharts(m, d, o, t, c, s, x)
    elif(v == "barchart"):
        check_barcharts(d, o, t, c, s)

# **********************************************************************************************
  
def start2(filePath, seq_ids, set_id_A, density_table, display, db_file, max, set_ids, display_mode, set_id_names, min_intensity, gap_allowed, block_export_file_path=None, ranges=None, label=None, xmode=None):

     check_display_mode(display, db_file, filePath, density_table, set_ids, seq_ids, max, display_mode)
     
     is_linechart = False
     if((set_id_A) != None):
           set_ids = set_id_A.split(",")

     if(set_ids == "all" or set_ids[0] == "all"):
         _set_ids = sqlite_methods.getSetIds(db_file, density_table)
         set_ids = []
         for _set_id in _set_ids:
             set_ids.append(_set_id[0])
     _filePath = filePath
     set_ids_concat = ""
     for set_id_A in set_ids:
         set_ids_concat = set_ids_concat + "" + set_id_A
     for set_id_A in set_ids:
         if(display_mode == "linechart"):
             is_linechart = True
             display_mode = "heatmap"
             filePath = _filePath
             if(max == "-1"):
                 max = "999999"
         heatMap = HeatMap("", "", "")
         heatMap.label_to_display = label
         if(is_linechart == True):
             heatMap.lineChart = True
             if(gap_allowed != None):
                 try:
                     heatMap.rel_allowed_gap.set(int(gap_allowed))
                 except Exception:
                     heatMap.rel_allowed_gap_var = int(gap_allowed)
             if(min_intensity != None):
                 try:
                     heatMap.rel_syn_value.set(int(min_intensity))
                 except Exception:
                     heatMap.rel_syn_value_var = (int(min_intensity))
         heatMap.density_table = density_table
         heatMap.display = display
         heatMap.db_file = db_file
         heatMap.cmd_line = True
    
         heatMap.psheight = 12000
         heatMap.pswidth = 12000
         heatMap.pswidthExport = 12000
         heatMap.set_id_A = set_id_A
         heatMap.nmb_max = None
                 
         if(display_mode == "heatmap" or display_mode == "barchart"):
             if(seq_ids[0] != "all"):
                 heatMap.seq_ids = seq_ids
             else:
                 seq_ids_2 = []
                 seq_ids_2 = sqlite_methods.getSeqIds(db_file, density_table, set_id_A)
                 for seq_id in seq_ids_2:
                     c_seq_id = seq_id[0]
                     heatMap.seq_ids.append(c_seq_id)
             if(display_mode != "barchart"):
                 max = int(max)
         try:
             heatMap.InitializeCanvas()
             heatMap.AddButton()
         except Exception:
             pass
         heatMap.image1Height = 15000
         heatMap.image1Width = 30000
         
         if(display_mode == "heatmap"):
             try:
                 if(int(max) != -1):
                     heatMap.scale.set(max)
                 else:
                     heatMap.scale.set(999999)
             except Exception:
                 print "ERROR", "start2", "parameter -x not supported, using absolute max per sequence"
                 pass
             redraw.RedrawHeatmap(heatMap, ranges)
             if(is_linechart == True):
                 if(block_export_file_path != None):
                     heatMap.set_id_A = set_id_A
                     block_export_file_path = block_export_file_path + "/" + set_id_A
                     try:
                         heatMap.GetStatistics(False, block_export_file_path)
                     except Exception:
                         print "ERROR", "GetStatistics", sys.exc_info()
                         pass
                         sys.exit()
         else:
             if(display_mode == "barchart"):
                 heatMap.SetIdList = set_ids
                 heatMap.set_id_A = heatMap.SetIdList[0]
                 c_max = None
                 try:
                    heatMap.bin_start = ranges[0]
                    heatMap.bin_stop = ranges[1]
                 except Exception:
                    pass
                 redraw.RedrawBarChart(heatMap, True, None, None, None, None, None, ranges)
             elif(display_mode == "stacked"):
                 seq_ids = sqlite_methods.getSeqIds(db_file, density_table, set_ids[0])
                 for seq_id in seq_ids:
                     heatMap.seq_ids.append(seq_id[0])
                 heatMap.anno_ids = set_ids
                 heatMapSize = 30
                 try:
                     heatMap.GapBetweenSequences.set(0)
                 except Exception:
                     heatMap.gapBetweenSequences = 0
                     pass
                 if(max != None and max != -1):
                     max_values = None
                     if(max.find(",") != -1):
                         max_values = max.split(",")
                     if(len(max_values) == len(seq_ids) and xmode == "seq"):
                         i = 0
                         print "INFO", "start2", "seq_id_constraint"
                         for seq_id in seq_ids:
                             if(max_values == None):
                                 cur_max = "999999"
                             else:
                                 cur_max = max_values[i]
                             heatMap.anno_ids_mItensities[seq_id[0]] = {}
                             heatMap.anno_ids_mItensities[seq_id[0]]["cur"] = int(cur_max)
                             i = i + 1
                     if(len(max_values) == len(set_ids) and xmode == "set"):
                         i = 0
                         print "INFO", "start2", "set_id_constraint"
                         for set_id in set_ids:
                             if(max_values == None):
                                 cur_max = "999999"
                             else:
                                 cur_max = max_values[i]
                             heatMap.anno_ids_mItensities[set_id] = {}
                             heatMap.anno_ids_mItensities[set_id]["cur"] = int(cur_max)
                             i = i + 1
                     if(xmode == "single"):
                         print "INFO", "start2", "seq_id+set_id (single track) constraint"
                         i=0
                         for seq_id in seq_ids:
                             for set_id in set_ids:
                                 cur_max=max_values[i]
                                 heatMap.anno_ids_mItensities[seq_id[0] + "_" + set_id] = {}
                                 heatMap.anno_ids_mItensities[seq_id[0] + "_" + set_id]["cur"] = int(cur_max)
                                 print "INFO", "max value for", set_id, seq_id[0], "is", int(cur_max)
                                 i=i+1
                 redraw.RedrawStackedHeatmap(heatMap, heatMapSize, ranges)
        
         block_export_file_path = filePath
         
         try:
             if(gap_allowed != None):
                 heatMap.rel_allowed_gap.set(int(gap_allowed))
             if(min_intensity != None):
                 heatMap.rel_syn_value.set(int(min_intensity))
         except Exception:
             pass
         
         if(str(filePath).endswith(".jpeg")):
             heatMap.export(filePath)
         elif(str(filePath).endswith(".png")):
             heatMap.export(filePath)
         elif(str(filePath).endswith(".pdf")):
             heatMap.export(filePath)
         else:
             filePath = filePath + ".jpeg"
             heatMap.export(filePath)
         if(display_mode == "barchart"):
             return        
         elif(display_mode == "stacked"):
             return

def start():
     heatMap = HeatMap("", "", "")
     heatMap.root.mainloop()

             
if __name__ == "__main__":
    args = sys.argv[1:]
    optlist, args = getopt.getopt(sys.argv[1:], "y:l:s:c:t:m:d:o:x:c:v:c:a:b:c:r:", ['xmode=', 'label=',
                                                                  'seq=',
                                                                  'set=',
                                                                  'dens=',
                                                                  'mode=',
                                                                  'db=',
                                                                  'output=',
                                                                  'max=',
                                                                  'set_ids=',
                                                                  'display-mode=',
                                                                  'set-id-names=',
                                                                  'min_intensity=',
                                                                  'gap_allowed=',
                                                                  'block_export_file_path='])
    filePath = None
    seq_ids = None
    set_id_A = None
    set_ids = None
    density_table = None
    display = None
    db_file = None
    display_mode = None
    max = None
    set_id_names = None
    min_intensity = None
    gap_allowed = None
    block_export_file_path = None
    label = None
    xmode = None
    
    r_start = -1
    r_stop = -1
    
    ranges = []
    for i in range(0, len(optlist)):
        value = optlist[i][1]
        value = value.strip()
        if(optlist[i][0] in ("-s", "--seq")):
            seq_ids = value
            seq_ids = seq_ids.split(",")
        elif(optlist[i][0] in("-c", "--set_ids")):
            set_ids = value
            set_ids = set_ids.split(",")
        elif(optlist[i][0] in("-l", "--label")):
            label = value
        elif(optlist[i][0] in("-y", "--xmode")):
            xmode = value
            assert(xmode == None or xmode == "seq" or xmode == "set" or xmode == "single")
        elif(optlist[i][0] in ("-c", "--set")):
            set_id_A = value
        elif(optlist[i][0] in ("-t", "--dens")):
            density_table = value
        elif(optlist[i][0] in ("-m", "--mode")):
            display = value
            assert(value == "p" or value == "a")
            if(value == "p"):
                display = "% bp"
            elif(value == "a"):
                display = "# per Mb"
        elif(optlist[i][0] in ("-d", "--db")):
            db_file = value
        elif(optlist[i][0] in ("-r")):
            pairs = value.split(",")
            for pair in pairs:
                coords = pair.split(":")
                try:
                    assert(int(coords[0] > 0))
                    assert(int(coords[1] > 0))
                    assert(int(coords[0]) < int(coords[1]))
                    ranges.append(coords[0])
                    ranges.append(coords[1])
                except Exception:
                    print "ERROR", "range format not supported", "example: '-r 1:10' where '1'=start position in MB and '10'=stop position in MB"
        elif(optlist[i][0] in ("-o", "--output")):
            filePath = value
        elif(optlist[i][0] in ("-x", "--max")):
            max = (value)
        elif(optlist[i][0] in ("-v", "--display-mode")):
            display_mode = value
        elif(optlist[i][0] == "--min_intensity"):
            min_intensity = value
        elif(optlist[i][0] == "--gap_allowed"):
            gap_allowed = value
        elif(optlist[i][0] == "--block_export_file_path"):
            block_export_file_path = value
        if(optlist[i][0] in ("-c", "--set-id-names")):
            set_id_names = value
    if(len(optlist) == 0):
        start()
    else:
        if(display_mode == "barchart"):
            assert(max == None)
        #max=-1
        block_export_file_path, ranges, label, xmode
        start2(filePath, seq_ids, set_id_A, density_table, display, db_file, max, set_ids, display_mode, set_id_names, min_intensity, gap_allowed, block_export_file_path, ranges, label, xmode)
