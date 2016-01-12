import sqlite_methods

def parse(tab_file, anno_id, genome_id, db_name, tab_type):
    entries = {}
    file_handler_2 = open(tab_file, "r")    
    entry = None
    
    for line in file_handler_2:
        values = line.split()
        
        if(tab_type[0]==str(values[1])):
            entry = {}
            start=int(values[3])
            stop=int(values[4])
            seq_id=values[2]
            strand="+"
            name=values[0]
            
            if(start>=stop):
                h=start
                start=stop
                stop=h
                strand="-"
            
            start=str(start)
            stop=str(stop)
    
            entry["seq_lower_coor"] = start
            entry["seq_upper_coor"] = stop
            entry["name"] = name
            entry["seq_id"] = seq_id
            entry["freq_coor"] = start + ";" + stop
            entry["strand"] = strand
    
            entries[entry["name"]] = entry
    if(len(entries)>0):
        sqlite_methods.saveGFFTypeElementsInDb(entries, db_name, genome_id, anno_id, "")

def example1():
    tab_file = "./test/example1.tab"
    db_name = "./test/example1.db"
    genome_id = "Bd"
    anno_id = "CDS_genes"
    tab_type="gene"
    dic_indexes_mRNAs = parse(tab_file, anno_id, genome_id, db_name,tab_type)

#example1()