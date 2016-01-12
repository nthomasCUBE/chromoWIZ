# first step, it needs creating the SQLite-database on the basis of this configuration file

#python extract_data.py chromoWIZ.conf

# now, the SQLitge-database allows to generate visualisations

/usr/bin/python /scratch/nussbaumer/MUNICH/CHROMOWIZ/chromoWIZ/src/visualize_data.py -c 500000_win_100000_shift__CDS_predicted -d ../data/Bd/Bd.db -m a -o ../data/chromoWIZ.png -s all -t density_Bd -v heatmap -x 100


