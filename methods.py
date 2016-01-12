import os
import sys
import dircache
import time

def expectedParameter(confExpected):
    confExpected["extract_data"] = ["no", "yes"]
    confExpected["genome_id"] = {}
    confExpected["db_file"] = {}
    confExpected["workspace"] = {}
    
    confExpected["calc_densities"] = ["no", "yes"]
    confExpected["seq_out_dir"] = []
    confExpected["seq_file"] = {}
    confExpected["win_size"] = {}
    confExpected["shift"] = {}
    confExpected["min_chromosome_length"] = {}
    
    confExpected["extract_tallymer"] = ["no", "yes"]
    confExpected["tallymer_output_files_directory"] = []
    confExpected["kmer_size"] = []
    confExpected["anno_id_tallymer"] = {}
    
    return confExpected

def chooseNewDb(choose, conf, defaultDbName, db_list):
    if(choose == "n"):

        print "INFO", "chooseNewDb", "Please choose another database name"
        newDbName = raw_input(">")

        while((newDbName in db_list)):
            print "INFO", "chooseNewDb", "Already used database name. Please choose another one"
            newDbName = raw_input(">")
        if(len(newDbName) == 0):
            conf["db_file"] = conf["workspace"] + "/" + conf["genome_id"] + ".db"
        elif(len(newDbName) > 0):
            conf["db_file"] = conf["workspace"] + "/" + newDbName + ".db"

def findMissingParameters(confExpected, conf, blocks, paramToBlocks):
    try:
        
        seq_id_map = {}
        visible_seqs = []
            
        for key in confExpected:
            try:
                if(key != "seq_out_dir" and key != "db_file"):
                    if(conf.get(key) == None):
                        block = paramToBlocks.get(key)
                        if(block != None):
                            if(conf.get(block) != None):
                                assert(blocks.get(block) == "no")
                    if(key == "seq_dir"):
                        if os.path.isfile((conf.get(key))) == False:
                            raise Exception
                    if(key == "workspace"):
                        dir = conf["workspace"]
                        if not os.path.exists(dir):
                            os.makedirs(dir)
                        db_files = dircache.listdir(conf["workspace"])
                        db_list = []
                        conf["db_file"] = conf["workspace"] + "/" + conf["genome_id"] + ".db"
                        conf["seq_out_dir"] = conf["workspace"]
                    if(key == "gff3_file"):
                        pass
                    if(key == "gff3_type"):
                        pass
                    if(conf.get(key) != None):
                        if(len(confExpected.get(key)) > 0):
                            listOfPossibleValues = confExpected.get(key)
                            if not (conf.get(key) in listOfPossibleValues):
                                raise AssertionError
            except AssertionError:
                errmsg = "ERROR", "findMissingParameters", "parameter not found or invalid:\t" + key + "\n"
                sys.exit()
            except Exception:
                errmsg = "ERROR", "findMissingParameters", "unable to open:\t" + key + "\t" + conf.get(key) + "\n"
                sys.exit()
    except Exception:
        errmsg = "ERROR", "findMissingParameters", "config file not found or invalid:\n"
        sys.exit()
    
def find_blocks(config_file):
    f1 = open(config_file)
    count_lines = 0
    blocks = {}
    
    #####################################################################################
    blocks["extract_data"] = {}
    blocks["calc_densities"] = {}
    blocks["extract_tallymer"] = {}
    #####################################################################################
    paramToBlocks = {}
    paramToBlocks["gff3_file"] = "extract_data"
    paramToBlocks["gff3_type"] = "extract_data"
    paramToBlocks["anno_id"] = "extract_data"

    paramToBlocks["win_size"] = "calc_densities"
    paramToBlocks["shift"] = "calc_densities"
    paramToBlocks["min_chromosome_length"] = "calc_densities"

    paramToBlocks["run_tallymer_processor"] = "extract_tallymer"
    paramToBlocks["tallymer_output_files_directory"] = "extract_tallymer"
    paramToBlocks["anno_id_tallymer"] = "extract_tallymer"
    paramToBlocks["kmer_size"] = "extract_tallymer"
    #####################################################################################

    try:
        while 1:
            line = f1.readline()
            count_lines = count_lines + 1
            if not line: break
            line = line.strip()
            try:
                if(str(line).find("#") >= 0):
                    line = str(line).rpartition("#")[0]
                    
                if((len(line) == 0 or line[0] == "#") == 0):
                    valuePair = line.split("::")
                    key = valuePair[0].strip()
                    value = valuePair[1].strip()
                    if(key in blocks.keys()):
                        assert(value == "yes" or value == "no")
                        blocks[key] = value
            except Exception:
                print "ERROR", "find_blocks", "line:\t" + str(count_lines) + "\tinvalid parameter\n"
                sys.exit()
    except Exception:
        print "ERROR", "find_blocks", "line:\t" + str(count_lines) + "\tinvalid parameter\n"
        sys.exit()
                
    assert(len(blocks.keys()) == 3)
    
    return (blocks, paramToBlocks)
    
    
