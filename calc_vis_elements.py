# -*- coding: iso-8859-1 -*-
import math
import sys
from decimal import *

def add_X_scale(self, elements, stepSizeInPixel, position, chrom_length, moveInPixel, shift, real_max, line_length_x_coor_label, extra_gap):
        try:
            for k in range(0, len(elements), int(stepSizeInPixel)):
                label = (int(k) * int(shift))
                if(chrom_length >= 1000000):
                    label = math.ceil(label / 1000000.0)
                    label = int(label)
                elif(len(str(label)) >= 2 and chrom_length >= 100000):
                    label = str((Decimal(str(label)) / Decimal(1000000)))[0:3]
                elif(len(str(label)) > 2):
                    label = str((Decimal(str(label)) / Decimal(1000000)))[0:4]
                y1 = self.gapBetweenHeatmaps * (position + 1) + self.heatMapSize + 10 - self.add_gap
                y2 = self.gapBetweenHeatmaps * (position + 1) + self.heatMapSize + 5 - self.add_gap
                x1 = self.startLabel + k
                x2 = self.startLabel + k
                
                try:
                    if(self.gapBetweenHeatmaps > 100):
	                    tt1 = self.root.canvas.create_text(x1 + moveInPixel, y1, text=str(label), anchor="w", font=('Courier New', self.guiFontSizeAxis))
                except Exception:
                    pass
                
                if(self.gapBetweenHeatmaps > 100 and self.image_export_possible == True):
                    import ImageFont
                    f = ImageFont.truetype(self.cwd + "font/cour.ttf", self.fontSizeFactor * self.fontSizeAxis)
                    self.draw.text((self.fontSizeFactor * (x1 + moveInPixel), self.fontSizeFactor * y1), str(label), fill="black", font=f)
                if(self.gapBetweenHeatmaps > 100):
                    try:
                        self.heatmapsToMove[position].append(tt1)
                    except Exception:
                        pass
                    if(self.image_export_possible == True):
                        import ImageFont
                        f = ImageFont.truetype(self.cwd + "font/cour.ttf", self.fontSizeFactor * self.fontSizeAxis)
                        
                        if(real_max != None):
                            stepSize = self.searchStepSize(real_max, 0, 5)
                            i = 0
                            while(i < real_max):
                                cur_pos = (float(i) / float(real_max)) * self.heatMapSize
                                i = i + stepSize
                                extra_gap = 50
                    if(self.lineChart == True):
                        line_length_x_coor_label = 10
                    
                    try:
                        try:
                            tt2 = self.root.canvas.create_line(x1 + moveInPixel, y1 - line_length_x_coor_label, x2 + moveInPixel , y2)
                            self.heatmapsToMove[position].append(tt2)
                        except Exception:
                            pass
                    except Exception:
                        pass
                    
                if(self.gapBetweenHeatmaps > 100 and self.image_export_possible == True):
                    self.draw.line((self.fontSizeFactor * (x1 + moveInPixel), self.fontSizeFactor * (y1 - line_length_x_coor_label), self.fontSizeFactor * (x2 + moveInPixel) , self.fontSizeFactor * y2), fill="black")
    
            if(self.lineChart == True):
                try:
                    self.root.canvas.create_line((self.startLabel, (y1 - 10), self.startLabel + len(elements), (y1 - 10)), fill="black")
                except Exception:
                    pass
                if(self.image_export_possible == True):
                    if(self.image_export_possible == True):
                        self.draw.rectangle((self.fontSizeFactor * (self.startLabel), self.fontSizeFactor * (y1 - 10), self.fontSizeFactor * (self.startLabel + len(elements)), self.fontSizeFactor * (y1 - 10)), fill="black")
        except Exception:
            print "ERROR", "add_X_scale", sys.exc_info()
            #sys.exit()

