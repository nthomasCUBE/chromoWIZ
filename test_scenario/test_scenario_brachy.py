#
# --------------------------------------------------------------------------------------------------
#
executable_chromoWIZ_1 = "/home/ibis/thomas.nussbaumer/workspace/chromoWIZ/src"
executable_chromoWIZ_2 = "/home/ibis/thomas.nussbaumer/workspace/chromoWIZ_2/src"
workspace = "/home/ibis/thomas.nussbaumer/workspace/chromoWIZ_2/src/test_scenario/test_scenario_1/"
#
# --------------------------------------------------------------------------------------------------
#
db_file = "/nfs/plant/data/repeats/heatmaps_Thomas/ChromoWIZ_problems/171110/brachy/brachy.db"
density_table = "density_brachy"
#
# --------------------------------------------------------------------------------------------------
#
set_ids2 = []
set_ids2.append("500000_win_100000_shift__ryeUnigeneAssembly_vs_brachy_relative")
set_ids2.append("500000_win_100000_shift__rye1r_snpmarker_vs_brachy_relative")
set_ids2.append("500000_win_100000_shift__rye2r_snpmarker_vs_brachy_relative")
set_ids2.append("500000_win_100000_shift__rye3r_snpmarker_vs_brachy_relative")
set_ids2.append("500000_win_100000_shift__rye4r_snpmarker_vs_brachy_relative")
set_ids2.append("500000_win_100000_shift__rye5r_snpmarker_vs_brachy_relative")
set_ids2.append("500000_win_100000_shift__rye6r_snpmarker_vs_brachy_relative")
set_ids2.append("500000_win_100000_shift__rye7r_snpmarker_vs_brachy_relative")

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
def heatmap(dir, set_id, id, f, max):
    cmd_ = "cd " + str(dir)
    cmd = cmd_ + ";" + "python ./visualize_data.py -c " + str(set_id) + " -d " + db_file + " -m a  -o " + str(workspace) + "/pix" + str(id) + ".png -v heatmap -s all -t " + density_table + " -x " + max + ";"
    os.system(cmd)
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
    os.system(str(cmd))

    f.write(str(cmd) + "\n")
#
# --------------------------------------------------------------------------------------------------
#
def set_constraint(dir, id, _set_ids):
    cmd_ = "cd " + str(dir)
    cmd = cmd_ + ";" + "python ./visualize_data.py -c " + (_set_ids) + " -d " + db_file + " -m p -o " + str(workspace) + "/pix" + str(id) + ".png -s all -t " + density_table + " -v stacked -x 1,2,3,4 -y set"
    print cmd
    os.system(cmd)
#
# --------------------------------------------------------------------------------------------------
#
def seq_constraint(dir, id, _set_ids):
    cmd_ = "cd " + str(dir)
    cmd = cmd_ + ";" + "python ./visualize_data.py -c " + (_set_ids) + " -d " + db_file + " -m p -o " + str(workspace) + "/pix" + str(id) + ".png -s all -t " + density_table + " -v stacked -x 1,2,3,4,5  -y seq"
    print cmd
    os.system(cmd)
#
# --------------------------------------------------------------------------------------------------
#
def single_constraint(dir, id, _set_ids):
    cmd_ = "cd " + str(dir)
    cmd = cmd_ + ";" + "python ./visualize_data.py -c " + (_set_ids) + " -d " + db_file + " -m p -o " + str(workspace) + "/pix" + str(id) + ".png -s all -t " + density_table + " -v stacked -x -1,27,27,27,27,27,27,27,-1,27,27,27,27,27,27,27,-1,27,27,27,27,27,27,27,-1,27,27,27,27,27,27,27,-1,27,27,27,27,27,27,27  -y single"
    print cmd
    os.system(cmd)
#
# --------------------------------------------------------------------------------------------------
#
def stacked3(dir, id, _set_ids):
    cmd_ = "cd " + str(dir)
    cmd = cmd_ + ";" + "python ./visualize_data.py -c " + (_set_ids) + " -d " + db_file + " -m p -o " + str(workspace) + "/pix" + str(id) + ".png -s all -t " + density_table + " -v stacked"
    print cmd
    os.system(cmd)
#
# --------------------------------------------------------------------------------------------------
#
#rel_set_id(executable_chromoWIZ_2, "rel_set_id", f_X)
#
#_set_ids=set_ids2[0]+","+set_ids2[1]+","+set_ids2[2]+","+set_ids2[3]
#stacked3(executable_chromoWIZ_2,"stacked_no_contraint",_set_ids)
#
#_set_ids = set_ids2[0] + "," + set_ids2[1] + "," + set_ids2[2] + "," + set_ids2[3]
#seq_constraint(executable_chromoWIZ_2, "stacked_constraint_seqs", _set_ids)
#
#_set_ids = set_ids2[0] + "," + set_ids2[1] + "," + set_ids2[2] + "," + set_ids2[3]
#set_constraint(executable_chromoWIZ_2, "stacked_constraint_set_ids", _set_ids)
#
_set_ids = set_ids2[0] + "," + set_ids2[1] + "," + set_ids2[2] + "," + set_ids2[3]
#
c_set_ids = ""
for _set_id in set_ids2:
    print _set_id
    if(len(c_set_ids) > 0):
        c_set_ids = c_set_ids + "," + _set_id
    else:
        c_set_ids = _set_id
    
#
single_constraint(executable_chromoWIZ_2, "stacked_constraint_single", c_set_ids)
import sys
sys.exit()
#
# --------------------------------------------------------------------------------------------------
#    
import sys
sys.exit()
#
# --------------------------------------------------------------------------------------------------
#
for i in range(0, len(set_ids2)):
    heatmap(executable_chromoWIZ_2, str(set_ids2[i]), str(set_ids2[i]) + "_no_max", f_X, "99999")
    heatmap(executable_chromoWIZ_2, str(set_ids2[i]), str(set_ids2[i]) + "_max_" + str(i), f_X, str(i))
#
f_nX.close()
f_X.close()
# ----------------------------------------------------------------------------------------------------
# 

