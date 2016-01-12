import sys
import sqlite_methods

def does_anno_id_already_exist(db_name, genome_id, anno_id):
    anno_table = "anno_" + genome_id
    nmb = sqlite_methods.does_annotation_exist(db_name, anno_table, anno_id)
    return nmb
      
def getAttribute(attributes, attributeName, required):
    entry = str(attributes).strip()
    entry = entry.partition(attributeName + "=")[2]
    entry = entry.partition(";")[0]
    
    if required:
        if(len(entry) == 0):
            raise NameError
    return entry

def orderGFFTypeElements(freq_coor_before_sorting):
    
    freq_coords = str(freq_coor_before_sorting).split(";");
    freq_coords_map = {}

    i = 0
    while i < len(freq_coords) - 1:
        a = int(str(freq_coords[i]))
        if(freq_coords_map.get(a) == None):
            freq_coords_map[a] = []
        list = freq_coords_map[a]
        list.append(str(freq_coords[i + 1]))
        i = i + 2

    keys = freq_coords_map.keys()
    keys.sort()
    freq_coor_sorted = ''
    
    for key in keys:
        freq_coords_map[key].sort()
        for item in freq_coords_map[key]:
            freq_coor_sorted = freq_coor_sorted + str(key) + ";" + str(item) + ";"
    
    return freq_coor_sorted
    
def stripValues(values):
    for i in range(0, len(values)):
        values[i] = values[i].strip()
    return values    
    
def checkStartEndOfGFFTypeElement(start, end, strand, count_lines):
    try:
        int(start)
    except Exception:
        errmsg = "ERROR", "checkStartEndOfGFFTypeElement", "start position invalid at pos " + str(count_lines)
        sys.stderr.write(errmsg)

    try:
        int(end)
    except Exception:
        errmsg = "ERROR", "checkStartEndOfGFFTypeElement", "end position invalid at pos " + str(count_lines)
        sys.stderr.write(errmsg)
        
    try:
        assert(strand == "+" or strand == "-" or strand == "." or strand == "?")
    except Exception:
        print "ERROR", "checkStartEndOfGFFTypeElement", "checkStartEndOfGFFTypeElement"
    
def getGFF3Types(gff3_file):

    f1 = open(gff3_file)
    count_lines = 0
    
    gff3_types = {}
    
    while 1:
        line = f1.readline()
        count_lines = count_lines + 1
        if not line: break
        line = line.strip()
        
        if(len(line) == 0 or line[0] == "#"):
            pass
        else:
            values = line.split("\t")
            values = stripValues(values)
            
            try:
                assert len(values) == 9

                id = getAttribute(values[8], "ID", False)
                gff3_types[id] = values[2]
                    
            except Exception:
                print "ERROR", "getGFF3Types", "Invalid data entry, entry has to consist of nine columns"
                sys.exit()
 
    f1.close() 

    return gff3_types

def getGFF3TypesHierarchy(gff3_file, gff3_types):

    f1 = open(gff3_file)
    
    gff3_types_ids = gff3_types.values()
    gff3_relation_map = {}
    
    while 1:
        line = f1.readline()

            
        if not line: break
        line = line.strip()
        
        if(len(line) == 0 or line[0] == "#"):
            pass
        else:
            values = line.split("\t")
            values = stripValues(values)
            
            try:

                assert len(values) == 9

                parents = getAttribute(values[8], "Parent", False)
                parents = parents.split(",")
                
                for parent in parents:
                    if(len(parent) > 0):
                        if(gff3_types.get(parent) != None):
                            if(gff3_relation_map.get(gff3_types.get(parent)) == None):
                                gff3_relation_map[gff3_types.get(parent)] = {}
                            gff3_relation_map[gff3_types.get(parent)][values[2]] = 1
                    
            except Exception:
                print "ERROR", "getGFF3TypesHierarchy", sys.exc_info()
                sys.exit()
 
    f1.close() 

    return gff3_relation_map
    
def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

