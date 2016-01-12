import os

#python_path = "C:/Python26_2/python.exe ../visualize_data.py "
python_path = "python ../visualize_data.py "

def heatmap_test():
    c1 = "-c 500000_win_100000_shift__GC_percent "
    d1 = "-d /nfs/plant/data/repeats/heatmaps_Thomas/test_runs/test_runs/brachy.db "
    m1 = "-m p "
    o1 = "-o /nfs/plant/data/repeats/heatmaps_Thomas/test_runs/test_runs/heatmap1.png "
    #s1 = "-s all "
    s1 = "-s Bd1,Bd2 "
    t1 = "-t density_brachy "
    v1 = "-v heatmap "
    x1 = "-x 11 "
    
    cmd_heatmaps = python_path + c1 + d1 + m1 + o1 + s1 + t1 + v1 + x1
    print cmd_heatmaps
    os.system(cmd_heatmaps)

def barchart_test():
    c4 = "-c 500000_win_100000_shift__GC_percent,500000_win_100000_shift__N_percent "
    d4 = "-d /nfs/plant/data/repeats/heatmaps_Thomas/test_runs/test_runs/brachy.db "
    o4 = "-o /nfs/plant/data/repeats/heatmaps_Thomas/test_runs/test_runs/barchart1.png "
    s4 = "-s all "
    t4 = "-t density_brachy "
    v4 = "-v barchart "
    
    cmd_stacked = python_path + c4 + d4 + o4 + s4 + t4 + v4
    print cmd_stacked
    os.system(cmd_stacked)


def linechart_test():
    c2 = "-c 500000_win_100000_shift__GC_percent "
    d2 = "-d /nfs/plant/data/repeats/heatmaps_Thomas/test_runs/test_runs/brachy.db "
    m2 = "-m p "
    o2 = "-o /nfs/plant/data/repeats/heatmaps_Thomas/test_runs/test_runs/linechart1.png "
    s2 = "-s all "
    t2 = "-t density_brachy "
    v2 = "-v linechart "
    x2 = "-x 99999 "
    
    cmd_linechart = python_path + c2 + d2 + m2 + o2 + s2 + t2 + v2 + x2
    print cmd_linechart
    os.system(cmd_linechart)

def stacked_test():
    c3 = "-c 500000_win_100000_shift__GC_percent,500000_win_100000_shift__hv6hs_scri_vs_brachy "
    d3 = "-d /nfs/plant/data/repeats/heatmaps_Thomas/test_runs/test_runs/brachy.db "
    m3 = "-m p "
    o3 = "-o /nfs/plant/data/repeats/heatmaps_Thomas/test_runs/test_runs/stacked1.png "
    s3 = "-s all "
    t3 = "-t density_brachy "
    v3 = "-v stacked "
    
    cmd_stacked = python_path + c3 + d3 + m3 + o3 + s3 + t3 + v3
    print cmd_stacked
    os.system(cmd_stacked)

# **************
print "heatmap_test"
heatmap_test()

print "barchart_test"
barchart_test()

print "linechart_test"
linechart_test()

print "stacked_test"
stacked_test()
# **************




