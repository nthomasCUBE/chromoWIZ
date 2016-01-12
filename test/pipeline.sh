rm *png
rm *tab

SRC=/home/ibis/mihaela.martis/myScripts/genomeZipper_pipeline/gzPipeline_jun14/chromoWIZ/
DB=/nfs/plantsp/bigstorage/data/Tritex/project_results/ryeB/check_origin_ryeB454_on_sc/sqllitedb/Sc.db

A=$DB
B=density_Sc
C=20
D=cds
E=10
F=10
G=/nfs/plantsp/bigstorage/data/Tritex/project_results/ryeB/
H=

cd chromoWIZ/src/test;python relative_set_ids.py $A $B $C $D $E $F $G $H