def parse_gff(gff3_file, db_name, allowed_gff3_types, genome_id, anno_id, anno_id_overwrite): #, min_chromosome_length):
    try:
        
        #min_chromosome_length = check_min_chromosome_length_db(db_name, genome_id, min_chromosome_length)
        dic_indexes_parents = {}
        nodes_line_indexes = {}
        
        gff3_types = getGFF3Types(gff3_file)
        gff3_relation_map = getGFF3TypesHierarchy(gff3_file, gff3_types)
        
        for key in gff3_relation_map.keys():
            gff3_relation_map[key] = gff3_relation_map[key].keys()
            
        hierarchy = {}
            
        for allowed_gff3_type1 in allowed_gff3_types:
            for allowed_gff3_type2 in allowed_gff3_types:
                paths = find_all_paths(gff3_relation_map, allowed_gff3_type1, allowed_gff3_type2)
                
                for path in paths:
                    
                    path_possible = True
                    
                    for allowed_gff3_type3 in allowed_gff3_types:
                        try:
                            (path.index(allowed_gff3_type3) == -1)
                        except Exception:
                            path_possible = False
                    
                    if(path_possible):
                        level = 0
                
                        for node in path:
                            level = level + 1
                            if(hierarchy.get(level) == None):
                                hierarchy[level] = {}
                            hierarchy[level][node] = 1
                        assert(len(paths[0]) == len(path))
                    
        gff3_children = hierarchy.get(len(hierarchy))
        gff3_parents = hierarchy.get(len(hierarchy) - 1)
        
        index_list_parents_parents_allowed = extractElementsToRemove(gff3_file, hierarchy)
        index_list_parents = extractElements(gff3_file, gff3_parents, index_list_parents_parents_allowed)
        index_list_parents = extractFragments(gff3_file, gff3_children, index_list_parents)

        sqlite_methods.saveGFFTypeElementsInDb(index_list_parents, db_name, genome_id, anno_id, anno_id_overwrite)
    except Exception:
        print "ERROR", "parse_gff", sys.exc_info()

def extractElementsToRemove(gff3_file, hierarchy):

    index_list_parents = {}
    
    c_key_id_list = {}
    c_key_id_list2 = {}
    
    for i in range(1, (len(hierarchy.keys()) - 2) + 1):
        c_key = hierarchy.get(i).keys()[0]
        
        f1 = open(gff3_file)
        count_lines = 0
        
        while 1:
            line = f1.readline()
            count_lines = count_lines + 1
            if not line: break
            line = line.strip()
            
            if(len(line) == 0 or line[0] == "#"):
                pass
            else:
                values = line.split("\t")
                values = stripValues(values)
                
                try:
    
                    assert len(values) == 9
                    
                    if(i == 1):
                        if values[2] in c_key:  
        
                            checkStartEndOfGFFTypeElement(values[3], values[4], values[6], count_lines)
                            c_id = getAttribute(values[8], "ID", False)
                            c_key_id_list[c_id] = 1
                    else:
                        if values[2] in c_key:  

                            c_id = getAttribute(values[8], "ID", False)
                            c_parents = getAttribute(values[8], "Parent", False)
                            c_parents = c_parents.split(",")
        
                            for c_parent in c_parents:
                                if(c_parent in c_key_id_list.keys()):
                                    c_key_id_list2[c_id] = 1
                        
                except Exception:
                    print "ERROR", "extractElementsToRemove", sys.exc_info()
                    sys.exit()
        f1.close() 
        if(len(c_key_id_list2) > 0):
            c_key_id_list = c_key_id_list2

    return c_key_id_list

def extractElements(gff3_file, gff3_type, index_list_parents_parents_allowed):

    f1 = open(gff3_file)
    count_lines = 0
    
    parentIds = {}
    elementIds = {}
    
    index_list_parents = {}
    
    while 1:
        line = f1.readline()
        count_lines = count_lines + 1
        if not line: break
        line = line.strip()
        
        if(len(line) == 0 or line[0] == "#"):
            pass
        else:
            values = line.split("\t")
            values = stripValues(values)
            
            try:
                assert len(values) == 9
                
                if(gff3_type==None):
                    print "extractElements",sys.exc_info()
                    print "ERROR","unable to store elements into db, maybe declaration of gff3_types is wrong"
                    sys.exit()
                    
                if values[2] in gff3_type:  

                    checkStartEndOfGFFTypeElement(values[3], values[4], values[6], count_lines)
    
                    c_id = getAttribute(values[8], "ID", False)

                    parents = getAttribute(values[8], "Parent", False)
                    parents = parents.split(",")

                    parent_allowed = False
                    
                    if(len(index_list_parents_parents_allowed) > 0):
                        for parent in parents:
                            if(parent in index_list_parents_parents_allowed):
                                parent_allowed = True
                    else:
                        parent_allowed = True
                        
                    if(parent_allowed == True):
                        infos = {}
                        infos["seq_id"] = values[0]
                        infos["seq_lower_coor"] = values[3]
                        infos["seq_upper_coor"] = values[4]
                        infos["strand"] = values[6]   
                        infos["freq_coor"] = ""
                   
                        index_list_parents[c_id] = infos
            except Exception:
                print line
                print "ERROR", "extractElements", sys.exc_info()
                sys.exit()
 
    f1.close() 

    return index_list_parents

