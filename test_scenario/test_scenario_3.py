import os

executable_chromoWIZ_2 = "/var/www/cgi-bin/chromowiz/chromowiz/chromoWIZ_2/src"
workspace =              "/var/www/cgi-bin/chromowiz/chromowiz/chromoWIZ_2/src/test_scenario/test_scenario_3/"

db_file = "/var/www/cgi-bin/chromowiz/chromowiz/chromoWIZ_2/src/test_scenario/test_scenario_3/sorghum.db"
density_table = "density_sorghum"

set_ids2 = []
set_ids2.append("hv4hl_scriest_vs_sorghum")

def heatmap(dir, set_id, id, fh, max):
    cmd_ = "cd " + str(dir)
    cmd = cmd_ + ";" + "/usr/bin/python ./visualize_data.py -c " + str(set_id) + " -d " + db_file + " -m a  -o " + str(workspace) + "/pix" + str(id) + ".png -v heatmap -s all -t " + density_table + " -x " + max + ";"
    print cmd
    os.system(cmd)

heatmap(executable_chromoWIZ_2, str(set_ids2[0]), str(set_ids2[0]) + "_no_max", "", "99999")
