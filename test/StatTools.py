#!/usr/bin/python

from Tkinter import *
from matplotlib import cm as CM, rc
from matplotlib.colors import ListedColormap
from matplotlib.pylab import meshgrid, rcParams, hist, colorbar, show, scatter, \
    figure, pie, figure, show, legend, linspace, setp, title, subplot, plot, savefig, \
    save, boxplot, arange, yticks, xlabel, ylabel, title, text, axvline, close
from scipy.stats import spearmanr
from tkColorChooser import askcolor, askcolor
from tkFileDialog import askopenfilename, asksaveasfilename
import numpy as NP
import numpy as np
import sqlite_methods
import tkSimpleDialog

class notebook:
    def __init__(self, master, side=LEFT):
        
        self.active_fr = None
        self.count = 0
        self.choice = IntVar(0)

        if side in (TOP, BOTTOM):
            self.side = LEFT
        else:
            self.side = TOP

        self.rb_fr = Frame(master, borderwidth=2, relief=RIDGE)
        self.rb_fr.pack(side=side, fill=BOTH)
        self.screen_fr = Frame(master, borderwidth=2, relief=RIDGE)
        self.screen_fr.pack(fill=BOTH)
        

    def __call__(self):
        return self.screen_fr

        
    def add_screen(self, fr, title):
        
        b = Radiobutton(self.rb_fr, text=title, indicatoron=0, \
            variable=self.choice, value=self.count, \
            command=lambda: self.display(fr))
        b.pack(fill=BOTH, side=self.side)
        
        if not self.active_fr:
            fr.pack(fill=BOTH, expand=1)
            self.active_fr = fr

        self.count += 1
        return b

    def display(self, fr):
        
        self.active_fr.forget()
        fr.pack(fill=BOTH, expand=1)
        self.active_fr = fr

class StatTools:

    def ChangeColor(self):
        (rgb, hexval) = askcolor()
           
        if(hexval != None):
            self.chromosomal_structure_colors[int(self.v.get()) - 1] = str(hexval).upper()
            self.colors[int(self.v.get()) - 1]["background"] = str(hexval).upper()
            
    def get_values(self, anno_id, seq_id, mode, lower=None, upper=None):
        values_map = []
        values = sqlite_methods.getValuesFromDatabase(self.db_file, self.density_table, anno_id, seq_id)
        N_values = sqlite_methods.getNPercentFromDatabase(self.db_file, self.density_table, anno_id, seq_id)
        
        assert(len(values) == len(N_values))
        
        max_block_size = 0  
        for i in range(0, len(values)):
            if(lower == None or (int(values[i][1]) >= int(lower) and int(values[i][2] <= int(upper)))):
                if(i == 0):
                    max_block_size = values[0][5]
                if(int(N_values[i][0]) > 60 or int(values[i][5]) < (max_block_size * 0.2)):
                    values_map.append(-1)
                else:
                    if(mode == "ApB"):
                        if(values[i][7] != None):
                            values_map.append(values[i][7])
                    elif(mode == "PpB"):
                        if(values[i][9] != None):
                            values_map.append(values[i][9])
        return values_map
    
    def length(self):
        if(self.radio4_v4.get() == False):
            self.length_values = {}

        anno_id = self.variable72.get()
        seq_id = self.variable71.get()

        seq_len = None
        
        if(seq_id == "all"):
            seq_len = sqlite_methods.getAmountAllAnnotations(self.db_file, anno_id, self.anno_table)
        else:
            seq_len = sqlite_methods.getAmountAnnotations(self.db_file, anno_id, self.anno_table, seq_id)
        
        seq_len = seq_len[0]
        
        if(seq_id == "all"):
            anno_ids = sqlite_methods.getAllAnnotations(self.db_file, anno_id, self.anno_table)
        else:
            anno_ids = sqlite_methods.getAnnotations(self.db_file, anno_id, self.anno_table, seq_id)
        
        b = [0] * seq_len 
        b_2 = [0] * ((seq_len) / 10000)
        
        b_3 = [0] * seq_len 
        b_4 = [0] * ((seq_len) / 10000)
        
         
        a = []

        for anno_id_entry in anno_ids:
            a.append(abs(anno_id_entry[2] - anno_id_entry[1]))
            
            start = anno_id_entry[1]
            stop = anno_id_entry[2]
            
            assert(int(start) <= int(stop))
            
            b[int(anno_id_entry[2]) - 1] = b[int(anno_id_entry[2]) - 1] + 1
            
            for i in range(start, stop):
                b_3[i] = b_3[i] + 1
                
        for i in range(0, seq_len / 10000):
            start = i * seq_len / 10000
            stop = (i + 1) * seq_len / 10000
            
            sum_nmb = sum(b[start:stop + 1])
            
            b_2[i] = sum_nmb
            
            sum_nmb = sum(b_3[start:stop + 1])
            
            b_4[i] = sum_nmb
            
        self.length_values[anno_id + "\t" + seq_id] = a

        colors = ['r', 'g', 'b', 'y', 'c']
        
        index = 0
        bins = int(self.variable73.get())
        
        subplot(511)
  
        plot(a)
        
        subplot(512)
        
        plot(b_2)

        subplot(513)

        plot(b_4)
        
        subplot(514)

        hist(b_2, bins=bins)
        
        subplot(515)

        hist(b_4, bins=bins)
        
        show()

    def stats(self, data):
         sum = 0.0
         for value in data:
             sum += value
         mean = sum / len(data)
         sum = 0.0
         for value in data:
             sum += (value - mean) ** 2
         variance = sum / (len(data) - 1)
         return (mean, variance)

    def length2(self):
        anno_id = self.variable72.get()
        seq_id = self.variable71.get()
        bins = int(self.variable73.get())
        seq_len = None
        
        if(seq_id == "all"):
            seq_len = sqlite_methods.getAmountAllAnnotations(self.db_file, anno_id, self.anno_table)
        else:
            seq_len = sqlite_methods.getAmountAnnotations(self.db_file, anno_id, self.anno_table, seq_id)
        
        seq_len = seq_len[0]
        
        if(seq_id == "all"):
            anno_ids = sqlite_methods.getAllAnnotations(self.db_file, anno_id, self.anno_table)
        else:
            anno_ids = sqlite_methods.getAnnotations(self.db_file, anno_id, self.anno_table, seq_id)
        
        b = [0] * seq_len 
        b_3 = []
        for anno_id_entry in anno_ids:
            values = str(anno_id_entry[3]).split(";")
            i = 0
            elmn_len = 0
            while i < len(values) - 1:
                elmn_len = elmn_len + int(values[i + 1]) - int(values[i]) + 1
                i = i + 2
            b[anno_id_entry[1]] = elmn_len
            b_3.append(elmn_len)

        stats = self.stats(b_3)

        mean = stats[0]
        sigma = stats[1] ** 0.5

        mean_b_3 = sum(b_3) / len(b_3)
        h = hist(b_3, bins=bins)
        label2 = str(anno_id) + "_" + str(seq_id)
        title(r'' + str(label2) + '(' + str(int(mean)) + ',' + str(int(sigma)) + ')')
        xlabel('Block #')
        ylabel('PpB')
        
        show()

    def distribution1(self):
        if(self.radio2_v2.get() == False):
            self.distribution1_values = {}

        anno_id = self.variable61.get()
        seq_id = self.variable62.get()
        mode = self.variable63.get()
        
        values = self.get_values(anno_id, seq_id, mode)
        #values = self.normalize_data(values)
        
        values_all = []
        x_values_all = []
        
        index = 0
        for value in values:
            values_all.append(int(value))
            x_values_all.append(index)
            index = index + 1
            
        coefficients = NP.polyfit(x_values_all, values_all, 1)
        polynomial = NP.poly1d(coefficients)
        ys = polynomial(x_values_all)

        coefficients2 = NP.polyfit(x_values_all, values_all, 2)
        polynomial2 = NP.poly1d(coefficients2)
        ys2 = polynomial2(x_values_all)

        coefficients3 = NP.polyfit(x_values_all, values_all, 3)
        polynomial3 = NP.poly1d(coefficients3)
        ys3 = polynomial2(x_values_all)

        _label = seq_id + " " + anno_id 
        
        for key in self.distribution1_values.keys():
            plot(self.distribution1_values[key]["1"], label=key)
            #plot(self.distribution1_values[key]["2"],label=key)
            #plot(self.distribution1_values[key]["3"],label=key)
            #plot(self.distribution1_values[key]["4"],label=key)

        plot(x_values_all, values_all, label=_label)
        #plot(x_values_all, ys)
        #plot(x_values_all, ys2)
        #plot(x_values_all, ys3)
        
        self.distribution1_values[_label] = {}
        self.distribution1_values[_label]["1"] = values_all
        self.distribution1_values[_label]["2"] = ys
        self.distribution1_values[_label]["3"] = ys2
        self.distribution1_values[_label]["4"] = ys3
        
        legend(loc='upper left')
        show()
        
    def histogram1(self):
        fig = figure(1, (15, 12))
        ax = fig.add_subplot(111)
        
        if(self.radio1_v1.get() == False):
            self.histogram1_values = {}
        
        anno_id = self.variable51.get()
        seq_id = self.variable52.get()
        mode = self.variable53.get()
        
        values = self.get_values(anno_id, seq_id, mode)
        
        a = []
        bins = 100
        
        for value in values:
            elmn_len = float(value)
            a.append(elmn_len)
        
        self.histogram1_values[anno_id + "\t" + seq_id] = a

        colors = ['r', 'g', 'b', 'y', 'c']
        
        index = 0
        for key in self.histogram1_values.keys():
            n, bins, patches = hist(self.histogram1_values[key], bins)
            setp(patches, 'facecolor', colors[index % len(colors)], 'alpha', 0.75)

            index = index + 1
        
        
        if(mode == "ApB"):        
            xlabel("# per MB", fontsize=40)
        else:
            xlabel("% bp", fontsize=40)
                
        ylabel("# blocks", fontsize=40)
        
        
        for label in ax.xaxis.get_ticklabels():
            label.set_fontsize(40)

        for label in ax.yaxis.get_ticklabels():
            label.set_fontsize(40)

        anno_id = str(anno_id).split("__")[1]
        
        savefig(anno_id + "_" + seq_id + "_" + mode + "_histogram.png", dpi=300)  
          
        title(anno_id, fontsize=40)
        show()
        
    def change_state_v1(self):
        value = self.radio1_v1.get()
        
        if(value == False):
            value = True
            self.radio1.deselect()
        else:
            value = False
            self.radio1.select()    
        
    def change_state_v2(self):
        value = self.radio2_v2.get()
        
        if(value == False):
            value = True
            self.radio2.deselect()
        else:
            value = False
            self.radio2.select()    

    def change_state_v4(self):
        value = self.radio4_v4.get()
        
        if(value == False):
            value = True
            self.radio4.deselect()
        else:
            value = False
            self.radio4.select()    


    def change_state_v3(self):
        value = self.radio3_v3.get()
        
        if(value == False):
            value = True
            self.radio3.deselect()
        else:
            value = False
            self.radio3.select()    

    def structure(self):
        values = sqlite_methods.getDensitiesDistribution(self.db_file, self.density_table)
        
        allowed_set_ids = []
        colors = []
        colorsMap = {}
        
        if(len(self.variable5.get())):
            allowed_set_ids.append(self.variable5.get())
