#
# --------------------------------------------------------------------------------------------------
#
executable_chromoWIZ_2 = "/home/ibis/thomas.nussbaumer/workspace/chromoWIZ_2/src"
workspace = "/nfs/plant/data/repeats/heatmaps_Thomas/test_runs/michael_testrun/"
#
# --------------------------------------------------------------------------------------------------
#
db_file = "/nfs/plant/data/repeats/heatmaps_Thomas/test_runs/michael_testrun/brachy.db"
density_table = "density_brachy"
#
# --------------------------------------------------------------------------------------------------
#
set_ids = []
set_id_1 = "500000_win_100000_shift__brachy1.2_cds"
set_ids.append(set_id_1)
set_id_2 = "500000_win_100000_shift__ryeESTs_vs_brachy"
set_ids.append(set_id_2)
set_id_3 = "500000_win_100000_shift__SNP_contigs"
#set_ids.append(set_id_3)
set_id_4 = "500000_win_100000_shift__SNP_contigs_hetero"
#set_ids.append(set_id_4)
#
set_ids_2 = []
set_ids_2.append(set_id_1)
set_ids_2.append(set_id_2)
set_ids_2.append(set_id_3)
set_ids_2.append(set_id_4)
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
    print cmd
    os.system(cmd)
    f.write(str(cmd) + "\n")
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
import sys
#
c_set_ids = ""
for _set_id in set_ids:
    print _set_id
    if(len(c_set_ids) > 0):
        c_set_ids = c_set_ids + "," + _set_id
    else:
        c_set_ids = _set_id
#        
c_set_ids_2 = ""
for _set_id in set_ids_2:
    print _set_id
    if(len(c_set_ids_2) > 0):
        c_set_ids_2 = c_set_ids_2 + "," + _set_id
    else:
        c_set_ids_2 = _set_id
#        
stacked3(executable_chromoWIZ_2, "stacked_2", c_set_ids)
linechart(executable_chromoWIZ_2, set_id_3, "linechart_1", f_X)
linechart(executable_chromoWIZ_2, set_id_4, "linechart_2", f_X)
stacked3(executable_chromoWIZ_2, "stacked_4", c_set_ids_2)
#
f_nX.close()
f_X.close()
# ----------------------------------------------------------------------------------------------------


# 