def calc_vis_elements(self , elements, seq_id, position, intensityFactor, isBarChart, isStackedHeatmap, Color, LabelSeqId, absolute_min, absolute_max, real_max=None):
        gapBetweenHeatmaps = None
        if(self.focusOnBarCharts == 2):
           try:
              gapBetweenHeatmaps = self.GapBetweenSequences.get() + self.heatMapSize
           except Exception:
              gapBetweenHeatmaps = self.gapBetweenHeatmaps + self.heatMapSize
              pass
        else:
           gapBetweenHeatmaps = self.gapBetweenHeatmaps
        self.maxLabelSizeFactor = 0.7
        LabelSeqId0 = LabelSeqId
        
        import sqlite_methods
        nmb_max = sqlite_methods.get_max_nmb_elements_per_seq_id(self.db_file, self.density_table, self.set_id_A, self.seq_ids)
	
        x_before = None
        y_before = None
        x_before_2_1 = None
        y_before_2_1 = None
        x_before_2_2 = None
        y_before_2_2 = None
        line_length_x_coor_label = 20
        extra_gap = 0
        hot_spots = [0] * len(elements)
        
        if(intensityFactor == None or intensityFactor == 0):
            intensityFactor = 1
        
        if(self.SequenceNameMap.get(seq_id) != None):
            _label = self.SequenceNameMap.get(seq_id)
        else:
            _label = seq_id
  
        try:
            LabelSeqId = str(LabelSeqId).split("__")[1]
        except Exception:
            pass
        
        if(len(LabelSeqId) > 0):
            if(self.SetIdMap.get(LabelSeqId0) == None):
                _label = _label + " " + LabelSeqId
            else:
                _label = _label + " " + self.SetIdMap.get(LabelSeqId0)

        if(isBarChart == False):
            self.heatmapsToMove[position] = []
        if(isBarChart == True):
            if(self.heatmapsToMove.get(position) == None):
                self.heatmapsToMove[position] = []
        self.add_gap = 0
        
        if(gapBetweenHeatmaps > 40):
            self.add_gap = gapBetweenHeatmaps / 5
            
        setIdAShortened = self.set_id_A.split("_win_")[1]
        shift = str(setIdAShortened).split("_shift")[0]
        
        moveInPixel = 0
        if(self.moveNPixelMap.get(position) != None):
            moveInPixel = self.moveNPixelMap.get(position)
        
        self.psheight = gapBetweenHeatmaps * (position)
        
        curWidth = int(self.startLabel) + len(elements) + 25 + self.maxLabelSizeFactor * self.maxLabelSize + moveInPixel
        curWithExport = int(self.startLabel) + len(elements) + 25 + self.maxLabelSizeFactor * self.maxLabelSizeExport + moveInPixel
        set_id_label = None
        
        set_id_label_max = None
        
        if(absolute_max != None):
            set_id_label_max = absolute_max
        else:
            set_id_label_max = self.maxV

        
        if(isStackedHeatmap == False):
            set_id_label = self.SetIdMap.get(self.set_id_A)
            if(set_id_label == None):
                try:
                    if(isBarChart == False):
                        set_id_label = self.set_id_A 
                except Exception:
                    pass
        if(set_id_label == None):
            set_id_label = ""
        else:
            try:
                set_id_label = set_id_label.split("__")[1]
            except Exception:
                pass
            
        if(self.label_to_display != None):
            set_id_label = self.label_to_display
            
        if position == 1 and self.focusOnBarCharts != 5:
            setIdX = self.startLabel
            setIdY = 100 + self.add_gap
            try:
                self.root.canvas.create_text(setIdX, setIdY, text=str(set_id_label), anchor="w", font=('Courier New', self.guiFontSizeLabel, 'bold'))
            except Exception:
                pass
            if(self.image_export_possible == True):
                import ImageFont
                f = ImageFont.truetype(self.cwd + "font/cour.ttf", self.fontSizeFactor * self.fontSizeLabel)
                self.draw.text((self.fontSizeFactor * setIdX, self.fontSizeFactor * setIdY), str(set_id_label), fill="black", font=f)
        if(self.pswidth < curWidth):
            self.pswidth = curWidth
            self.pswidthExport = curWidth

        chrom_length = (nmb_max * float(shift))
        stepSize = self.searchStepSize(int(chrom_length), 0, 5)
        stepSizeInPixel = float(stepSize) / float(shift)

        Nvalues = self.NList[seq_id]
        Wvalues = self.WindowLengthList[seq_id]

        relevantElementList = []
        try:
            for l in range(len(elements)):
                    if((float(Wvalues[l]) / float(Wvalues[0])) * 100.0 >= float(self.currFullLength)):
                        if(float(self.NList[seq_id][l]) < float(self.currNContent)):
                            relevantElementList.append(elements[l])
        except Exception:
            pass

        if(self.focusOnBarCharts == 2):
            self.minV = min(relevantElementList)
            self.maxV = max(relevantElementList)

        if(self.lineChart==True):
          _y1 = self.fontSizeFactor*(gapBetweenHeatmaps * (position + 1) + self.heatMapSize- self.add_gap)
	  import ImageFont
          f = ImageFont.truetype(self.cwd + "font/cour.ttf", self.fontSizeFactor * self.fontSizeLabel)
	  self.draw.line([(80,_y1), (90,_y1), (90,_y1-175), (80,_y1-175)], fill="#000000")
          f = ImageFont.truetype(self.cwd + "font/cour.ttf", self.fontSizeFactor * 14)
          min_L=len(str(f.getsize(str(self.minV))[0]))
          max_L=len(str(f.getsize(str(self.maxV))[0]))
          offset=min_L
	  if(max_L>offset):
	    offset=max_L
          self.draw.text((30-offset, _y1-190), str(int(round(self.maxV))), font=f, fill="#000000")
	  self.draw.text((30-offset, _y1-15), str(int(round(self.minV))), font=f, fill="#000000")
    
        for l in range(len(elements)):
            _Color = Color
	    try:
                if((float(Wvalues[l]) / float(Wvalues[0])) * 100.0 >= float(self.currFullLength)):
                    if(float(Nvalues[l]) < float(self.currNContent)):
                        intensity = self.getItensity(elements[l], intensityFactor)
                    else:
                        intensity = self.getItensity(-0.5, intensityFactor)
                        _Color = "grey"
                else:
                    intensity = self.getItensity(-0.5, intensityFactor) 
                    _Color = "grey"
            except Exception:
                import sys
                #sys.exit()
                intensity = 100
                _Color = "white"
                sys.exit()
                
            
            x1 = self.startLabel + self.maxLabelSizeFactor * self.maxLabelSize + self.gapBetweenLabelAndHeatmap + l
            x1 = self.startLabel + l

            if(isBarChart == True):
                y1 = gapBetweenHeatmaps * (position + 1) + self.heatMapSize - self.add_gap
            else:
                y1 = gapBetweenHeatmaps * (position + 1) - self.add_gap
                
            x2 = self.startLabel + self.maxLabelSizeFactor * self.maxLabelSize + self.gapBetweenLabelAndHeatmap + l
            x2 = self.startLabel + l
            
            if(isBarChart == True):
                barChartIntensity = elements[l]
                if(barChartIntensity > 100):
                    barChartIntensity = 100
                y2 = gapBetweenHeatmaps * (position + 1) + self.heatMapSize - barChartIntensity - self.add_gap
            else:
                y2 = gapBetweenHeatmaps * (position + 1) + self.heatMapSize - self.add_gap

                    
            try:
                if(isBarChart == True):
                    try:
                        self.heatmapsToMove[position].append(self.root.canvas.create_line(x1 + moveInPixel, y1 , x2 + moveInPixel , y2 , width=1, fill=_Color))
                    except Exception:
                        pass
                elif(self.lineChart == False):
                    try:
                        self.heatmapsToMove[position].append(self.root.canvas.create_line(x1 + moveInPixel, y1 , x2 + moveInPixel , y2 , width=1, fill=getJetColorMapColor(intensity / 255.0)[0]))
                    except Exception:
                        pass
                else:
                    rel_line_len = 10
                    rel_syn_value = 20

		    try:
                        rel_line_len = self.rel_line_len.get()
                        rel_syn_value = self.rel_syn_value.get()
                    except Exception:
                        rel_line_len = self.rel_line_len_var
                        rel_syn_value = self.rel_syn_value_var
                        pass
                    try:
                        if(l % rel_line_len == 0):
                            if(intensity < 0):
                                intensity = 0
                            if(x_before == None):
                                x_before = x1 + moveInPixel
                                y_before = y2 - intensity / 3.0
                            try:
                                self.root.canvas.create_line(x_before, y_before, x1 + moveInPixel , y2 - intensity / 3.0 , width=3, fill=getJetColorMapColor(intensity / 255.0)[0])                
                            except Exception:
                                pass
                            if(elements[l] >= rel_syn_value):
                                hot_spots[l] = (elements[l])
                                try:
                                    self.root.canvas.create_line(x_before, y1 - 15, x1 + moveInPixel, y1 - 15, fill="black")
                                except Exception:
                                    pass
                            x_before = x1 + moveInPixel
                            y_before = y2 - intensity / 3.0
                    except Exception:
                        pass
            except Exception:
                pass
            for i in range(0, self.fontSizeFactor):
                if(isBarChart == True):
                    if(self.image_export_possible == True):
                        try:
                            self.draw.line((self.fontSizeFactor * (x1 + moveInPixel) + i, self.fontSizeFactor * y1, self.fontSizeFactor * (x1 + moveInPixel) + i, self.fontSizeFactor * y2), fill=_Color)
                        except Exception:
                            print "draw_line", sys.exc_info()
                elif(self.lineChart == False):
                    if(self.image_export_possible == True):
                        try:
                            self.draw.line((self.fontSizeFactor * (x1 + moveInPixel) + i, self.fontSizeFactor * y1, self.fontSizeFactor * (x1 + moveInPixel) + i, self.fontSizeFactor * y2), fill=getJetColorMapColor(intensity / 255.0)[1])
                        except Exception:
                            print "draw_line", sys.exc_info()
                else:
                    try:
                        rel_line_len = None
                        rel_syn_value = None
                        
                        try:
                            rel_line_len = self.rel_line_len.get()
                            rel_syn_value = self.rel_syn_value.get()
                        except Exception:
                            rel_syn_value = self.rel_syn_value_var;
                            rel_line_len = self.rel_line_len_var;
                        
                        if(l % rel_line_len == 0):
                            if(x_before_2_1 == None):
                                x_before_2_1 = self.fontSizeFactor * (x1 + moveInPixel) + i
                                y_before_2_1 = self.fontSizeFactor * (y2 - intensity / 3.0 + 2) + i
                                x_before_2_2 = self.fontSizeFactor * (x1 + moveInPixel) + i
                                y_before_2_2 = self.fontSizeFactor * (y2 - intensity / 3.0 - 2) + i
    
                            x_before_cur_1 = self.fontSizeFactor * (x1 + moveInPixel) + i
                            y_before_cur_2 = self.fontSizeFactor * (y2 - intensity / 3.0 + 2) + i
                            x_before_cur_3 = self.fontSizeFactor * (x1 + moveInPixel) + i
                            y_before_cur_4 = self.fontSizeFactor * (y2 - intensity / 3.0 - 2) + i
                            
                            
                            if(self.image_export_possible == True):
				if(float(intensity)==0):
				  self.draw.polygon([(x_before_2_1, y_before_2_1), (x_before_cur_1, y_before_cur_2),
						(x_before_cur_3, y_before_cur_4), (x_before_2_2, y_before_2_2)],
						  fill="white") 
				else:
				  self.draw.polygon([(x_before_2_1, y_before_2_1), (x_before_cur_1, y_before_cur_2),
						(x_before_cur_3, y_before_cur_4), (x_before_2_2, y_before_2_2)],
						  fill=getJetColorMapColor(intensity / 255.0)[1]) 
    
                            if(elements[l] >= rel_syn_value):
                                if(self.image_export_possible == True):
                                    self.draw.rectangle((x_before_2_1, self.fontSizeFactor * y1, x_before_cur_1, self.fontSizeFactor * y1), fill="black")
                                
                            x_before_2_1 = self.fontSizeFactor * (x1 + moveInPixel) + i
                            y_before_2_1 = self.fontSizeFactor * (y2 - intensity / 3.0 + 2) + i
                            x_before_2_2 = self.fontSizeFactor * (x1 + moveInPixel) + i
                            y_before_2_2 = self.fontSizeFactor * (y2 - intensity / 3.0 - 2) + i
                    except Exception:
                        import sys
                        print "calc_vis_elements", sys.exc_info()
                        sys.exit()
                        pass
        start = -1
        stop = -1  

        blocks = []

        try:
            add_X_scale(self, elements, stepSizeInPixel, position, chrom_length, moveInPixel, shift, real_max, line_length_x_coor_label, extra_gap)
        except Exception:
            import sys
            pass

        for i in range(0, len(elements)):
            if(hot_spots[i] > 0):
                if(start == -1):
                    start = i
                    stop = i
                else:
                    stop = i
            else:
                if(start >= 0 and stop >= 0):
                    block = {}
                    block["start"] = start
                    block["stop"] = stop
                    blocks.append(block)

                start = -1
                stop = -1

        if(start > 0 and stop >= 0):
            block = {}
            block["start"] = start
            block["stop"] = stop
            blocks.append(block)
            
        start_before_cur = -1
        start_before_real = -1
        stop_before_real = -1
       
        try:
            self.merged_blocks[seq_id] = []
        except Exception:
            pass
        mean_value = -1
        
        rel_allowed_gap = None
        
        try:
            rel_allowed_gap = self.rel_allowed_gap.get()
        except Exception:
            rel_allowed_gap = self.rel_allowed_gap_var;
            
        
        for block in blocks:
            if(start_before_cur == -1):
                start_before_cur = block["start"]
                stop_before_cur = block["stop"]
                start_before_real = start_before_cur
            if(abs(block["start"] - start_before_cur) <= rel_allowed_gap):      
                start_before_cur = block["start"]
                stop_before_real = block["stop"]
            elif(abs(block["start"] - stop_before_cur) <= rel_allowed_gap):
                stop_before_real = block["stop"]
            else:
                intensity_sum_rel = 0
                elements_nmb_rel = 0
                max_len_element = 0
                all_blocks_elements = 0
                sum_len_blocks = 0

                for block2 in blocks:
                    if(block2["start"] >= start_before_real and block2["start"] <= stop_before_real):
                        intensity_sum_rel = intensity_sum_rel + sum(elements[int(block2["start"]):int(block2["stop"] + 1)])
                        elements_nmb_rel = elements_nmb_rel + len(elements[int(block2["start"]):int(block2["stop"] + 1)])
                        if(((int(block2["stop"]) + 1) - int(block2["start"])) > max_len_element):
                            max_len_element = ((int(block2["stop"]) + 1) - int(block2["start"]))
                        all_blocks_elements = all_blocks_elements + ((int(block2["stop"]) + 1) - int(block2["start"]))
                            
                mean_value_rel = intensity_sum_rel / elements_nmb_rel
                mean_value = sum(elements[start_before_real:stop_before_real + 1]) / (len(elements[start_before_real:stop_before_real + 1]))
                try:
                    self.root.canvas.create_line(self.startLabel + start_before_real, y1 - 20, self.startLabel + stop_before_real, y1 - 20, fill=getJetColorMapColor((mean_value - self.minV) / self.maxV)[0])
                except Exception:
                    pass
                rel_length = max_len_element / float((len(elements[start_before_real:stop_before_real + 1])))
                merged_block = {}
                merged_block["left"] = start_before_real
                merged_block["right"] = stop_before_real
                merged_block["avg"] = mean_value
                merged_block["avg_rel"] = mean_value_rel
                merged_block["max_element_len"] = (max_len_element / float(len(elements[start_before_real:stop_before_real + 1])))
                merged_block["all_element_len"] = (all_blocks_elements / float(len(elements[start_before_real:stop_before_real + 1])))
                #    
                try:
                    self.merged_blocks[seq_id].append(merged_block)
                except Exception:
                    pass
                #
                x_from = self.fontSizeFactor * (self.startLabel + start_before_real)
                x_to = self.fontSizeFactor * (self.startLabel + stop_before_real)
                if(self.image_export_possible == True):
                    self.draw.rectangle((x_from, self.fontSizeFactor * (y1 - 20), x_to, self.fontSizeFactor * (y1 - 20)), fill=getJetColorMapColor((mean_value - self.minV) / self.maxV)[1])
                start_before_real = block["start"]
                stop_before_real = block["stop"]
                
            start_before_cur = block["start"]
            stop_before_cur = block["stop"]

        if(seq_id != -1 and start_before_real != -1):
            merged_block = {}

            intensity_sum_rel = 0
            elements_nmb_rel = 0
            max_len_element = 0
            all_blocks_elements = 0

            for block2 in blocks:
                if(block2["start"] >= start_before_real and block2["start"] <= stop_before_real):
                    intensity_sum_rel = intensity_sum_rel + sum(elements[int(block2["start"]):int(block2["stop"] + 1)])
                    elements_nmb_rel = elements_nmb_rel + len(elements[int(block2["start"]):int(block2["stop"] + 1)])
                    if(((int(block2["stop"]) + 1) - int(block2["start"])) > max_len_element):
                        max_len_element = ((int(block2["stop"]) + 1) - int(block2["start"]))
                    all_blocks_elements = all_blocks_elements + ((int(block2["stop"]) + 1) - int(block2["start"]))
                        
            mean_value_rel = intensity_sum_rel / elements_nmb_rel
            mean_value = sum(elements[start_before_real:stop_before_real + 1]) / (len(elements[start_before_real:stop_before_real + 1]))
            merged_block["left"] = start_before_real
            merged_block["right"] = stop_before_real
            merged_block["avg"] = mean_value
            merged_block["avg_rel"] = mean_value_rel
            merged_block["max_element_len"] = (max_len_element / float(len(elements[start_before_real:stop_before_real + 1])))
            merged_block["all_element_len"] = (all_blocks_elements / float(len(elements[start_before_real:stop_before_real + 1])))
            #
            try:
                self.merged_blocks[seq_id].append(merged_block)
            except Exception:
                pass
            #
        if(start_before_real != -1):
            mean_value = sum(elements[start_before_real:stop_before_real + 1]) / (len(elements[start_before_real:stop_before_real + 1]))
            try:
                self.root.canvas.create_line(self.startLabel + start_before_real, y1 - 20, self.startLabel + stop_before_real, y1 - 20, fill=getJetColorMapColor((mean_value - self.minV) / self.maxV)[0])
            except Exception:
                pass
            x_from = self.fontSizeFactor * (self.startLabel + start_before_real)
            x_to = self.fontSizeFactor * (self.startLabel + stop_before_real)
            if(self.image_export_possible == True):
                self.draw.rectangle((x_from, self.fontSizeFactor * (y1 - 20), x_to, self.fontSizeFactor * (y1 - 20)), fill=getJetColorMapColor((mean_value - self.minV) / self.maxV)[1])

        if(absolute_min != None):
            try:
                if(self.scale.get() < absolute_min):
                    self.scale.set(absolute_min)
            except Exception:
                pass
            
        y1 = gapBetweenHeatmaps * (position + 1) + self.heatMapSize - self.add_gap
        
        self.positionHeatmaps[position] = y1 + 40

        if(self.focusOnBarCharts == 2):
            if(len(_label) <= 25):
                _label = _label  + " " + "(" + str(round(min(relevantElementList))) + ";" + str(round(max(relevantElementList))) + ")"
            else:
                _label = _label[0:25] + "... " + "(" + str(round(min(relevantElementList))) + ";" + str(round(max(relevantElementList))) + ")"
        add_gap = 10
        try:
            self.root.canvas.create_text((self.startLabel + len(elements) + 30) , y1 - self.heatMapSize + add_gap, anchor="w", text=_label, font=('Courier New', self.guiFontSizeSetid))
        except Exception:
            pass
        add_gap = 0
        if(self.image_export_possible == True):
            import ImageFont
            f = ImageFont.truetype(self.cwd + "font/cour.ttf", self.fontSizeFactor * self.fontSizeSetId)
            self.draw.text((self.fontSizeFactor * (self.startLabel + len(elements) + 30 + extra_gap) , self.fontSizeFactor * (y1 - self.heatMapSize + add_gap)), _label, fill="black", font=f)
            f = ImageFont.truetype(self.cwd + "font/cour.ttf", 40)
            if(isBarChart==False and isStackedHeatmap==False):
	      _label="("+str(min(relevantElementList))[0:str(min(relevantElementList)).find(".")+2]+","+str(max(relevantElementList))[0:str(max(relevantElementList)).find(".")+2]+","+str(sum(relevantElementList)/len(relevantElementList))[0:str(sum(relevantElementList)/len(relevantElementList)).find(".")+2]+")"
	      self.draw.text((self.fontSizeFactor * (self.startLabel + len(elements) + 30 + extra_gap) , self.fontSizeFactor * (y1 - self.heatMapSize + add_gap+50)), _label, fill="black", font=f)
        
