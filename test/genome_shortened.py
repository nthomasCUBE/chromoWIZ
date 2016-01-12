import sys
import random
sys.path.append('/nfs/plant/data/repeats/heatmaps_Thomas/software/biopython-1.54')
#sys.path.append('C:/heatmap_Thomas/biopython-1.54')
from Bio import SeqIO
from Bio.Seq import Seq
    
seq_file = "/nfs/plant/data/repeats/heatmaps_Thomas/test_runs/extract_border_3/shorter_sequence/MicromonasCCMP1545.fasta"
gff3_file = "/nfs/plant/data/repeats/heatmaps_Thomas/Micromonas_Mp_validated_28Jan10/GFF/CCMP1545.FGC_20090403_cds.gff3"

min_size = 100000
max_size = 500000

seq_file_export = "Micromonas_test_" + str(min_size) + "_" + str(max_size) + ".seq"
gff3_file_export = "Micromonas_test.gff3_" + str(min_size) + "_" + str(max_size) + ""

seq_len_map = {}

# SEQUENCE

fh=open(seq_file_export,"w")
for seq_record in SeqIO.parse(seq_file, "fasta"):
    if(len(seq_record.seq) > min_size):
        c_max = len(seq_record.seq)
        if(len(seq_record.seq) > max_size):
            c_max = max_size
        seq_len_map[str(seq_record.id)] = (c_max)
        fh.write(">"+seq_record.id+"\n")
        fh.write(str(seq_record.seq[0:c_max])+"\n")
fh.close()


# GFF3  
      
fh = open(gff3_file, "r")
fh_w=open(gff3_file_export,"w")
for line in fh.readlines():
    line = line.strip()
    values = line.split("\t")
    seq_lower_coor = -1
    seq_upper_coor = -1
    if(len(values) == 9):
        seq_lower_coor = int(values[3])
        seq_upper_coor = int(values[4])
        seq_id = (values[0])
        if(seq_id in seq_len_map.keys()):
          if(seq_upper_coor < seq_len_map[seq_id]):
              fh_w.write(line+"\n")
    else:
        fh_w.write(line+"\n")
fh_w.close()
fh.close()

