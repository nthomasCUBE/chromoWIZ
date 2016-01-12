import sqlite_methods
import calc_vis_elements
import methods
import sys
import math
from Tkconstants import DISABLED, NORMAL

def RedrawHeatmap(master, _ranges=None) :
        try:
            master.root.canvas.delete('all')  
        except Exception:
            pass

        if(master.image_export_possible == True):
            master.draw.rectangle((0, 0, master.image1Width, master.image1Height), fill="white")
        
        bin_start = None
        bin_stop = None
        
        master.heatMapSize = 75
        
        master.focusOnBarCharts = 0
        
        position = 1
        
        mode = master.display
            
        master.pswidth = 0
        master.pswidthExport = 0
        
        master.AdaptMaxLabelSize()
        
        try:
            master.getMax2()
        except Exception:
            pass
        
        absolute_max = master.maxV
        absolute_min = master.minV
        
        try:
            master.scale["to"] = math.ceil(absolute_max)
            master.scale["from"] = math.ceil(absolute_min)
        except Exception:
            pass

        l = 0
        for seq_id in master.seq_ids:
            elements = []
            
            if(_ranges != None and l < len(_ranges)):
                bin_start = int(int(_ranges[l]) * 1000000)
                master.bin_start = (bin_start / 1000000)
                bin_stop = int(int(_ranges[l + 1]) * 1000000)
                l = l + 2
            
            if(master.elementList.get(seq_id) == None or _ranges != None):
                elements = master.getElementsFromDatabase(seq_id, master.set_id_A, master.density_table, master.db_file, bin_start, bin_stop)[0]               
                master.elementList[seq_id] = elements
            else:
                elements = master.elementList.get(seq_id)

            try:
                scaleValue = master.scale.get()
                if(scaleValue == 0):
                    scaleValue = master.maxV
            except Exception:
                scaleValue = master.maxV
            
            #SCALING PARAMETER
            scaleValue = 100                                       #damit heatmap colors zw. 0 und 100 prozent skaliert

            if(scaleValue - absolute_min == 0):
	        intensityF = absolute_max / absolute_min
            elif(scaleValue - absolute_min < 0):
                intensityF = 0
            else:
                intensityF = (absolute_max - absolute_min) / (scaleValue - absolute_min)
            
            calc_vis_elements.calc_vis_elements(master, elements, seq_id, position, intensityF, False, False, False, "", absolute_min, absolute_max, None)
            position = position + 1   

        if len(master.seq_ids) > 0:  
            calc_vis_elements.createColorMap(master, mode)
        

def RedrawBarChart(master, loadSequences, _position=None, _seq=None, _set_ids=None, _elements=None, _heatMapSize=None, _ranges=None):
        cur_window_size = -1
        bin_start = None
        bin_stop = None
        if(len(master.SetIdList) > 0):
            cur_shift_size = master.SetIdList[0].split("_")[2]
        
        #master.button5["state"] = DISABLED
        if( _position == None):
            try:
		master.root.canvas.delete('all') 
            except Exception:
		pass
            if(master.image_export_possible == True):
                master.draw.rectangle((0, 0, master.image1Width, master.image1Height), fill="white")

        master.lineChart = False
        
        master.focusOnBarCharts = 1
                
        if(_heatMapSize == None):
            master.heatMapSize = 100
        else:
            master.heatMapSize = _heatMapSize

        master.pswidth = 0
        master.pswidthExport = 0
        master.psheight = 0
        
        barChart = {}
        
        real_max = -1
        
        if(_seq != None):
            master.seq_ids = []
            master.seq_ids.append(_seq)
        
        if(_set_ids != None):
            master.SetIdList = _set_ids

        max_value = -1
        max_value_total = -1

        l = 0
        if(len(master.SetIdList) > 0):
            for seq in master.seq_ids:
                if(_ranges != None and l < len(_ranges)):
                    bin_start = int(int(_ranges[l]) * 1000000)
                    master.bin_start = (bin_start / 1000000)
                    bin_stop = int(int(_ranges[l + 1]) * 1000000)
                    l = l + 2
                counter = 0
                elements_total = None
                for value in master.SetIdList:
                    if(master.cmd_line == False):
                        master.display = "% bp"
                    elements = None
                    #master.NContent.set(100)
                    if(_elements == None):
                        elements = master.getElementsFromDatabase(seq, value, master.density_table, master.db_file, bin_start, bin_stop)[0]
                        if(master.display != "% bp"):
                            if(elements_total == None):
                                elements_total = [0] * (len(elements))
                            for i in range(0, len(elements)):
                                elements_total[i] = elements_total[i] + elements[i]
                                elements[i] = (elements[i])
                    else:
                        elements = _elements[value]
                    if(barChart.get(seq) == None):
                        barChart[seq] = {}
                    barChart[seq][counter] = []
                    barChart[seq][counter] = elements
                    
                    if(master.colorToSetIdMap.get(value) != None):
                        master.colorMap[counter] = master.colorToSetIdMap.get(value)
                    else:
                        master.colorMap[counter] = master.colors[counter % len(master.colors)]
                        master.colorToSetIdMap[value] = master.colors[counter % len(master.colors)]
                    counter = counter + 1
                if(master.cmd_line == True and master.display != "% bp"):
                    max_value = max(elements_total)
                    if(max_value_total < max_value):
                        max_value_total = max_value
            real_max = max_value_total
            if(master.cmd_line == True and master.display != "% bp"):
                for seq in master.seq_ids:
                    amountElements = len((barChart.get(seq)).get(0))
                    for i in range(0, amountElements):
                            sum = 0
                            for k in range(0, len(barChart.get(seq).keys())):
                                barChart[seq].get(k)[i] = int((barChart[seq].get(k)[i] / float(real_max)) * 100.0)
            position = 0
            if(_position != None):
                position = _position
            x = 0
            for seq in master.seq_ids:
                if(_ranges != None and x < len(_ranges)):
                    bin_start = int(int(_ranges[x]) * 1000000)
                    master.bin_start = (bin_start / 1000000)
                    x = x + 2
                amountElements = len((barChart.get(seq)).get(0))
                for i in range(0, amountElements):
                    sum = 0
                    for k in range(1, len(barChart.get(seq).keys())):
                        barChart[seq].get(k)[i] += barChart[seq].get(k - 1)[i]
                barChart[seq][counter] = []
                master.colorMap[counter] = master.colorBackGround
                for l in range(0, amountElements):
                    barChart.get(seq).get(counter).append(100)
                    
                keys = []
                keys = barChart[seq].keys()
                keys.reverse()
                
                master.AdaptMaxLabelSize()

                for ckey in keys:
                    if(len(seq) * master.fontSize > master.maxLabelSize):
                        master.maxLabelSize = len(seq) * master.fontSize
                    elements = barChart.get(seq).get(ckey)
                    for i in range(0, len(elements)):
                        elements[i] = elements[i] * master.heatMapSize / 100.0
                    calc_vis_elements.calc_vis_elements(master, elements , seq, position, 1, True, False, master.colorMap.get(ckey), "", None, None, real_max)
                position = position + 1
        
        if(_position != None):
            return
             
        calc_vis_elements.createBarChartLegend(master, "BarChart")
        master.ChangeSize()

        if(master.scale != None):
            master.scale.destroy()
            master.scale = None
        if(master.button != None):
            master.button.destroy()
            master.button = None
        