def createColorMap(self, label):
        try:
            self.add_gap = 0
            if(self.gapBetweenHeatmaps > 40):
                self.add_gap = self.gapBetweenHeatmaps / 5
                
            try:
                max = self.scale.get() - self.minV
            except Exception:
                max = self.maxV - self.minV
            
            #SCALING PARAMETER
            max = 100 - self.minV                                         #damit heatmap legende zw. 0 und 100 prozent skaliert
            
            if(self.set_id_A.find("_TALLYMER") > 0):
                if(self.set_id_A.find("MEAN") > 0):
                    label = "MEAN"
                else:
                    if(self.set_id_A.find("MEDIAN") > 0):
                        label = "MEDIAN"
            if(self.set_id_A.find("_GC") > 0):
                label = "% GC"
            
            if(str(label) == "# per Mb" and str(self.set_id_A).endswith("_relative") == True):
                label = "REL"
                
            stepSize = self.searchStepSize()        
            self.colorBarToMove = []
            
            x1 = self.pswidth + 50
            y1 = 2 * self.gapBetweenHeatmaps - self.add_gap
            x2 = self.pswidth + 75
    
            y2 = 2 * self.gapBetweenHeatmaps + 256 - self.add_gap
            
            try:
                self.colorBarToMove.append(self.root.canvas.create_rectangle(x1, y1, x2, y2, fill="black", width=2))
            except Exception:
                pass

            if(self.image_export_possible == True):
                self.draw.rectangle((self.fontSizeFactor * x1, self.fontSizeFactor * y1, self.fontSizeFactor * x2, self.fontSizeFactor * y2), fill="black")       
                   
            if(stepSize == None):
                cStepSize = -1
            else:
                cStepSize = max - (max % stepSize)
            
            n = 257
            
            for h in range(0, 257):
                h2 = 256 - h
                
                try:
                    self.colorBarToMove.append(self.root.canvas.create_line(x1, y1 + h, x2, y1 + h, width=1, fill=getJetColorMapColor((h2) / 256.0)[0]))
                except Exception:
                    pass
            
                for i in range(0, self.fontSizeFactor):
                    if(self.image_export_possible == True):
                        self.draw.line((self.fontSizeFactor * x1, self.fontSizeFactor * (y1 + h) + i, self.fontSizeFactor * x2, self.fontSizeFactor * (y1 + h) + i), fill=getJetColorMapColor((h2) / 256.0)[1])
    
                cIntensity = int(math.ceil((h2 / 256.0) * max))
                
                if(int(cIntensity + math.ceil(self.minV)) % stepSize <= max / 256.0 and int(cIntensity + math.ceil(self.minV)) / stepSize < n):
                    c_value = int(cIntensity + math.ceil(self.minV))
                    c_value = c_value - c_value % stepSize
                    n = int(cIntensity + math.ceil(self.minV)) / stepSize
                    try:
                        self.colorBarToMove.append(self.root.canvas.create_text(x1 + 40, 2 * self.gapBetweenHeatmaps + h - self.add_gap, text=str(c_value), anchor="w", font=('Courier New', self.guiFontSizeAxis)))
                    except Exception:
                        pass
                    fontSize = self.fontSizeFactor * self.fontSizeSetId
                    if(self.image_export_possible == True):
                        import ImageFont
                        f = ImageFont.truetype(self.cwd + "font/cour.ttf", self.fontSizeFactor * self.fontSizeAxis)
                        self.draw.text((self.fontSizeFactor * (x1 + 40), self.fontSizeFactor * (2 * self.gapBetweenHeatmaps + h - self.fontSizeSetId / 2 - self.add_gap)), str(c_value), anchor="w", fill="black", font=f)
            
                try:
                    self.colorBarToMove.append(self.root.canvas.create_text(x1, 2 * self.gapBetweenHeatmaps + 256 + 10 - self.add_gap, anchor="w", text=str("[" + label + "]"), font=('Courier New', self.guiFontSizeAxis)))
                except Exception:
                    pass
                if(self.image_export_possible == True):
                    import ImageFont
                    f = ImageFont.truetype(self.cwd + "font/cour.ttf", self.fontSizeFactor * self.fontSizeAxis)
                    self.draw.text((self.fontSizeFactor * (x1), self.fontSizeFactor * (2 * self.gapBetweenHeatmaps + 256 + 10 - self.add_gap)), str("[" + label + "]"), fill="black", font=f)
        except Exception:
            print "createColorMap", sys.exc_info()
            sys.exit()
            
