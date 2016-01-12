# -*- coding: iso-8859-1 -*-
import sys
import os
from Tkinter import *

python_path = "python"
#python_path = "C:/Python26_2/python.exe "

def import_path(fullpath):
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.append(path)
    module = __import__(filename)
    reload(module) 
    del sys.path[-1]
    return module

def test_cases_Relative_Set_Ids_Heatmaps_Barley(set, seq, dens, db, path_to_create_heatmaps, min_intensity, gap_allowed, export_pic_path="."):
    _export_pic_path = export_pic_path + "/" + set + "_heatmap.png"
    cmd_heatmap = python_path + " " + "../visualize_data.py -c " + set + " -d " + db + " -m a " + " -o " + _export_pic_path + " -v heatmap -s " + seq + " -t " + dens + " -x " + "99999"
    os.system(cmd_heatmap)
    #
    _export_pic_path = export_pic_path + "/" + set + "_linechart.png"
    cmd_linechart = python_path + " " + "../visualize_data.py -c " + set + " -d " + db + " -m a " + " -o " + _export_pic_path + " -v linechart -s " + seq + " -t " + dens + " -x " + "-1 --min_intensity=" + min_intensity + " --gap_allowed=" + gap_allowed + " --block_export_file_path=" + export_pic_path
    os.system(cmd_linechart)
    #sys.exit()
    
def start_relative_set_id(density_table, db_file, nmb_B_min, rel_B_pattern, min_intensity, gap_allowed, export_pic_path, rel_A_pattern=None):
     rel = {}
     all = {}
     seq_ids = {}

     sqlite_methods = import_path("../sqlite_methods.py")
     path_to_create_heatmaps = "../create_heatmaps.py"

     _set_ids = sqlite_methods.getSetIds(db_file, density_table)
     _seq_ids = sqlite_methods.getSeqIds(db_file, density_table, _set_ids[0][0])
     
     seq_ids = ""
     rel = []
     all = None
         
     for j in range(0, len(_seq_ids)):
             if(len(seq_ids) == 0):
                 seq_ids = _seq_ids[0][0]
                 #break
             else:    
                 seq_ids = seq_ids + "," + _seq_ids[j][0]
     
     for k in range(0, len(_set_ids)):
             c_set_id = _set_ids[k][0]
             if(c_set_id.find("relative") == -1):
                 if(str(c_set_id).find("GC_percent") == -1):
                     if(str(c_set_id).find(rel_B_pattern) != -1):
                         all = c_set_id
                     else:
                         if(rel_A_pattern == None):
                             rel.append(c_set_id)
                         elif(str(c_set_id).find(rel_A_pattern) != -1):
                             rel.append(c_set_id)
     rels_cur = rel
     alls_cur = all
     
     params = {}
     params["db_file"] = density_table
     params["density_table"] = density_table
     
    
     for rel_cur in rels_cur:
             if(rel_cur.find("_relative5") == -1):
                 set_id_new = rel_cur + "_relative5"
                 params["new_id"] = set_id_new.split("__")[1]
                 relative_set_ids(params, rel_cur, alls_cur, nmb_B_min)
                 max_value = sqlite_methods.getMaxNmbFromDatabase(db_file, density_table, set_id_new)
                 _min_intensity = str(int(round((float(min_intensity) * float(max_value[0])) / 100.0)))
                 test_cases_Relative_Set_Ids_Heatmaps_Barley(set_id_new, seq_ids, density_table, db_file, path_to_create_heatmaps, _min_intensity, gap_allowed, export_pic_path)