def parse_config(config_file):
    
    (blocks, paramToBlocks) = find_blocks(config_file)
    
    conf = {}
    
    confExpected = {}
    confExpected = expectedParameter(confExpected)
    
    f1 = open(config_file)

    count_lines = 0
    
    ge_map = {}
    counter = 0
    seq_ids_orig_gff = {}
    seq_ids_orig_tallymer = {}
    
    try:
        while 1:
            line = f1.readline()
            count_lines = count_lines + 1
            if not line: break
            line = line.strip()
            
            try:
                if(str(line).find("#") >= 0):
                    line = str(line).rpartition("#")[0]
                    
                if((len(line) == 0 or line[0] == "#") == 0):
                    valuePair = line.split("::")
                    key = valuePair[0].strip()
                    value = valuePair[1].strip()
                    conf[key] = value
                    
                    enable_param = "yes"
                    
                    if(paramToBlocks.get(key) != None):
                        enable_param = blocks.get(paramToBlocks.get(key))
                           
                    if(enable_param == "yes"):
                        if(key == "gff3_file" or key=="tab_file"):
                            if os.path.isfile(value) == False:
                                    raise Exception
                        elif(key == "seq_file"):
                            if os.path.isfile(value) == False:
                                    raise Exception
                        if(line.find("seq_id_orig") != -1 and line.find("seq_id_gff") != -1 and line.find("seq_id_gff") > line.find("seq_id_orig")):
                            values = line.split("::")
                            seq_ids_orig_gff[str(values[2]).strip()] = str(values[3]).strip()
                        elif(line.find("seq_id_orig") != -1 and line.find("seq_id_gff") != -1 and line.find("seq_id_gff") < line.find("seq_id_orig")):
                            values = line.split("::")
                            seq_ids_orig_gff[str(values[3]).strip()] = str(values[2]).strip()
                        if(line.find("seq_id_orig") != -1 and line.find("seq_id_tallymer") != -1 and line.find("seq_id_orig") < line.find("seq_id_tallymer")):
                            values = line.split("::")
                            seq_ids_orig_tallymer[str(values[2]).strip()] = str(values[3]).strip()
                        elif(line.find("seq_id_orig") != -1 and line.find("seq_id_tallymer") != -1 and line.find("seq_id_orig") > line.find("seq_id_tallymer")):
                            values = line.split("::")
                            seq_ids_orig_tallymer[str(values[3]).strip()] = str(values[2]).strip()
    
                        if(conf.get("anno_id") != None):
                            ge_map[counter] = {}
                            ge_map[counter]["anno_id"] = conf.get("anno_id")
                        if(conf.get("anno_id") != None and conf.get("tab_type") != None and conf.get("tab_file") != None):
                            ge_map[counter]["tab_file"] = conf.get("tab_file")
                            ge_map[counter]["tab_type"] = conf.get("tab_type")
                        
                            typesAsString = ge_map[counter]["tab_type"].split(",")
                            types = []
                            for type in typesAsString:
                                type = type.strip()
                                types.append(type)
                            ge_map[counter]["tab_type"] = types
                                
                            counter = counter + 1
                            
                            conf["anno_id"] = None
                            conf["tab_type"] = None
                            conf["tab_file"] = None

                        if(conf.get("anno_id") != None and conf.get("gff3_type") != None and conf.get("gff3_file") != None):
                            ge_map[counter]["gff3_file"] = conf.get("gff3_file")
                            ge_map[counter]["gff3_type"] = conf.get("gff3_type")
                        
                            typesAsString = ge_map[counter]["gff3_type"].split(",")
                            types = []
                            for type in typesAsString:
                                type = type.strip()
                                types.append(type)
                            ge_map[counter]["gff3_type"] = types
                                
                            counter = counter + 1
                            
                            conf["anno_id"] = None
                            conf["gff3_type"] = None
                            conf["gff3_file"] = None
                        
            except IndexError:
                print "ERROR", "parse_config", "line:\t" + str(count_lines) + "\tinvalid or missing parameter\n"
                sys.exit()
            except Exception:
                print "ERROR", "parse_config", "parse_config", "line:\t" + str(count_lines) + "\tinvalid parameter\n"
                sys.exit()
        f1.close()
        
        findMissingParameters(confExpected, conf, blocks, paramToBlocks)
    
    except Exception:
        print "ERROR", "parse_config", "line:\t" + str(count_lines) + "\tinvalid config file\n"
        sys.exit()

    conf["orig_gff"] = seq_ids_orig_gff
    conf["orig_tallymer"] = seq_ids_orig_tallymer
    
    return (conf, ge_map)

