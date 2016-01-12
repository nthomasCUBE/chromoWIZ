import sys
import methods
import data_to_db
import calc_dens
import extract_tab
import time

def main(argc):
    
    if(len(argc) == 0):
        print "ERROR", "extract_data", "The program expects a config file as input paramter."
        print "INFO", "USAGE:", "python ./extract_data genome_id.conf"
        sys.exit()
        
    config_file = argc[0]
    
    print "INFO", "main", "config_file_used", config_file
    
    conf, ge_map = methods.parse_config(config_file)
    
    start = time.time()
    
    anno_id_overwrite = {}

    for key in ge_map.keys():
        for key2 in ge_map[key].keys():
            conf[key2] = ge_map[key][key2]
        nmb = data_to_db.does_anno_id_already_exist(conf["db_file"], conf["genome_id"], conf["anno_id"])
        if(int(nmb) > 0):
            anno_id_overwrite[conf["anno_id"]] = 1
    
    try:
        for key in ge_map.keys():
            
            print "*****************************************************************************"
            print "Configuration parameter"
            print "-----------------------"
            for key2 in ge_map[key].keys():
                conf[key2] = ge_map[key][key2]
                print "\t", key2, "=", ge_map[key][key2]
                
            print ""    
            print ""
            
            start = time.time()
            
            if (conf.get("extract_data") != None and conf.get("extract_data") == "yes"):
                print "-----------------------"
                print "INFO\textract_data"
                if(conf.get("gff3_file") != None and conf.get("gff3_type") != None):
                    data_to_db.parse_gff(conf["gff3_file"], conf["db_file"] , conf["gff3_type"], conf["genome_id"], conf["anno_id"], anno_id_overwrite) #, conf["min_chromosome_length"])
                elif(conf.get("tab_file") != None and conf.get("tab_type") != None):
                    extract_tab.parse(conf["tab_file"], conf["anno_id"], conf["genome_id"], conf["db_file"],conf["tab_type"])
                print "INFO\textract_data took:\t", int(time.time() - start), "seconds"    
                print "-----------------------"
                start = time.time()
            
            if (conf.get("calc_densities") != None and conf.get("calc_densities") == "yes"):
                print "-----------------------"
                print "INFO\tcalc_densities"
                calc_dens.calculate_densities(conf["anno_id"], conf["win_size"], conf["shift"], conf["genome_id"], conf["seq_file"], conf["seq_out_dir"], conf["db_file"], conf["min_chromosome_length"], config_file, conf["orig_gff"], False)
                print "INFO\tcalc_densities took:\t", int(time.time() - start), "seconds"
                print "-----------------------"
                start = time.time()
    
        if (conf.get("calc_densities") != None and len(ge_map) == 0):
            print "-----------------------"
            print "INFO\tcalc_densities"
            calc_dens.calculate_densities(conf["anno_id"], conf["win_size"], conf["shift"], conf["genome_id"], conf["seq_file"], conf["seq_out_dir"], conf["db_file"], conf["min_chromosome_length"], config_file, conf["orig_gff"])
            print "INFO\tcalc_densities took:\t", int(time.time() - start), "seconds"
            print "-----------------------"
            start = time.time()
    
        print "*****************************************************************************"
            
    except KeyError:
        print sys.exc_info()
        print "ERROR", "extract_data", "property ", sys.exc_info()[1], "not defined in config file"
        
if __name__ == "__main__":
    main(sys.argv[1:])
    