#            colors.append(self.colors[0]["background"])
            colorsMap[self.variable5.get()] = self.colors[0]["background"]
        if(len(self.variable6.get())):
            allowed_set_ids.append(self.variable6.get())
#            colors.append(self.colors[1]["background"])
            colorsMap[self.variable6.get()] = self.colors[1]["background"]
        if(len(self.variable7.get())):
            allowed_set_ids.append(self.variable7.get())
#            colors.append(self.colors[2]["background"])
            colorsMap[self.variable7.get()] = self.colors[2]["background"]
        if(len(self.variable8.get())):
            allowed_set_ids.append(self.variable8.get())
#            colors.append(self.colors[3]["background"])
            colorsMap[self.variable8.get()] = self.colors[3]["background"]
        if(len(self.variable9.get())):
            allowed_set_ids.append(self.variable9.get())
#            colors.append(self.colors[4]["background"])
            colorsMap[self.variable9.get()] = self.colors[4]["background"]
        
        seq_id_selected = self.variable21.get()
        
        intensities = []
        labels = []
        undefined = 100.0
        
        for value in values:
            label = value[1]
            if(label in allowed_set_ids):
                colors.append(colorsMap[label])
                label = str(label).split("__")[1]
                labels.append(label)
                intensities.append(value[0])
                undefined = undefined - float(value[0])
                
        if(float(undefined) > 0):
            labels.append("undefined")
            intensities.append(undefined)
            colors.append("gray")

        seq_ids = sqlite_methods.getSeqIds(self.db_file, self.density_table, allowed_set_ids[0])
        
        if(seq_id_selected != "total"):
            if(len(seq_ids) <= 5):
                figure(figsize=(3 * (len(seq_ids) + 1), 4 * len(seq_ids) + 1), facecolor='white')
            else:
                figure(figsize=(2 * (len(seq_ids) + 1), 4 * len(seq_ids) + 1), facecolor='white')
        else:
            figure(facecolor='white')
            
        c_position = 1
        if(seq_id_selected != "total"):
            subplot((len(seq_ids) + 1) / 2 + 1, 2, c_position)

        title("total")
        c_position = c_position + 1
        
        _autopct = '%1.f%%' #None
        _show_label = False
        
        if(_show_label == True):
            pie(intensities, labels=labels, autopct=_autopct, colors=colors)
        else:
            pie(intensities, labels=None, autopct=_autopct, colors=colors)
                
        if(seq_id_selected != "total"):
            
            values = sqlite_methods.getDensitiesDistributionPerChr(self.db_file, self.density_table)

            c_seq_id = ""
    
            intensities = []
            labels = []
            undefined = 100.0
            
            for value in values:
                label = value[1]
                if(label in allowed_set_ids):
                    if(len(c_seq_id) == 0):
                        c_seq_id = str(value[2])
                    if(c_seq_id != str(value[2])):
                        old_seq_id = c_seq_id
                        c_seq_id = str(value[2])

                        labels.append("undefined")
                        intensities.append(undefined)
                        
                        subplot((len(seq_ids) + 1) / 2 + 1, 2, c_position)
                        c_position = c_position + 1
                        title(old_seq_id)
                        colors.append("gray")
                       
                        if(_show_label == True):
                            pie(intensities, labels=labels, autopct=_autopct, colors=colors)
                        else:
                            pie(intensities, labels=None, autopct=_autopct, colors=colors)
                        intensities = []
                        labels = []
                        intensities.append(value[0])
                        
                        colors = []
                        colors.append(colorsMap[label])
                        label = str(label).split("__")[1]
                        labels.append(label)
                        undefined = 100.0
                        undefined = undefined - float(value[0])
                    else:
                        colors.append(colorsMap[label])
                        label = str(label).split("__")[1]
                        labels.append(label)
                        intensities.append(value[0])
                        undefined = undefined - float(value[0])
                            
            if(len(intensities) > 0):
                labels.append("undefined")
                intensities.append(undefined)
                subplot((len(seq_ids) + 1) / 2 + 1, 2, c_position)
                c_position = c_position + 1
                title(c_seq_id)
                if(_show_label == True):
                    pie(intensities, labels=labels, autopct=_autopct, colors=colors)
                else:
                    pie(intensities, labels=None, autopct=_autopct, colors=colors)
                    
        if(seq_id_selected != "total"):
            rcParams['font.size'] = 20.0
            rcParams['axes.titlesize'] = 16.0
            rcParams['xtick.labelsize'] = 20.0
            rcParams['legend.fontsize'] = 20.0
        else:
            rcParams['font.size'] = 40.0
            rcParams['axes.titlesize'] = 32.0
            rcParams['xtick.labelsize'] = 40.0
            rcParams['legend.fontsize'] = 40.0
    
        savefig(self.density_table + "_structure.png")    
        show()
        
    def scatterplot(self):
        anno_id1 = self.variable1.get()
        anno_id2 = self.variable3.get()
        seq_id = self.variable2.get()
        mode1 = self.variable41.get()
        mode2 = self.variable41.get()
        labels = []
        
        if(self.radio3_v3.get() == False):
            self.scatterplot_values = {}
        
        a = []
        b = []

        if(seq_id == "all"):
            seq_ids = sqlite_methods.getSeqIds(self.db_file, self.density_table, anno_id1)
            
            for seq_id in seq_ids:
                a = []
                b = []
                values = self.get_values(anno_id1, seq_id[0], mode1)
        
                for value in values:
                    v1 = int(value)
                    a.append(v1)
                values = self.get_values(anno_id2, seq_id[0], mode1)
                
                for value in values:
                    v1 = int(value)
                    b.append(v1)

                self.scatterplot_values[anno_id1 + "\t" + anno_id2 + "\t" + seq_id[0]] = {}
                self.scatterplot_values[anno_id1 + "\t" + anno_id2 + "\t" + seq_id[0]]["A"] = a
                self.scatterplot_values[anno_id1 + "\t" + anno_id2 + "\t" + seq_id[0]]["B"] = b

                labels.append(seq_id[0])
        else:
            values = self.get_values(anno_id1, seq_id, mode1)
            for value in values:
                v1 = int(value)
                a.append(v1)

            values = self.get_values(anno_id2, seq_id, mode1)
            for value in values:
                v1 = int(value)
                b.append(v1)

            self.scatterplot_values[anno_id1 + "\t" + anno_id2 + "\t" + seq_id] = {}
            self.scatterplot_values[anno_id1 + "\t" + anno_id2 + "\t" + seq_id]["A"] = a
            self.scatterplot_values[anno_id1 + "\t" + anno_id2 + "\t" + seq_id]["B"] = b

            labels.append(seq_id)
                
        index = 0
        
        colors = ['r', 'g', 'b', 'y', 'c']
        
        index = 0
        
        for key in self.scatterplot_values.keys():
            a = self.scatterplot_values[key]["A"]
            b = self.scatterplot_values[key]["B"]
            
            scatter(a, b, c=colors[index % len(colors)], label=labels[index % len(labels)])
            
            index = index + 1
            
        legend(loc='lower left') 

        title("Scatterplot")
        xlabel(anno_id1)
        ylabel(anno_id2)

        show()
        
    def set_density_table(self, density_table):
        self.density_table = density_table
        
    def set_db_file(self, db_file):
        self.db_file = db_file

    def correlations(self, mode1=None, mode2=None, min_border=0, max_border=0, enable_window=True, enable_diff_matrix=True):
        if(mode1 == None):
            mode1 = self.variable42.get()
        
        if(mode2 == None):
            mode2 = self.variable42.get()
        
        set_ids = set_ids = self.e44.get(0, END)
        
        amount_seqs = -1
        for set_id in set_ids:
            seq_ids = sqlite_methods.getSeqIds(self.db_file, self.density_table, set_id)
            
            if(amount_seqs == -1):
                amount_seqs = len(seq_ids)
            
            assert(amount_seqs == len(seq_ids))

        nmb_elements = len(set_ids) * len(set_ids)
        
        A = NP.random.randint(len(set_ids), nmb_elements, nmb_elements).reshape(len(set_ids), len(set_ids)) 

        for x in range(0, len(set_ids)):
            for y in range(0, len(set_ids)):
                A[x][y] = 0
            
        boxplot_map = {}
        
        remove_half = False 

        fig = figure()         
        
        for seq_id in seq_ids:
            for x in range(0, len(set_ids)):
                for y in range(0, len(set_ids)):
                    
                    values_A = self.get_values(set_ids[x], seq_id[0], mode1)
                    values_B = values = self.get_values(set_ids[y], seq_id[0], mode2)
                    nmb_A = []
                    nmb_B = []
                    nmb_excluded = 0
                        
                    try:
                        assert(len(values_A) == len(values_B))
                        for i in range(0, len(values_A)):
                            if(values_A[i] == -1 or values_B[i] == -1):
                                nmb_excluded = nmb_excluded + 1
                            else:
                                nmb_A.append(values_A[i])
                                nmb_B.append(values_B[i])
                            
                        r = spearmanr(nmb_A, nmb_B)[0]
                        A[x][y] = A[x][y] + int(100.0 * r)
                    except AssertionError:
                        print sys.exc_info()
                        pass
                    except Exception:
                        print sys.exc_info()
                        pass
                    
        A = A / (100.0 * len(seq_ids))
        
        for x in range(0, len(set_ids)):
            cor_line = ""
            for y in range(0, len(set_ids)):
                if(len(cor_line) == 0):
                    cor_line = str(A[x][y])
                else:
                    cor_line = cor_line + ";" + str(A[x][y])

        subplot_index = 111
        
        enable_diff_matrix = False
        
        if(enable_diff_matrix == True):
            if(self.matrixes_previous != None):
                subplot_index += 200
                ax1 = subplot(subplot_index)
                subplot_index = subplot_index + 1
                C = abs(self.matrixes_previous - A)
                cmap = CM.get_cmap('jet', 10) 
                cmap.set_bad('w') 
                axim1 = ax1.imshow(C, interpolation="nearest", cmap=CM.gray) # bilinear, bicubic also possible
                ax1.grid(False)
                colorbar(axim1, orientation='vertical')
                ax12 = subplot(subplot_index)
                subplot_index = subplot_index + 1
                axim12 = ax12.imshow(self.matrixes_previous, interpolation="nearest", cmap=cmap) # bilinear, bicubic also possible
                ax12.grid(False)
                colorbar(axim12, orientation='vertical')
                
            self.matrixes_previous = A
        
        if(remove_half == True):
            mask = NP.tri(A.shape[0], k= -1) 

            for x in range(0, len(set_ids)):
                for y in range(0, len(set_ids)):
                    if(x == y):
                        mask[x][y] = 1
                    elif(not(float(A[x][y]) <= float(min_border) or float(A[x][y]) >= float(max_border))):
                        mask[x][y] = 1
       
            A = NP.ma.array(A, mask=mask) 
            
        cmap = CM.get_cmap('jet', 10) 
        cmap.set_bad('w') 
        
        for x in range(0, len(set_ids)):
            label1 = str(set_ids[len(set_ids) - x - 1]).split("__")[1]
            label2 = str(set_ids[x]).split("__")[1]
            
        ax2 = subplot(subplot_index) 
        axim2 = ax2.imshow(A, interpolation="nearest", cmap=cmap) # bilinear, bicubic also possible
        ax2.grid(False) 
        colorbar(axim2, orientation='vertical')
        
        set_id_display = []
        
        for set_id in set_ids:
            set_id_display.append(set_id[0])
            
        savefig(self.density_table + "_" + mode1 + "_" + mode2 + ".png")    
        
        if(enable_window == True):
            show()

    def boxplots(self):
        mode1 = self.variable32.get()
        mode2 = self.variable32.get()
                
        lower = self.variable35.get()
        upper = self.variable37.get()
        
        lower = lower.strip()
        upper = upper.strip()
        
        set_id_X = self.variable11.get()

        set_ids = self.e34.get(0, END)#sqlite_methods.getSetIds(self.db_file, self.density_table)

        seq_ids = []
        
        amount_seqs = -1
        seq_ids2 = None
        for set_id in set_ids:
            seq_ids2 = sqlite_methods.getSeqIds(self.db_file, self.density_table, set_id)
            
            if(amount_seqs == -1):
                amount_seqs = len(seq_ids2)
            assert(amount_seqs == len(seq_ids2))
            
        if(self.variable33.get() == "all"):
            for seq_id2 in seq_ids2:
                seq_ids.append(seq_id2[0])
        else:
            seq_ids.append(self.variable33.get())

        nmb_elements = len(set_ids) * len(set_ids)
        boxplot_map = {}

        
        cor_set_map = {}

        for seq_id in seq_ids:
            for y in range(0, len(set_ids)):
                if(len(lower) > 0 and len(upper) > 0):
                    values_A = self.get_values(set_id_X, seq_id, mode1, lower, upper)
                    values_B = values = self.get_values(set_ids[y], seq_id, mode2, lower, upper)
                else:
                    values_A = self.get_values(set_id_X, seq_id, mode1)
                    values_B = values = self.get_values(set_ids[y], seq_id, mode2)
    
                nmb_A = []
                nmb_B = []
                            
                nmb_excluded = 0
                      
                try:
                    assert(len(values_A) == len(values_B))
                                
                    for i in range(0, len(values_A)):
                        if(values_A[i] == -1 or values_B[i] == -1):
                            nmb_excluded = nmb_excluded + 1
                        else:
                            nmb_A.append(values_A[i])
                            nmb_B.append(values_B[i])
                                    
                    r = spearmanr(nmb_A, nmb_B)[0]
                    
                    if(cor_set_map.get(set_ids[y]) == None):
                        cor_set_map[set_ids[y]] = r
                    else:
                        cor_set_map[set_ids[y]] = cor_set_map[set_ids[y]] + r

                    if(boxplot_map.get(set_id_X + "_" + set_ids[y]) == None):
                        boxplot_map[set_id_X + "_" + set_ids[y]] = []
                    boxplot_map[set_id_X + "_" + set_ids[y]].append(r)
                except AssertionError:
                    pass

        boxplot_values = []
        keys = []
        keys = boxplot_map.keys()
        keys.sort()

        for key in keys:
            boxplot_values.append(boxplot_map[key])
            
        ind = arange(len(boxplot_map.keys()))
        b1 = boxplot(boxplot_values, 0, 'rs', 0)
        keys = b1.keys()
        for key in keys:    
            setp(b1[key], color='red') 
            
        yticks(ind + 1., keys)

        savefig(self.density_table + "_" + mode1 + "_" + mode2 + "_boxplot" + ".png")    
        show() 

    def boxplots2(self, show_image=True, export_directory="."):
        mode1 = self.variable32.get()
        mode2 = self.variable32.get()
        lower = self.variable35.get()
        upper = self.variable37.get()
        lower = lower.strip()
        upper = upper.strip()
        
        set_id_X = self.variable11.get()
        set_ids = self.e34.get(0, END)
        seq_ids = []
        amount_seqs = -1

        seq_ids2 = None
        seq_len2 = []
        for set_id in set_ids:
            seq_ids2 = sqlite_methods.getSeqIds(self.db_file, self.density_table, set_id)
            
            if(len(seq_len2) == 0):
                for seq_id2 in seq_ids2:
                    seq_len2.append(sqlite_methods.find_seq_id(self.db_file, seq_id2[0]))
            
            if(amount_seqs == -1):
                amount_seqs = len(seq_ids2)
            try:
                assert(amount_seqs == len(seq_ids2))
            except Exception:
                print "ERROR\t", set_id_X, set_id
        if(self.variable33.get() == "all"):
            for seq_id2 in seq_ids2:
                seq_ids.append(seq_id2[0])
        else:
            seq_ids.append(self.variable33.get())

        nmb_elements = len(set_ids) * len(set_ids)
        boxplot_map = {}
        cor_set_map = {}

        for seq_id in seq_ids:
            for y in range(0, len(set_ids)):
                if(len(lower) > 0 and len(upper) > 0):
                    values_A = self.get_values(set_id_X, seq_id, mode1, lower, upper)
                    values_B = values = self.get_values(set_ids[y], seq_id, mode2, lower, upper)
                else:
                    values_A = self.get_values(set_id_X, seq_id, mode1)
                    values_B = values = self.get_values(set_ids[y], seq_id, mode2)
                
                    
                nmb_A = []
                nmb_B = []
                            
                nmb_excluded = 0
                      
                try:
                    assert(len(values_A) == len(values_B))
                                
                    for i in range(0, len(values_A)):
                        if(values_A[i] == -1 or values_B[i] == -1):
                            nmb_excluded = nmb_excluded + 1
                        else:
                            nmb_A.append(values_A[i])
                            nmb_B.append(values_B[i])
                                    
                    r = spearmanr(nmb_A, nmb_B)[0]
                    
                    set_id_X_shortened = set_id_X.split("__")[1]
                    set_id_Y_shortened = set_ids[y].split("__")[1]
                    #label = set_id_X_shortened + "_vs_" + set_id_Y_shortened
                    label = set_id_Y_shortened
                    
                    if(cor_set_map.get(label) == None):
                        cor_set_map[label] = r
                    else:
                        cor_set_map[label] = cor_set_map[label] + r

                    if(boxplot_map.get(label) == None):
                        boxplot_map[label] = []
                    boxplot_map[label].append(r)
                    
                except AssertionError:
                    pass
                
        names = []
        boxplot_values = {}
        keys = []
        keys = boxplot_map.keys()
        keys.sort()

        nmb_elmn = -1
        for key in keys:
            boxplot_values[key] = (boxplot_map[key])
            if(nmb_elmn == -1):
                nmb_elmn = len(boxplot_values[key])
            
        ind = arange(len(boxplot_map.keys()))
        y = []
        close = []
        color = []
        pos = []
        for j in range(0, len(boxplot_values.keys()) + 1):
            y1 = []
            c1 = []
            col = []
            pos.append(j)
            for i in range(0, nmb_elmn):
                y1.append(int(j))
                c1.append(int(2000 * (seq_len2[i] / float(max(seq_len2)))))
                col.append(i)
            y.append(y1)
            close.append(c1)
            color.append(col)

        fig = figure(1, (40, 10)) 
        ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1.1, 1.1), ylim=(-0.5, len(boxplot_map.keys()) - 0.5))
        fig.subplots_adjust(right=0.7)

        stepSize = 2.0 / float(len(seq_len2))
        
        boxplot_value = []
        for i in range(0, len(seq_ids)):
            boxplot_value.append(-1 + float(i * stepSize))
            ax.text(-1 + float(i * stepSize), len(set_ids) + 0.3, seq_ids[i], fontsize=20)
        boxplot_values[" "] = (boxplot_value)
        
        set_ids_array = []
        
        for set_id in set_ids:
            set_ids_array.append(set_id)
            
        set_ids_array.reverse()
        
        i = 0
        keys_sorted = boxplot_values.keys()

        for key in set_ids_array:
            set_id_Y_shortened = key.split("__")[1]
            ax.scatter(boxplot_values.get(set_id_Y_shortened), y[i], s=close[i], c=color[i])
            i = i + 1
        
        ax.scatter(boxplot_value, y[i], s=close[i], c=color[i])

        axvline(-0.3)
        axvline(0.3)
        axvline(-0.8)
        axvline(0.8)

        try:
            title = self.density_table.split("density_")[1]
        except Exception:
            print sys.exc_info()
            pass
        
        name_map = {}
        name_map["Copia"] = "         Copia"
        name_map["DNA_Transposon"] = "      DNA Transposon"
        name_map["GC_percent"] = "   GC"
        name_map["Gypsy"] = "         Gypsy"
        name_map["LTR_Retrotransposon"] = "      LTR_Retrotransposon"
        name_map["MITE"] = "         MITE"
        name_map["Retroelement"] = "   Retroelement"
        name_map["Satellite"] = "      Satellite"
        name_map["Tandem_Repeats"] = "   Tandem Repeats"
        name_map["non-LTR_Retrotransposons_(RXX)"] = "      non-LTR Retrotransposons"
        name_map["Genes_CDS"] = "   Gene_CDS"
        
        names = []
        for key in set_ids_array:
            set_id_Y_shortened = key.split("__")[1]
            if(name_map.get(set_id_Y_shortened) != None):
                names.append(name_map.get(set_id_Y_shortened))
            else:
                names.append(set_id_Y_shortened)
         
        ytickNames = yticks(pos, names, fontsize=36, horizontalalignment='left')
        
        for tick in ax.yaxis.get_major_ticks():
            tick.label1On = False
            tick.label2On = True
            tick.label2.set_fontsize(32)
            
        for label in ax.xaxis.get_ticklabels():
            label.set_fontsize(32)

        savefig(export_directory + "/" + self.density_table + "_" + set_id_X + "_" + mode1 + ".png", dpi=300)    
        if(show_image == True):
            show() 
        
        fig.clear()
        
    def boxplot1_2(self):
        if(self.e33.selection_get() != None and
           len(self.e33.curselection()) > 0):
           values = self.e33.selection_get().split("\n")
           indexes = self.e33.curselection()
           for i in range(0, len(indexes)):
               self.e34.insert(END, values[len(indexes) - 1 - i])
               self.e33.delete(indexes[len(indexes) - 1 - i], indexes[len(indexes) - 1 - i])
    
    def boxplot2_1(self):
        if(self.e34.selection_get() != None and
           len(self.e34.curselection()) > 0):
           values = self.e34.selection_get().split("\n")
           indexes = self.e34.curselection()
           for i in range(0, len(indexes)):
               self.e33.insert(END, values[len(indexes) - 1 - i])
               self.e34.delete(indexes[len(indexes) - 1 - i], indexes[len(indexes) - 1 - i])
                       
    def correlation1_2(self):
        if(self.e43.selection_get() != None and
           len(self.e43.curselection()) > 0):
           values = self.e43.selection_get().split("\n")
           indexes = self.e43.curselection()
           for i in range(0, len(indexes)):
               self.e44.insert(END, values[len(indexes) - 1 - i])
               self.e43.delete(indexes[len(indexes) - 1 - i], indexes[len(indexes) - 1 - i])
        
    def correlation2_1(self):
        if(self.e44.selection_get() != None and
           len(self.e44.curselection()) > 0):
           values = self.e44.selection_get().split("\n")
           indexes = self.e44.curselection()
           for i in range(0, len(indexes)):
               self.e43.insert(END, values[len(indexes) - 1 - i])
               self.e44.delete(indexes[len(indexes) - 1 - i], indexes[len(indexes) - 1 - i])
        
    def listbox_insert_seqIds(self, listbox, set_ids):
        for i in range(0, len(set_ids) - 1):
            listbox.insert(i, set_ids[i])
    
    def update(self):
        self.db_file = self.variable81.get()
        self.density_table = self.variable82.get()
        self.anno_table = self.variable83.get()

        self.body(self.db_file, self.density_table, self.anno_table, False, True)
        
    def body(self, db_file, density_table, anno_table, run=True, update=False):
            if(update == False):
                self.master = Tk()
                    
                n = notebook(self.master, TOP)
                self.f = Frame(n())
                self.f2 = Frame(n())
                self.f3 = Frame(n())
                self.f4 = Frame(n())
                self.f5 = Frame(n())
                self.f6 = Frame(n())
                self.f7 = Frame(n())
                self.f8 = Frame(n())
                
                self.db_file = db_file
                self.density_table = density_table
                self.anno_table = anno_table
            
                self.scatterplot_values = {}
                self.histogram1_values = {}
                self.histogram2_values = {}
                self.length_values = {}
                self.distribution1_values = {}
                self.distribution2_values = {}
                self.matrixes_previous = None
            
            # ***********************************************************************
            self.variable1 = StringVar(self.f)
            self.variable1.set("")
            self.variable11 = StringVar(self.f)
            self.variable11.set("")
            self.variable2 = StringVar(self.f)
            self.variable2.set("")
            self.variable21 = StringVar(self.f)
            self.variable21.set("")
            self.variable3 = StringVar(self.f)
            self.variable3.set("")
            self.variable32 = StringVar(self.f)
            self.variable32.set("")
            self.variable33 = StringVar(self.f)
            self.variable33.set("")
            self.variable4 = StringVar(self.f)
            self.variable4.set("")
            self.variable5 = StringVar(self.f)
            self.variable5.set("")
            self.variable6 = StringVar(self.f)
            self.variable6.set("")
            self.variable7 = StringVar(self.f)
            self.variable7.set("")
            self.variable8 = StringVar(self.f)
            self.variable8.set("")
            self.variable9 = StringVar(self.f)
            self.variable9.set("")
            self.variable35 = StringVar(self.f)
            self.variable35.set("")
            self.variable37 = StringVar(self.f)
            self.variable37.set("")
            self.variable41 = StringVar(self.f)
            self.variable41.set("")
            self.variable42 = StringVar(self.f)
            self.variable42.set("")
            self.variable51 = StringVar(self.f)
            self.variable51.set("")
            self.variable52 = StringVar(self.f)
            self.variable52.set("")
            self.variable53 = StringVar(self.f)
            self.variable53.set("")
            self.variable61 = StringVar(self.f)
            self.variable61.set("")
            self.variable62 = StringVar(self.f)
            self.variable62.set("")
            self.variable63 = StringVar(self.f)
            self.variable63.set("")
            self.variable71 = StringVar(self.f)
            self.variable71.set("")
            self.variable72 = StringVar(self.f)
            self.variable72.set("")
            self.variable73 = StringVar(self.f)
            self.variable73.set("")
            self.variable81 = StringVar(self.f)
            self.variable81.set("")
            self.variable82 = StringVar(self.f)
            self.variable82.set("")
            self.variable83 = StringVar(self.f)
            self.variable83.set("")
            
            self.options1 = []
            self.options11 = []
            self.options2 = []
            self.options21 = []
            self.options3 = []
            self.options32 = []
            self.options33 = []
            self.options4 = []
            self.options5 = []
            self.options6 = []
            self.options7 = []
            self.options8 = []
            self.options9 = []
            self.options41 = []
            self.options42 = []
            self.options51 = []
            self.options52 = []
            self.options53 = []
            self.options61 = []
            self.options62 = []
            self.options63 = []
            self.options71 = []
            self.options72 = []
            self.options73 = []
            self.options81 = []
            self.options82 = []
            self.options83 = []
            
            
            set_ids = sqlite_methods.getSetIds(self.db_file, self.density_table)
            set_ids.append(["", "\n"])
            
            anno_ids = sqlite_methods.getAnnoIds(self.db_file, self.anno_table)
            
            for anno_id in anno_ids:
                self.options72.append(anno_id[0])
            
            for set_id in set_ids:
                c_set_id = set_id[0]
                self.options1.append(c_set_id)
                self.options3.append(c_set_id)
                self.options5.append(c_set_id)
                self.options6.append(c_set_id)
                self.options7.append(c_set_id)
                self.options8.append(c_set_id)
                self.options9.append(c_set_id)
                self.options11.append(c_set_id)
                self.options51.append(c_set_id)
                self.options61.append(c_set_id)

            self.options32.append("PpB")
            self.options32.append("ApB")
            self.options41.append("PpB")
            self.options41.append("ApB")
            self.options42.append("PpB")
            self.options42.append("ApB")
            self.options53.append("PpB")
            self.options53.append("ApB")
            self.options63.append("PpB")
            self.options63.append("ApB")

            self.options73.append("10")
            self.options73.append("100")
            self.options73.append("1000")
            
            self.options81.append("/home/ibis/thomas.nussbaumer/Comparative_Genomics/Comparative_Genomics/Bd_toDo/Bd.db")
            self.options81.append("/home/ibis/thomas.nussbaumer/Comparative_Genomics/Comparative_Genomics/Os_toDo/Os.db")
            self.options81.append("/home/ibis/thomas.nussbaumer/Comparative_Genomics/Comparative_Genomics/Sb_toDo/Sb.db")
            self.options81.append("/home/ibis/thomas.nussbaumer/Comparative_Genomics/Comparative_Genomics/mihaela/Bd/Bd.db")
            self.options81.append("C:/heatmap_Thomas/Bd.db")
            self.options81.append("C:/heatmap_Thomas/Os.db")
            self.options81.append("C:/heatmap_Thomas/Sb.db")
            self.options81.append("C:/heatmap_Thomas/Zm_only_density_table.db")
            
            self.options82.append("density_Bd")
            self.options82.append("density_Os")
            self.options82.append("density_Sb")
            self.options82.append("density_Zm")
            
            self.options83.append("anno_Bd")
            self.options83.append("anno_Os")
            self.options83.append("anno_Sb")
            self.options83.append("anno_Zm")
            
            seq_ids = sqlite_methods.getSeqIdsAll(self.db_file, self.density_table)

            if(len(seq_ids) > 1):
                self.options2.append("all")

                self.options21.append("total")
                self.options21.append("all")
            seq_ids.append(["", "\n"])
            
            for seq_id in seq_ids:
                c_seq_id = seq_id[0]
                self.options2.append(c_seq_id)
                self.options4.append(c_seq_id)
                self.options52.append(c_seq_id)
                self.options62.append(c_seq_id)
                self.options33.append(c_seq_id)
            
            self.options33.append("all")
            seq_ids2 = sqlite_methods.getSeqIdsAll(self.db_file, self.anno_table)

            for seq_id2 in seq_ids2:
                self.options71.append(seq_id2[0])
            
            
            self.options71.append("all")
            
            if(update == True):
                self.e1.destroy()
                self.e12.destroy()
                self.e2.destroy()
                self.e21.destroy()
                self.e31.destroy()
                self.e32.destroy()
                self.e33.destroy()
                self.e34.destroy()
                self.e35.destroy()
                self.e37.destroy()
                self.e41.destroy()
                self.e42.destroy()
                self.e43.destroy()
                self.e44.destroy()
                self.e5.destroy()
                self.e51.destroy()
                self.e52.destroy()
                self.e53.destroy()
                self.e6.destroy()
                self.e61.destroy()
                self.e62.destroy()
                self.e63.destroy()
                self.e7.destroy()
                self.e8.destroy()
                self.e9.destroy()
                
                self.lab11.destroy()
                self.lab12.destroy()
                self.lab13.destroy()
                self.lab14.destroy()
                self.lab15.destroy()
                self.lab21.destroy()
                self.lab22.destroy()
                self.lab23.destroy()
                self.lab24.destroy()
                self.lab25.destroy()
                self.lab26.destroy()
                self.lab3.destroy()
                self.lab31.destroy()
                self.lab32.destroy()
                self.lab4.destroy()
                self.lab51.destroy()
                self.lab52.destroy()
                self.lab53.destroy()
                self.lab61.destroy()
                self.lab62.destroy()
                self.lab63.destroy()
                self.lab71.destroy()
                self.lab71_2.destroy()
                self.lab72.destroy()
                self.lab72_2.destroy()
                self.lab73.destroy()
                self.lab73_2.destroy()
                self.lab74.destroy()
                self.lab75.destroy()
                self.lab75.destroy()
                self.lab81.destroy()
                self.lab81_2.destroy()
                self.lab82.destroy()
                self.lab82_2.destroy()
                self.lab83.destroy()
                self.lab83_2.destroy()
                self.lab84.destroy()
                
                self.radio1.destroy()
                self.radio2.destroy()
                self.radio3.destroy()
                self.radio74.destroy()
                
                self.color1.destroy()
                self.color2.destroy()
                self.color3.destroy()
                self.color4.destroy()
                self.color5.destroy()
                
                self.bb11.destroy() 
                self.bb33.destroy()
                self.bb34.destroy()
                self.bb35.destroy()
                self.bb41.destroy()
                self.bb42.destroy()
                self.bb43.destroy()
                self.bb51.destroy()
                self.bb61.destroy()
                
                self.iframe31.destroy()
                self.iframe41.destroy()

            self.lab11 = Label(self.f, text="anno_id 1", anchor=W)
            self.lab11.grid(row=0, sticky="E")
                
            self.lab12 = Label(self.f, text="seq_id 1")
            self.lab12.grid(row=2, sticky="E")
    
            self.lab13 = Label(self.f, text="mode 1")
            self.lab13.grid(row=3, sticky="E")
                
            self.lab14 = Label(self.f, text="anno_id 2", anchor=W)
            self.lab14.grid(row=1, sticky="E")

            self.lab15 = Label(self.f, text="")
            self.lab15.grid(row=2, column=4, sticky="W")

            self.bb11 = Button(self.f, text="Scatterplot", command=self.scatterplot)
            self.bb11.grid(row=5, column=1, sticky="E")
    
            self.lab51 = Label(self.f5, text="anno_id 1", anchor=W)
            self.lab51.grid(row=0, sticky="E")
                
            self.lab52 = Label(self.f5, text="seq_id 1")
            self.lab52.grid(row=1, sticky="E")
    
            self.lab53 = Label(self.f5, text="mode 1")
            self.lab53.grid(row=2, sticky="E")
    
            self.lab61 = Label(self.f6, text="anno_id 1", anchor=W)
            self.lab61.grid(row=0, sticky="E")
                
            self.lab62 = Label(self.f6, text="seq_id 1")
            self.lab62.grid(row=1, sticky="E")
    
            self.lab63 = Label(self.f6, text="mode 1")
            self.lab63.grid(row=2, sticky="E")
    
            self.bb51 = Button(self.f5, text="Histogram", command=self.histogram1)
            self.bb51.grid(row=3, column=2, sticky="W")
            self.radio1_v1 = BooleanVar()
            self.radio1 = Checkbutton(self.f5, text='include previously calculated', variable=self.radio1_v1, command=self.change_state_v1)
            self.radio1.grid(row=3, column=3, sticky="W")
    
            self.bb61 = Button(self.f6, text="Distribution", command=self.distribution1)
            self.bb61.grid(row=3, column=2, sticky="W")
            self.radio2_v2 = BooleanVar()
            self.radio2 = Checkbutton(self.f6, text='include previously calculated', variable=self.radio2_v2, command=self.change_state_v2)
            self.radio2.grid(row=3, column=3, sticky="W")
                
     
            self.radio3_v3 = BooleanVar()
            self.radio3 = Checkbutton(self.f, text='include previously calculated', variable=self.radio3_v3, command=self.change_state_v3)
            self.radio3.grid(row=5, column=2, sticky="W")
    
            self.lab31 = Label(self.f3, text="anno_id", anchor=W)
            self.lab31.grid(row=0, sticky="E")
    
            self.e31 = apply(OptionMenu, (self.f3, self.variable11) + tuple(self.options11))
            self.e31.config(width=40)
            self.e31.grid(row=0, column=1)
    
            self.lab32 = Label(self.f3, text="mode", anchor=W)
            self.lab32.grid(row=1, sticky="E")
    
            self.e33 = Listbox(self.f3, selectmode=EXTENDED)
            self.e33.config(width=40)
            self.e33.grid(row=5, column=0, sticky="W")
            self.listbox_insert_seqIds(self.e33, set_ids)

            self.lab33 = Label(self.f3, text="seq_ids", anchor=W)
            self.lab33.grid(row=2, sticky="E")
    
            self.e31 = apply(OptionMenu, (self.f3, self.variable33) + tuple(self.options33))
            self.e31.config(width=40)
            self.e31.grid(row=2, column=1)
            
            self.lab34 = Label(self.f3, text="lower_seq_coord", anchor=W)
            self.lab34.grid(row=3, sticky="E")
    
            self.e35 = Entry(self.f3, textvariable=self.variable35)
            self.e35.config(width=40)
            self.e35.grid(row=3, column=1)
            
            self.lab36 = Label(self.f3, text="upper_seq_coord", anchor=W)
            self.lab36.grid(row=4, sticky="E")
    
            self.e37 = Entry(self.f3, textvariable=self.variable37)
            self.e37.config(width=40)
            self.e37.grid(row=4, column=1)
    
            self.iframe31 = Frame(self.f3, bd=4, relief=RIDGE)
            self.bb33 = Button(self.iframe31, text="<<", command=self.boxplot2_1)
            self.bb33.pack(side=BOTTOM)
            self.bb34 = Button(self.iframe31, text=">>", command=self.boxplot1_2)
            self.bb34.pack(side=BOTTOM)
            self.iframe31.grid(row=5, column=1)
    
            self.e34 = Listbox(self.f3, selectmode=EXTENDED)
            self.e34.config(width=40)
            self.e34.grid(row=5, column=2, sticky="W")
    
            self.e32 = apply(OptionMenu, (self.f3, self.variable32) + tuple(self.options32))
            self.e32.config(width=40)
            self.e32.grid(row=1, column=1)
    
            self.bb33 = Button(self.f3, text="Boxplots", command=self.boxplots)
            self.bb33.grid(row=6, column=0, sticky="W")

            self.bb35 = Button(self.f3, text="Scatterplot", command=self.boxplots2)
            self.bb35.grid(row=6, column=1, sticky="W")
    
            self.lab4 = Label(self.f4, text="mode 1")
            self.lab4.grid(row=0, column=0, sticky="W")
                
            self.bb41 = Button(self.f4, text="Correlations", command=self.correlations)
            self.bb41.config(width=10)
            self.bb41.grid(row=2, column=0, sticky="W")

            self.e41 = apply(OptionMenu, (self.f, self.variable41) + tuple(self.options41))
            self.e41.config(width=40)
            self.e41.grid(row=3, column=1)

            self.e42 = apply(OptionMenu, (self.f4, self.variable42) + tuple(self.options42))
            self.e42.config(width=40)
            self.e42.grid(row=0, column=1, sticky="W")
                
            self.e43 = Listbox(self.f4)
            self.e43.config(width=40)
            self.e43.grid(row=1, column=0, sticky="W")
            self.listbox_insert_seqIds(self.e43, set_ids)
    
            self.iframe41 = Frame(self.f4, bd=4, relief=RIDGE)
            self.bb42 = Button(self.iframe41, text="<<", command=self.correlation2_1)
            self.bb42.pack(side=BOTTOM)
            self.bb43 = Button(self.iframe41, text=">>", command=self.correlation1_2)
            self.bb43.pack(side=BOTTOM)
            self.iframe41.grid(row=1, column=1)
    
            self.e44 = Listbox(self.f4)
            self.e44.config(width=40)
            self.e44.grid(row=1, column=2, sticky="W")
                
            self.chromosomal_structure_colors = []
            self.chromosomal_structure_colors.append("#458B74")
            self.chromosomal_structure_colors.append("#66CDAA")
            self.chromosomal_structure_colors.append("#4e91c9")
            self.chromosomal_structure_colors.append("#DB7093")
            self.chromosomal_structure_colors.append("#EEE8AA")
                
            self.v = StringVar()
            self.v.set("1")
                
            self.colors = []
                
            self.e5 = apply(OptionMenu, (self.f2, self.variable5) + tuple(self.options5))
            self.e5.config(width=40)
            self.e5.grid(row=10, column=1)
            self.lab21 = Label(self.f2, text="anno_id #1")
            self.lab21.grid(row=10, column=0)
            self.color1 = Radiobutton(self.f2, text="Color", command=self.ChangeColor, background=self.chromosomal_structure_colors[0], variable=self.v, value="1")
            self.color1.grid(row=10, column=2)
            self.colors.append(self.color1)
                
            self.e6 = apply(OptionMenu, (self.f2, self.variable6) + tuple(self.options6))
            self.e6.config(width=40)
            self.e6.grid(row=11, column=1)
            self.lab22 = Label(self.f2, text="anno_id #2")
            self.lab22.grid(row=11, column=0)
            self.color2 = Radiobutton(self.f2, text="Color", command=self.ChangeColor, background=self.chromosomal_structure_colors[1], variable=self.v, value="2")
            self.color2.grid(row=11, column=2)
            self.colors.append(self.color2)
                
            self.e7 = apply(OptionMenu, (self.f2, self.variable7) + tuple(self.options7))
            self.e7.config(width=40)
            self.e7.grid(row=12, column=1)
            self.lab23 = Label(self.f2, text="anno_id #3")
            self.lab23.grid(row=12, column=0)
            self.color3 = Radiobutton(self.f2, text="Color", command=self.ChangeColor, background=self.chromosomal_structure_colors[2], variable=self.v, value="3")
            self.color3.grid(row=12, column=2)
            self.colors.append(self.color3)
                
            self.e8 = apply(OptionMenu, (self.f2, self.variable8) + tuple(self.options8))
            self.e8.config(width=40)
            self.e8.grid(row=13, column=1)
            self.lab24 = Label(self.f2, text="anno_id #4")
            self.lab24.grid(row=13, column=0)
            self.color4 = Radiobutton(self.f2, text="Color", command=self.ChangeColor, background=self.chromosomal_structure_colors[3], variable=self.v, value="4")
            self.color4.grid(row=13, column=2)
            self.colors.append(self.color4)
                
            self.e9 = apply(OptionMenu, (self.f2, self.variable9) + tuple(self.options9))
            self.e9.config(width=40)
            self.e9.grid(row=14, column=1)
            self.lab25 = Label(self.f2, text="anno_id #5")
            self.lab25.grid(row=14, column=0)
            self.color5 = Radiobutton(self.f2, text="Color", command=self.ChangeColor, background=self.chromosomal_structure_colors[4], variable=self.v, value="5")
            self.color5.grid(row=14, column=2)
            self.colors.append(self.color5)
  
            self.lab26 = Label(self.f2, text="seq_id 1")
            self.lab26.grid(row=15, column=0)
                 
            self.lab3 = Button(self.f2, text="Chromosomal Structure", command=self.structure)
            self.lab3.grid(row=16, column=1, sticky="W")
                
            self.e21 = apply(OptionMenu, (self.f2, self.variable21) + tuple(self.options21))
            self.e21.config(width=40)
            self.e21.grid(row=15, column=1, sticky="W")
                
            self.e1 = apply(OptionMenu, (self.f, self.variable1) + tuple(self.options1))
            self.e1.config(width=40)
        
            self.e2 = apply(OptionMenu, (self.f, self.variable2) + tuple(self.options2))
            self.e2.config(width=40)
    
    
            self.e51 = apply(OptionMenu, (self.f5, self.variable51) + tuple(self.options51))
            self.e51.config(width=40)
        
            self.e52 = apply(OptionMenu, (self.f5, self.variable52) + tuple(self.options52))
            self.e52.config(width=40)
    
            self.e53 = apply(OptionMenu, (self.f5, self.variable53) + tuple(self.options53))
            self.e53.config(width=40)
                
            self.e61 = apply(OptionMenu, (self.f6, self.variable61) + tuple(self.options61))
            self.e61.config(width=40)
        
            self.e62 = apply(OptionMenu, (self.f6, self.variable62) + tuple(self.options62))
            self.e62.config(width=40)
    
            self.e63 = apply(OptionMenu, (self.f6, self.variable63) + tuple(self.options63))
            self.e63.config(width=40)
                
            self.e1.grid(row=0, column=1)
            self.e2.grid(row=2, column=1)
                
            self.e12 = apply(OptionMenu, (self.f, self.variable3) + tuple(self.options3))
            self.e12.config(width=40)
        
            self.e12.grid(row=1, column=1)
            self.e51.grid(row=0, column=5)
            self.e52.grid(row=1, column=5)
            self.e53.grid(row=2, column=5)
            self.e61.grid(row=0, column=5)
            self.e62.grid(row=1, column=5)
            self.e63.grid(row=2, column=5)
                
            iframe21 = Frame(self.f, bd=4, relief=RIDGE)
            iframe21.grid(row=2, column=3)
    
            self.lab71 = Label(self.f7, text="seq id")
            self.lab71.grid(row=0, column=0, sticky="E")
    
            self.lab71_2 = apply(OptionMenu, (self.f7, self.variable71) + tuple(self.options71))
            self.lab71_2.grid(row=0, column=1, sticky="E")
    
            self.lab72 = Label(self.f7, text="anno_id")
            self.lab72.grid(row=1, column=0, sticky="E")
    
            self.lab72_2 = apply(OptionMenu, (self.f7, self.variable72) + tuple(self.options72))
            self.lab72_2.grid(row=1, column=1, sticky="E")
    
            self.lab73 = Label(self.f7, text="bins")
            self.lab73.grid(row=2, column=0, sticky="E")
    
            self.lab73_2 = apply(OptionMenu, (self.f7, self.variable73) + tuple(self.options73))
            self.lab73_2.grid(row=2, column=1, sticky="E")
    
            self.lab74 = Button(self.f7, text="Length", command=self.length)
            self.lab74.grid(row=3, column=0, sticky="E")
    
            self.lab75 = Button(self.f7, text="Length_2", command=self.length2)
            self.lab75.grid(row=3, column=1, sticky="E")
    
            self.radio4_v4 = BooleanVar()
            self.radio74 = Checkbutton(self.f7, text='include previously calculated', variable=self.radio4_v4, command=self.change_state_v4)
            self.radio74.grid(row=4, column=1, sticky="W")
    
            self.lab81 = Label(self.f8, text="db_file")
            self.lab81.grid(row=1, column=0, sticky="E")
    
            self.lab81_2 = apply(OptionMenu, (self.f8, self.variable81) + tuple(self.options81))
            self.lab81_2.grid(row=1, column=1, sticky="E")
    
            self.lab82 = Label(self.f8, text="density_table")
            self.lab82.grid(row=2, column=0, sticky="E")
    
            self.lab82_2 = apply(OptionMenu, (self.f8, self.variable82) + tuple(self.options82))
            self.lab82_2.grid(row=2, column=1, sticky="E")
    
    
            self.lab83 = Label(self.f8, text="anno_table")
            self.lab83.grid(row=3, column=0, sticky="E")
    
            self.lab83_2 = apply(OptionMenu, (self.f8, self.variable83) + tuple(self.options83))
            self.lab83_2.grid(row=3, column=1, sticky="E")
                
            self.lab84 = Button(self.f8, text="Update", command=self.update)
            self.lab84.grid(row=4, column=0, sticky="E")
    
            if(update == False):
                #n.add_screen(self.f, "Scatterplot")
                #n.add_screen(self.f2, "Chromosomal Structure")
                n.add_screen(self.f3, "Correlation in Chromosomes")
                n.add_screen(self.f4, "Correlation in Features")
                #n.add_screen(self.f5, "Histogram")
                #n.add_screen(self.f6, "Distribution")  
                #n.add_screen(self.f7, "Anno Table")   
                #n.add_screen(self.f8, "Settings") 
           
            if(run == True):                  
                self.master.mainloop()

def start():
    statTools = StatTools()
    
    db_file = "/nfs/plant/data/heatmaps/mihaela/barleyHeatmaps_jun10/Bd/Bd.db"
    density_table = "density_Bd"
    anno_table = "anno_Bd"
    
    statTools.body(db_file, density_table, anno_table)    
    
if __name__ == "__main__":
    #create_correlation_matrixes()
    start()
    #testCorrelationMatrices()
    #testBoxplots2CpGIslands()