def export_seq_1_line(seq_id, seq, seq_out_dir):
    fileName = ""
    seqFileName = ""
    try:
        seq_id = seq_id.strip()
        seqFileName = seq_id[1:]
        
        if(not os.path.exists(fileName)):
            
            fileName = seq_out_dir + "/" + seqFileName + ".fa"
                        
            f = open(fileName, "w")
            try:
                f.write(seq_id + "\n")
                f.write(seq)
            finally:
                f.close()
        else:
            print "INFO", "export_seq_1_line", fileName, "already exists"
    except Exception:
        print "ERROR", "export_seq_1_line", "Unable to split seq files into single seq files"
    return fileName
                   
def seq_file_to_seq_1_line(seq_dir, seq_out_dir, files, min_chromosome_length):
    f1 = open(seq_dir)
    
    seq_id = seq = ""
    
    dirname = "sequences"
    
    if not os.path.isdir(seq_out_dir + "/" + dirname + "/"):
        os.mkdir(seq_out_dir + "/" + dirname + "/")
    
    seq_out_dir = seq_out_dir + "/" + dirname

    while 1:
        line = f1.readline()
        
        if not line: break
        
        if(len(line) > 0 and line[0] == ">"):
            if(len(seq_id) > 0):
                seq_id = seq_id.split(" ")[0]
                
                if(len(seq) > int(min_chromosome_length)):
                    files.append(export_seq_1_line(seq_id, seq, seq_out_dir))

            seq_id = line
            seq = ""
        else:
            seq = seq + line
            
    f1.close()
    
    if(len(seq) > int(min_chromosome_length)):
        seq_id = seq_id.split(" ")[0]
        files.append(export_seq_1_line(seq_id, seq, seq_out_dir))
    


def seq_1line_and_id_from_tfa(seq_file):
    ary = open(seq_file).readlines()
    seq_id = ary[0][1:] 
    seq = []
    for line in ary[1:]:
        line = line.strip()
        if not line == '':
            seq.append(line)
    
    seq = ''.join(seq)
    
    return seq_id, seq    


def GC_and_N_percent_sliding_window_calculation(seq_file, window_size, shift_length, density_table, set_id_GC, set_id_N):
    seq_id, seq = seq_1line_and_id_from_tfa(seq_file)
    
    collect_N = []
    collect_GC = []
    
    window_no = 0    
    seq_len = len(seq)
    
    shift_length = int(shift_length)
    window_size = int(window_size)
    
    for lower in range(1, seq_len + 1, shift_length):
        window_no += 1
        upper = lower + window_size - 1
        real_upper = upper
        real_window_size = window_size

        factor_winsize = 1 
        if upper > seq_len:
            real_upper = seq_len
            real_window_size = seq_len - lower + 1
            factor_winsize = float(window_size) / float(real_window_size)
            
      
        window_seq = seq[lower - 1:real_upper]
        window_seq = window_seq.upper() 
        
        N_ncl = window_seq.count('N') 
        nonN_ncl = len(window_seq) - N_ncl
        
        factor_N_content = 0 
        if nonN_ncl > 0:
            factor_N_content = float(real_window_size) / float(nonN_ncl)
        
        factor = factor_winsize * factor_N_content
        
        N_d = {}
        N_d['seq_id'] = seq_id.strip()
        N_d['set_id'] = set_id_N
        N_d['name'] = '%s_window' % (str(window_no).zfill(3))
        
        N_d['seq_lower_coor'] = lower
        N_d['seq_upper_coor'] = real_upper
        N_d['elmn_len'] = real_upper - lower + 1
        
        
        N_d['nmb_orig'] = N_ncl
        N_d['perc_orig'] = perc_float_round(N_ncl, real_window_size, 3) 
        N_d['perc'] = N_d['perc_orig'] 
        N_d['N'] = -1
        N_d['flag'] = -1
        
        collect_N.append(N_d.copy()) 
        
        GC_d = {}
        GC_d['seq_id'] = seq_id.strip()
        GC_d['set_id'] = set_id_GC
        GC_d['name'] = '%s_window' % (str(window_no).zfill(3))
        
        GC_d['seq_lower_coor'] = lower
        GC_d['seq_upper_coor'] = real_upper
        GC_d['elmn_len'] = real_upper - lower + 1
        
        GC_d['perc'] = perc_GC_float(window_seq, 3)
        GC_d['N'] = -1
        GC_d['flag'] = -1

        collect_GC.append(GC_d.copy())
    
    return collect_N, collect_GC