def extractFragments(gff3_file, gff3_type, index_list_parents):

    f1 = open(gff3_file)
    count_lines = 0
    
    parentIds = {}
    elementIds = {}
    
    while 1:
        line = f1.readline()
        count_lines = count_lines + 1
        if not line: break
        line = line.strip()
        
        if(len(line) == 0 or line[0] == "#"):
            pass
        else:
            values = line.split("\t")
            values = stripValues(values)
            
            try:

                assert len(values) == 9
                
                if values[2] in gff3_type:  

                    checkStartEndOfGFFTypeElement(values[3], values[4], values[6], count_lines)
    
                    parents = getAttribute(values[8], "Parent", False)
                    parents = parents.split(",")

                    for parent in parents:
                        if(len(parent) > 0):
                            if(index_list_parents.get(parent) != None):
                                infos = index_list_parents.get(parent)
                                
                                if(int(values[3]) < int(values[4])):
                                    infos["freq_coor"] = infos["freq_coor"] + str(values[3]) + ";" + str(values[4]) + ";"
                                else:
                                    infos["freq_coor"] = infos["freq_coor"] + str(values[4]) + ";" + str(values[3]) + ";"
    
                                index_list_parents[parent] = infos
                            
            except Exception:
                print "ERROR", "extractFragments", sys.exc_info()
    f1.close() 

    return index_list_parents

def find_gff3_types(file_path):
        gff3_types = {}
        
        f = open(file_path)
        for line in f.readlines():
            values = str(line).split("\t")

            if(len(values) == 9):
                gff3_types[values[2]] = 1

        return gff3_types
    
def path_possible(gff3_file):
  
        gff3_types = find_gff3_types(gff3_file)
        values = gff3_types
        _allowed_gff_types_map = {}

        for value in values:
            _allowed_gff_types_map[value] = 1
        
        allowed_gff3_types = _allowed_gff_types_map.keys()

        gff3_types = None
        gff3_relation_map = None
        found_paths = {}
        for allowed_gff3_type2 in allowed_gff3_types:
            for allowed_gff3_type2_2 in allowed_gff3_types:
                (gff3_types, gff3_relation_map) = _path_possible(gff3_file, allowed_gff3_type2_2, allowed_gff3_type2, gff3_types, gff3_relation_map, found_paths)

        return found_paths.keys()
        
def _path_possible(gff3_file, gff3_type_1, gff3_type_2, gff3_types=None, gff3_relation_map=None, found_paths=None):
    try:
        if(gff3_types == None):
            gff3_types = getGFF3Types(gff3_file)
        
        
        if(gff3_relation_map == None):
            gff3_relation_map = getGFF3TypesHierarchy(gff3_file, gff3_types)

        allowed_gff3_types = []
        allowed_gff3_types.append(gff3_type_1)
        allowed_gff3_types.append(gff3_type_2)
        
        gff3_relation_map2 = {}
        
        for key in gff3_relation_map.keys():
            gff3_relation_map2[key] = gff3_relation_map[key].keys()
                    
            hierarchy = {}
                    
            for allowed_gff3_type1 in allowed_gff3_types:
                for allowed_gff3_type2 in allowed_gff3_types:
                    paths = find_all_paths(gff3_relation_map2, allowed_gff3_type1, allowed_gff3_type2)
                        
                    for path in paths:
                            
                        path_possible = True
                            
                        for allowed_gff3_type3 in allowed_gff3_types:
                            try:
                                (path.index(allowed_gff3_type3) == -1)
                            except Exception:
                                path_possible = False
                            
                        if(path_possible):
                            
                            level = 0
                        
                            #path.sort()
                            path.reverse()
                            
                            path_config_string = ""
                            if(len(path) > 1):
#                            if(len(path)==2):
                                for path_e in path:
                                    if(len(path_config_string) == 0):
                                        path_config_string = path_e
                                    else:
                                        path_config_string = path_config_string + "," + path_e
                                    
                                if(found_paths.get(path_config_string) == None):
                                    found_paths[path_config_string] = 1
                                
                                
                                for node in path:
                                    level = level + 1
                                    if(hierarchy.get(level) == None):
                                        hierarchy[level] = {}
                                    hierarchy[level][node] = 1
                                assert(len(paths[0]) == len(path))
    except Exception:
        print "ERROR", "_path_possible", sys.exc_info()
        pass
    
    return (gff3_types, gff3_relation_map)
    