def relative_set_ids(params, set_id_A=None, set_id_B=None, min_nmb_B=None):
        sqlite_methods = import_path("../sqlite_methods.py")
        
        def state(set_id_A=None, set_id_B=None, min_nmb_B=None):
                
                    seq_ids_A = sqlite_methods.getSeqIds(db_file, density_table, set_id_A)
                    seq_ids_B = sqlite_methods.getSeqIds(db_file, density_table, set_id_B)
                    
                    min_nmb_B = int(min_nmb_B)
                    
                    for seq_id_A in seq_ids_A:
                        assert(seq_id_A in seq_ids_B)

                    collect_E = []

                    for seq_id_A in seq_ids_A:
                        values1 = sqlite_methods.getValuesFromDatabase(db_file, density_table, set_id_A, seq_id_A[0])
                        values2 = sqlite_methods.getValuesFromDatabase(db_file, density_table, set_id_B, seq_id_A[0])
                        
                        assert(len(values1) == len(values2))

                        new_set_id = set_id_A.split("__")[0] + "__" + params["new_id"]
                        sqlite_methods.deleteElementsInDb(db_file, density_table,new_set_id)

                        for i in range(0, len(values1)):

                            E_d = {}
                            E_d['seq_id'] = values2[i][3]
                            E_d['set_id'] = new_set_id
                            E_d['name'] = values2[i][0]
                            E_d['seq_lower_coor'] = values2[i][1]
                            E_d['seq_upper_coor'] = values2[i][2]
                            E_d['elmn_len'] = values2[i][5]
                            E_d['N'] = values2[i][10]
                            E_d['flag'] = values2[i][11]
                            
                            enough_genes_in_block = False
                            
                            if(float(values2[i][7]) >= min_nmb_B):
                                enough_genes_in_block = True
                            
                            # **********************************************************************************************
                            if(values1[i][6] == "None" or values2[i][6] == "None" or float(values2[i][6]) == 0):
                                E_d['perc_orig'] = (0)
                            else:
                                if(enough_genes_in_block):
                                    E_d['perc_orig'] = 100.0 * ((float(values1[i][6])) / (float(values2[i][6])))
                                else:
                                    E_d['perc_orig'] = -1
				    E_d['flag'] = 1
				    E_d['N'] = 100
                           # **********************************************************************************************
                            if(values1[i][7] == "None" or values2[i][7] == "None" or float(values2[i][7]) == 0):
                                E_d['nmb_orig'] = (0)
                            else:
                                if(enough_genes_in_block):
                                    E_d['nmb_orig'] = 100.0 * ((float(values1[i][7])) / (float(values2[i][7])))
                                else:
                                    E_d['nmb_orig'] = -1
                                    E_d['flag'] = 1
				    E_d['N'] = 100
                            # **********************************************************************************************
                            if(values1[i][8] == "None" or values2[i][8] == "None" or float(values2[i][8]) == 0):
                                E_d['nmb'] = (0)
                            else:
                                if(enough_genes_in_block):
                                    E_d['nmb'] = 100.0 * ((float(values1[i][8])) / (float(values2[i][8])))
                                else:
                                    E_d['nmb'] = -1
                                    E_d['flag'] = 1
				    E_d['N'] = 100
                            # **********************************************************************************************
                            if(values1[i][9] == "None" or values2[i][9] == "None" or float(values2[i][9]) == 0):
                                E_d['perc'] = (0)
                            else:
                                if(enough_genes_in_block):
                                    E_d['perc'] = 100.0 * ((float(values1[i][9])) / (float(values2[i][9])))
                                else:
                                    E_d['perc'] = -1
                                    E_d['flag'] = 1
				    E_d['N'] = 100
                            # **********************************************************************************************
                            
                            collect_E.append(E_d.copy()) 
                    
                    sqlite_methods.saveDensityElementsInDb(collect_E, [], db_file, density_table)
                
        state(set_id_A, set_id_B, min_nmb_B)             
                
         
if __name__ == "__main__":
     values = sys.argv[1:]
     
     db_file = values[0]
     density_table = values[1]
     nmb_B_min = values[2]
     rel_B_pattern = values[3]
     min_intensity = values[4]
     gap_allowed = values[5]
     export_pic_path = values[6]
     rel_A_pattern = None

     # ----------------------------------------------------------------------------------------
     
     #db_file = "/nfs/plant/data/repeats/heatmaps_Thomas/ChromoWIZ_problems/021110/rice.db"
     #density_table = "density_rice"
     #nmb_B_min = "30"
     #rel_B_pattern = "cds"
     #min_intensity = "50"
     #gap_allowed = "10"
     #export_pic_path = "/nfs/plant/data/repeats/heatmaps_Thomas/ChromoWIZ_problems/021110/"
     #rel_A_pattern = ""

     try:
         rel_A_pattern = values[7]
     except Exception:
         pass
     
     start_relative_set_id(density_table, db_file, nmb_B_min, rel_B_pattern, min_intensity, gap_allowed, export_pic_path, rel_A_pattern)

    