def calculate_densities(anno_table, anno_id, density_table, window_size, shift_length, seq_file, db_file, N_data, anno_data, set_id_A):  
    seq_id, seq = seq_1line_and_id_from_tfa(seq_file)
    seq_id = seq_id.strip()
    seq_len = len(seq)

    dummy_seq = [0] * seq_len
    elmn_seq = [0] * seq_len
    
    collect_A = []
    
    for d in anno_data:
        frag_coords = d[3] 
        
        if(d[1] > len(elmn_seq)):
            print "ERROR", "calculate_densities", "annotation element excluded, because length of FASTA sequence is smaller than annotation element position"
        else:
            elmn_seq[d[1]] = elmn_seq[d[1]] + 1
            
            frag_ul_coor = frag_coords.split(";");
            
            frag_ul_coor_integer = []
            
            for i in range(0, len(frag_ul_coor)):
                if(len(frag_ul_coor[i]) > 0):
                    frag_ul_coor_integer.append(int(frag_ul_coor[i]))
                    
            for i in range(0, len(frag_ul_coor_integer), 2):
                a = frag_ul_coor_integer[i] - 1
                b = frag_ul_coor_integer[i + 1] - 1
                
                l = b - a + 1
                dummy_seq[a:b + 1] = l * [1]
    
    window_no = 0
    counter_N = 0
    
    start = time.time()

    for currN in N_data:
        
        counter_N = counter_N + 1
        annotation_d = {}
        annotation_d['seq_id'] = currN["seq_id"]
        annotation_d['set_id'] = set_id_A
        annotation_d['name'] = currN["name"]
            
        annotation_d['seq_lower_coor'] = currN["seq_lower_coor"]
        annotation_d['seq_upper_coor'] = currN["seq_upper_coor"]
        annotation_d['elmn_len'] = currN["elmn_len"]

        window_no += 1
        lower = annotation_d['seq_lower_coor']
        upper = annotation_d['seq_lower_coor'] + int(window_size) - 1
        real_upper = annotation_d['seq_upper_coor']
        real_window_size = window_size

        factor_winsize = 1 
        
        if upper > seq_len:
            real_upper = seq_len
            real_window_size = seq_len - lower + 1
            factor_winsize = float(window_size) / float(real_window_size)
            
        window_seq = dummy_seq[lower - 1:real_upper]
        
        A_ncl = window_seq.count(1)
        
        N_perc = float(currN["perc"]) 
        
        if(N_perc < 100):
            factor_N_content = 100 / (100 - N_perc)
        else:
            factor_N_content = 9999
    
        factor = factor_winsize * factor_N_content
        
        annotation_d['perc_orig'] = perc_float_round(A_ncl, window_size, 3)
        annotation_d['perc'] = round(annotation_d['perc_orig'] * factor, 3)
        annotation_d['N'] = N_perc
        annotation_d['flag'] = 0


        nmb_elements = elmn_seq[lower - 1:real_upper]
        nmb_orig = sum(nmb_elements)

        annotation_d['nmb_orig'] = nmb_orig
        annotation_d['nmb'] = round(annotation_d['nmb_orig'] * factor, 3) / (float(window_size) / 1000000)
        
        collect_A.append(annotation_d)
        
    return collect_A

def perc_GC_float(seq, digits):
    l = len(seq.strip())
    seq = seq.upper()
    
    n = seq.count('N')
    l = l - n
    if l == 0:
        return 0
    
    gc = seq.count('G') + seq.count('C') + seq.count('S')
    gc_perc = float(gc) / float(l) * 100
    gc_perc = round(gc_perc, digits)

    return gc_perc
        
def perc_float_round(num, denum, digits):
    num = float(num)
    denum = float(denum)
    
    if not denum == 0:
        perc = num / denum * 100
        perc = round(perc, digits)
 
        return perc
    else:
        print "ERROR", "perc_float_round", "division %s/%s" % (num, denum)
        return None


def sort_seq_ids(a):
    for i in range(0, len(a)):
        for j in range(0, len(a)):
            if(len(a[i]) < len(a[j])):
                swap = a[j]
                a[j] = a[i]
                a[i] = swap
            else:
                if(len(a[i]) == len(a[j]) and str(a[i]) < str(a[j])):
                    swap = a[j]
                    a[j] = a[i]
                    a[i] = swap
    return a

if __name__ == "__main__":
    pass