def RedrawStackedHeatmap(master, heatMapSize=None, _ranges=None):
        try:
            master.button5["state"] = NORMAL
            master.root.canvas.delete('all') 
            if(master.image_export_possible == True):
                master.draw.rectangle((0, 0, master.image1Width, master.image1Height), fill="white")
        except Exception:
            pass
        
        master.lineChart = False
        master.pswidth = 0
        master.psheight = 0
        master.gapBetweenHeatmaps = 0

        if(heatMapSize == None):
            master.heatMapSize = 50
        else:
            master.heatMapSize = heatMapSize
            
        position = 0

        master.focusOnBarCharts = 2
        
        seq_ids = master.seq_ids
        anno_ids = master.anno_ids
        master.AdaptMaxLabelSize()

        l = 0
        bin_start = None
        bin_stop = None
        for seq_id in seq_ids:
            if(_ranges != None and l < len(_ranges)):
                bin_start = int(int(_ranges[l]) * 1000000)
                bin_stop = int(int(_ranges[l + 1]) * 1000000)
                l = l + 2

            for anno_id in anno_ids:
                
                master.set_id_A = anno_id
                                
                try:
                    minIntensity = None
                    maxIntensity = None
                    
                    try:
                        master.calculateMinAndMax()
                        print "anno_id::",anno_id,seq_id
                        minIntensity = master.anno_ids_mItensities[anno_id]["min"]
                        maxIntensity = master.anno_ids_mItensities[anno_id]["max"]
                        print "max:",maxIntensity,"min:",minIntensity
                        print "\n\n";
                        
                    except Exception:
                        print "ERROR", "RedrawStackedHeatmap", sys.exc_info()
                        
                    cIntensity = None

                    filterOn=False
                    try:
                        cIntensity = master.anno_ids_mItensities[seq_id]["cur"]
                        print "INFO", "using seq_id constraint", cIntensity, "for seq_id", seq_id
                        filterOn=True
                    except Exception:
                        pass

                    try:
                        cIntensity = master.anno_ids_mItensities[anno_id]["cur"]
                        print "INFO", "using set_id constraint", cIntensity, "for set_id", anno_id
                        filterOn=True
                    except Exception:
                        pass

                    try:
                        cIntensity = master.anno_ids_mItensities[seq_id+"_"+anno_id]["cur"]
                        filterOn=True
                        print "INFO", "using seq_id+set_id constraint", cIntensity, "for set_id", anno_id
                    except Exception:
                        pass


                    #
                    elements = master.getElementsFromDatabase(seq_id, anno_id, master.density_table, master.db_file, bin_start, bin_stop)[0]
                    #
                    if(cIntensity == None):
                        print "INFO", "cIntensity>maxIntensity",maxIntensity
                        cIntensity = maxIntensity
                    elif(int(cIntensity) == -1):
                            print "INFO", "using track max",max(elements)
                            cIntensity = max(elements)
                    #
                    if(filterOn==True):
                        intensity = max(elements)/cIntensity
                    else:
                        intensity = max(elements)/maxIntensity
                    #   
                    if(intensity < 0):
                        intensity = abs(intensity)    
                    try:
                        calc_vis_elements.calc_vis_elements(master, elements, seq_id, position, intensity , False, True, False, anno_id, None, None)
                    except Exception:
                        print "ERROR", "RedrawStackedHeatmap", "Creating visualisation element failed for", seq_id, sys.exc_info()
                    position = position + 1
                except Exception:
                    print "ERROR", "RedrawStackedHeatmap", sys.exc_info()
                    pass
            position = position + 1

        if(master.scale != None):
            master.scale.destroy()
            master.scale = None
        if(master.button != None):
            master.button.destroy()
            master.button = None

def RedrawLineChart(master):
    master.lineChart = True
    RedrawHeatmap(master)