def createBarChartLegend(self, label, _position=1, _align="right"):
        self.add_gap = 0
        if(self.gapBetweenHeatmaps > 40):
            self.add_gap = self.gapBetweenHeatmaps / 5
            
        position = _position
        
        if(_align == "right"):
            x1 = self.pswidth + 100
        elif(_align == "left"):
            x1 = self.startLabel
        
        y1 = self.gapBetweenHeatmaps * position - self.add_gap
        x2 = self.pswidth + self.gapBetweenHeatmaps
        y2 = self.gapBetweenHeatmaps * position + len(self.SetIdList) * (self.fontSize + 15) - self.add_gap
        
        max = 0
        rectangle_size = 40
        
        for i in range(0, len(self.SetIdList)):
            set_id_label = self.SetIdMap.get(self.SetIdList[i])
            if(set_id_label == None):
                 set_id_label = self.SetIdList[i]
                                        
            try:
            	self.barCodeLegendToMove.append(self.root.canvas.create_text((x1 + 50), (y1 + i * (self.guiFontSizeSetid + 15)), text=str(set_id_label), anchor="w", font=('Courier New', self.guiFontSizeSetid)))
            	self.barCodeLegendToMove.append(self.root.canvas.create_rectangle(x1, (y1 + i * (self.guiFontSizeSetid + 15)) - self.guiFontSizeSetid / 2, (x1 + rectangle_size), (y1 + (i) * (self.guiFontSizeSetid + 15) + rectangle_size / 2), fill=self.colorToSetIdMap.get(self.SetIdList[i])))
            except Exception:
            	pass
            if(self.image_export_possible == True):
                import ImageFont
                f = ImageFont.truetype(self.cwd + "font/cour.ttf", self.fontSizeFactor * self.fontSizeSetId)
                self.draw.text((self.fontSizeFactor * (x1 + 50), self.fontSizeFactor * (y1 + i * (self.fontSizeSetId + 15))), str(set_id_label), font=f, fill="black")
                self.draw.rectangle((self.fontSizeFactor * x1, self.fontSizeFactor * (y1 + i * (self.fontSizeSetId + 15)), self.fontSizeFactor * (x1 + rectangle_size), self.fontSizeFactor * (y1 + (i) * (self.fontSizeSetId + 15) + rectangle_size / 2)), fill=self.colorToSetIdMap.get(self.SetIdList[i]))
        
            if(max < len(self.SetIdList[i])):
                max = len(self.SetIdList[i])
        
        self.pswidth = self.pswidth + self.gapBetweenHeatmaps + (self.guiFontSizeSetid / 2) * max
        self.pswidthExport = self.pswidthExport + self.gapBetweenHeatmaps + (self.fontSizeSetId / 2) * max
       
