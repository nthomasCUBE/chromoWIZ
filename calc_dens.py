import sys
import math
import methods
import sqlite_methods

def get_seq_id_from_file_name(file):
    a = str(file).rfind(".")
    b = str(file).rfind("/")
    
    return str(file)[b + 1:a]

def check_min_chromosome_length_db(db_file, genome_id, min_chromosome_length):
        min_chromosome_length_db = -1
        
        try:
            min_chromosome_length_db = sqlite_methods.get_min_chromosome_length(db_file, genome_id)
        except Exception:
            pass
        
        if(min_chromosome_length_db != -1): 
            try:
                assert(int(min_chromosome_length_db) == int(min_chromosome_length))
            except AssertionError:
                print "ERROR", "check_min_chromosome_length_db", "min_chromosome_length has to be identical in all features in the db"
                print "INFO", "check_min_chromosome_length_db", "Do you want to change the value of min_chromosome_length to", min_chromosome_length_db, "? (y/n)"
                input = raw_input(">")
                while(not(input == "y" or input == "n")):
                    input = raw_input(">")
                if(input == "y"):
                    print "INFO", "check_min_chromosome_length_db", "min_chromosome_length changed"
                    min_chromosome_length = min_chromosome_length_db
                else:
                    sys.exit()
        return min_chromosome_length

def calculate_densities(anno_id, win_size, shift, genome_id, seq_dir, seq_out_dir, db_file, min_chromosome_length, conf_file, map_orig_gff,only_gc_content_calc=False):
    files = []
    density_table = "density" + "_" + genome_id
    anno_table = "anno" + "_" + genome_id

    min_chromosome_length = check_min_chromosome_length_db(db_file, genome_id, min_chromosome_length)

    methods.seq_file_to_seq_1_line(seq_dir, seq_out_dir, files, min_chromosome_length)
    
    prefix = '%s_win_%s_shift' % (win_size, shift)
    seq_ids = []
    set_id_A = prefix + "__" + str(anno_id)
    set_id_GC = prefix + "__" + str("GC_percent")
    set_id_N = prefix + "__" + str("N_percent")
    
    sqlite_methods.save_conf_file(db_file, conf_file, set_id_A)
    
    reCalculate = ""

    if(len(files)>0):
        print "INFO","calculate_densities","current density calculation for:",anno_id

    for seq_file in files:
        
        seq_id = get_seq_id_from_file_name(seq_file)
        (seq_len) = sqlite_methods.find_seq_id(db_file, seq_id)
        
        print seq_id,
            
        if(seq_len == None):
            seq_id, seq = methods.seq_1line_and_id_from_tfa(seq_file)
            seq_len = len(seq)
            seq_id = seq_id.strip()
            sqlite_methods.save_seq_id(db_file, seq_id, seq_len, seq_dir, min_chromosome_length, genome_id)
            
        seq_ids.append(seq_id)
        if(only_gc_content_calc==False):
            sqlite_methods.updateValues(db_file, anno_table, set_id_A, seq_id)

        amount_densities_expected = math.ceil(seq_len / float(shift))
        rerun_gc_n_calculation = 0
        try:
            (rerun_gc_n_calculation, reCalculate) = sqlite_methods.findFormerCalculationAndRemove(db_file, density_table, amount_densities_expected, set_id_N, set_id_GC, set_id_A, rerun_gc_n_calculation, seq_id, reCalculate)
        except Exception:
            #print "ERROR","calculate_densities",sys.exc_info()
            return
        
        (collect_N, collect_GC) = methods.GC_and_N_percent_sliding_window_calculation(seq_file, win_size, shift, density_table, set_id_GC, set_id_N)

        print len(collect_N),len(collect_GC) 

        if(only_gc_content_calc==False):
            anno_data = sqlite_methods.getAnnotations(db_file, anno_id, anno_table, seq_id)
            
            if(len(anno_data) == 0 and map_orig_gff.get(seq_id) != -1):
                seq_id_anno = map_orig_gff.get(seq_id)
                anno_data = sqlite_methods.getAnnotations(db_file, anno_id, anno_table, seq_id_anno)

        if(rerun_gc_n_calculation == 1):
            sqlite_methods.saveDensityElementsInDb([], collect_GC, db_file, density_table)

        if(only_gc_content_calc==False):
            (collect_A) = methods.calculate_densities(anno_table, anno_id, density_table, win_size, shift, seq_file, db_file,collect_N, anno_data, set_id_A)
            sqlite_methods.saveDensityElementsInDb([], collect_A, db_file, density_table)
        
    print "\n"

        
if __name__ == "__main__":
    pass
    
