#
# --------------------------------------------------------------------------------------------------
#
executable_chromoWIZ_1 = "/home/ibis/thomas.nussbaumer/workspace/chromoWIZ/src"
executable_chromoWIZ_2 = "/home/ibis/thomas.nussbaumer/workspace/chromoWIZ_2/src"
workspace = "/home/ibis/thomas.nussbaumer/workspace/chromoWIZ_2/src/test_scenario/test_scenario_1/"
#
# --------------------------------------------------------------------------------------------------
#
db_file = "/home/ibis/thomas.nussbaumer/workspace/chromoWIZ_2/src/test_scenario/barley.db"
density_table = "density_barley"
#
# --------------------------------------------------------------------------------------------------
#
set_ids = []
set_ids.append("500000_win_100000_shift__ryeSNPmarker1R_win500000_vs_barley")
set_ids.append("500000_win_100000_shift__GC_percent")
set_ids.append("500000_win_100000_shift__ryeSNPmarker2R_win500000_vs_barley")
set_ids.append("500000_win_100000_shift__ryeSNPmarker3R_win500000_vs_barley")
set_ids.append("500000_win_100000_shift__ryeSNPmarker4R_win500000_vs_barley")
set_ids.append("500000_win_100000_shift__ryeSNPmarker5R_win500000_vs_barley")
set_ids.append("500000_win_100000_shift__ryeSNPmarker6R_win500000_vs_barley")
set_ids.append("500000_win_100000_shift__ryeSNPmarker7R_win500000_vs_barley")
set_ids.append("500000_win_100000_shift__barley_cds")
#
# --------------------------------------------------------------------------------------------------
#
sh_file_no_X = "run_without_X.txt"
sh_file_X = "run_X.txt"
f_X = open(sh_file_X, "w")
f_nX = open(sh_file_no_X, "w")
#
# --------------------------------------------------------------------------------------------------
#
import os
#
# --------------------------------------------------------------------------------------------------
#
def heatmap(dir, set_id, id, f):
    cmd_ = "cd " + str(dir)
    cmd = cmd_ + ";" + "python ./visualize_data.py -c " + str(set_id) + " -d " + db_file + " -m a  -o " + str(workspace) + "/pix" + str(id) + ".png -v heatmap -s all -t " + density_table + " -x 99999;"
    f.write(str(cmd) + "\n")
#
# --------------------------------------------------------------------------------------------------
#
def linechart(dir, set_id, id, f):
    cmd_ = "cd " + str(dir)
    cmd = cmd_ + ";" + "python ./visualize_data.py -c " + str(set_id) + " -d " + db_file + " -m a  -o " + str(workspace) + "/pix" + str(id) + ".png -v linechart -s all -t " + density_table + " -x -1;"
    f.write(str(cmd) + "\n")
#
# --------------------------------------------------------------------------------------------------
#
def rel_set_id(dir, id, f):
    nmb_B_min = 5
    rel_B_pattern = "cds"
    min_intensity = 10	
    gap_allowed = 10
    export_pic_path = workspace + "/" + str(id)
    #rel_A_pattern = None    
    
    cmd_ = "cd " + str(dir) + "/test"
    cmd = cmd_ + ";" + "python relative_set_ids.py " + db_file + " " + density_table + " " + str(nmb_B_min) + " " + str(rel_B_pattern) + " " + str(min_intensity) + " " + str(gap_allowed) + " " + str(export_pic_path) + ";"
    f.write(str(cmd) + "\n")
#
# --------------------------------------------------------------------------------------------------
#
def stacked(dir,id,_set_ids):
    cmd_ = "cd " + str(dir)
    cmd=cmd_+ ";" +"python ./visualize_data.py -c "+(_set_ids)+" -d "+db_file+" -m p -o " + str(workspace) + "/pix"+str(id)+".png -s all -t " + density_table + " -v stacked -x 5,10,5,10,5,10,5   -y seq"
    print cmd
    os.system(cmd)
#
# --------------------------------------------------------------------------------------------------
#
def stacked2(dir,id,_set_ids):
    cmd_ = "cd " + str(dir)
    cmd=cmd_+ ";" +"python ./visualize_data.py -c "+(_set_ids)+" -d "+db_file+" -m p -o " + str(workspace) + "/pix"+str(id)+".png -s all -t " + density_table + " -v stacked -x 5,10 -y set"
    print cmd
    os.system(cmd)
#
# --------------------------------------------------------------------------------------------------
#
def stacked3(dir,id,_set_ids):
    cmd_ = "cd " + str(dir)
    cmd=cmd_+ ";" +"python ./visualize_data.py -c "+(_set_ids)+" -d "+db_file+" -m p -o " + str(workspace) + "/pix"+str(id)+".png -s all -t " + density_table + " -v stacked"
    print cmd
    os.system(cmd)
#
# --------------------------------------------------------------------------------------------------
#
import sys
#_set_ids=set_ids[1]+","+set_ids[6]+","+set_ids[8]
#stacked(executable_chromoWIZ_2,"stacked",_set_ids)
#_set_ids=set_ids[1]+","+set_ids[6]+","+set_ids[8]
#stacked2(executable_chromoWIZ_2,"stacked_2",_set_ids)
#_set_ids=set_ids[1]+","+set_ids[6]+","+set_ids[8]
#stacked3(executable_chromoWIZ_2,"stacked_3",_set_ids)
#
# --------------------------------------------------------------------------------------------------
#
#heatmap(executable_chromoWIZ_1, set_ids[6], "old_heatmap_1", f_X)
#heatmap(executable_chromoWIZ_2, set_ids[6], "new_heatmap_1", f_X)
#heatmap(executable_chromoWIZ_2, set_ids[6], "new_heatmap_1_nX", f_nX)
#
# ----------------------------------------------------------------------------------------------------
#
#linechart(executable_chromoWIZ_1, set_ids[6], "old_linechart_1", f_X)
#linechart(executable_chromoWIZ_2, set_ids[6], "new_linechart_1", f_X)
#linechart(executable_chromoWIZ_2, set_ids[6], "new_linechart_1_nX", f_nX)
#
# ----------------------------------------------------------------------------------------------------
#
#rel_set_id(executable_chromoWIZ_1, "old", f_X)
#rel_set_id(executable_chromoWIZ_2, "new_no_X", f_nX)
#rel_set_id(executable_chromoWIZ_2, "new_X", f_X)
#
f_nX.close()
f_X.close()
# ----------------------------------------------------------------------------------------------------


# 