def getJetColorMapColor(x):
    if (x < -0.5) :
        r1 = 0.8;
        r2 = 0.8;
        r3 = 0.8;
    elif (x < 0) :
        r1 = 0.5;
        r2 = 0.5;
        r3 = 0.5;
    else:
        if(x < 0.125):
            a = x / 0.125;
            r1 = 0;
            r2 = 0;
            r3 = 0.5 + 0.5 * a;
        else:
            if (x < 0.375):
                a = (x - 0.125) / 0.25;
                r1 = 0;
                r2 = a;
                r3 = 1;
            else:
                if (x < 0.625) :
                    a = (x - 0.375) / 0.25;
                    r1 = a;
                    r2 = 1;
                    r3 = 1 - a;
                else:
                    if (x < 0.875):
                        a = (x - 0.625) / 0.25;
                        r1 = 1;
                        r2 = 1 - a;
                        r3 = 0;
                    else:
                        if (x <= 1.0):
                            a = (x - 0.875) / 0.125;
                            r1 = 1 - 0.5 * a;
                            r2 = 0;
                            r3 = 0;
                        else:
                            r1 = 1;
                            r2 = 1;
                            r3 = 1;

    triple = (int(255 * r1), int(255 * r2), int(255 * r3))
    
    r1 = hex(int(round(float(r1) * 255)))[2:]
    r2 = hex(int(round(float(r2) * 255)))[2:]
    r3 = hex(int(round(float(r3) * 255)))[2:]
    
    if(len(r1) == 1):
        r1 = "0" + r1
        
    if(len(r2) == 1):
        r2 = "0" + r2
        
    if(len(r3) == 1):
        r3 = "0" + r3
        
    return "#" + r1 + r2 + r3, triple

