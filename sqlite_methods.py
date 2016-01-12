# -*- coding: iso-8859-1 -*-
import sqlite3
import sys
import data_to_db
import methods
import time

def does_annotation_exist(db_name, anno_table, anno_id):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM " + anno_table + " where anno_id=:anno_id", {"anno_id":anno_id})
        nmb_annos = cursor.fetchone()[0]
        return nmb_annos
    except Exception:
        pass
    return 0

def saveDensityElementsInDb(collect_N, collect_GC, db_name, density_table, reruns=5):
    try:
        create_density_table(density_table, db_name)
        
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        
        sql = "INSERT INTO " + density_table + " VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"

        for currN in collect_N:
            values = (currN.get("name"), currN.get("seq_lower_coor"), currN.get("seq_upper_coor"), currN.get("seq_id"), currN.get("set_id"), currN.get("elmn_len"), currN.get("perc_orig"), currN.get("nmb"), currN.get("nmb_orig"), currN.get("perc"),currN.get("N"),currN.get("flag"))
            cursor.execute(sql, values)
        
        for currGC in collect_GC:
            values = (currGC.get("name"), currGC.get("seq_lower_coor"), currGC.get("seq_upper_coor"), currGC.get("seq_id"), currGC.get("set_id"), currGC.get("elmn_len"), currGC.get("perc_orig"), currGC.get("nmb"), currGC.get("nmb_orig"), currGC.get("perc"),currGC.get("N"),currGC.get("flag"))
            cursor.execute(sql, values)

        connection.commit()
    except sqlite3.OperationalError:
        print "ERROR", "saveDensityElementsInDb", "Database is locked or readonly", sys.exc_info()
        if(reruns > 0):
            time.sleep(20)
            saveDensityElementsInDb(collect_N, collect_GC, db_name, density_table, reruns - 1)
    except Exception:
        print "ERROR", "saveDensityElementsInDb", sys.exc_info()

def deleteGFFTypeElementsInDb(connection, anno_table, anno_id, density_table):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM " + anno_table + " where anno_id=:anno_id", {"anno_id":anno_id})
        print "INFO", "deleteGFFTypeElementsInDb", "previous annotation calculation deleted", anno_id
        try:
            cursor.execute("DELETE FROM " + density_table + " where set_id LIKE '%" + anno_id + "%'")
            print "INFO", "deleteGFFTypeElementsInDb", "previous density calculation deleted", anno_id
        except Exception:
            pass
        connection.commit()
    except Exception:
        pass

def deleteElementsInDb(db_name, density_table,set_id):
    try:
        try:
	    connection = sqlite3.connect(db_name)
	    cursor = connection.cursor()
            cursor.execute("DELETE FROM " + density_table + " where set_id LIKE '%" + set_id + "%'")
	    connection.commit()
        except Exception:
            pass
    except Exception:
        pass
      
      
def saveGFFTypeElementsInDb(dic_indexes_mRNAs, db_name, genome_id, anno_id, anno_id_overwrite, reruns=5,):
    try:
        
        anno_table = "anno_" + genome_id
        density_table = "density_" + genome_id
        
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS " + anno_table + "(name TEXT, seq_lower_coor INTEGER, seq_upper_coor  INTEGER, frag_coor  TEXT, strand  TEXT, seq_id  TEXT, anno_id TEXT)") 
        
        cursor.execute("SELECT COUNT(*) FROM " + anno_table + " where anno_id=:anno_id", {"anno_id":anno_id})

        nmb_annos = cursor.fetchone()[0]
        
        if(nmb_annos > 0):
            pass
        
        if(nmb_annos > 0):
            reCalculate = ""
            while(reCalculate != "y" and reCalculate != "n"):
                print "INFO", "saveGFFTypeElementsInDb", "Overwrite existing calculations? (y/n)"
                reCalculate = raw_input(">")
                reCalculate = reCalculate.strip()
                if(reCalculate == "y"):
                    if(len(anno_id_overwrite.keys()) > 1):
                        print "INFO", "saveGFFTypeElementsInDb", "Overwrite all  existing calculations? (y/n)"
                        for key in anno_id_overwrite.keys():
                            print "\t\t", "affected densities identifier:\t<", key, ">"
                        reCalculate = raw_input(">")
                        reCalculate = reCalculate.strip()
                        for c_anno_id in anno_id_overwrite.keys():
                            deleteGFFTypeElementsInDb(connection, anno_table, c_anno_id, density_table)
                    else:
                        deleteGFFTypeElementsInDb(connection, anno_table, anno_id, density_table)
                    anno_id_overwrite = {}
                #else:
                #    return()
                
        for mRNA in dic_indexes_mRNAs.keys():
            infos = dic_indexes_mRNAs[mRNA]

            if(not len(dic_indexes_mRNAs[mRNA]) == 0):
                infos["freq_coor"] = data_to_db.orderGFFTypeElements(infos["freq_coor"])
                sql = "INSERT INTO " + anno_table + " VALUES (?,?,?,?,?,?,?)"
                
                if(int(infos["seq_upper_coor"]) < int(infos["seq_lower_coor"])):
                    h = infos["seq_upper_coor"]
                    infos["seq_upper_coor"] = infos["seq_lower_coor"]
                    infos["seq_lower_coor"] = h

                values = (mRNA, infos["seq_lower_coor"], infos["seq_upper_coor"], infos["freq_coor"], infos["strand"], infos["seq_id"], anno_id)
                cursor.execute(sql, values)
        connection.commit()
    except sqlite3.OperationalError:
        print "ERROR", "saveGFFTypeElementsInDb", "Database is locked or readonly", sys.exc_info()
        if(reruns > 0):
            time.sleep(20)
            saveGFFTypeElementsInDb(dic_indexes_mRNAs, db_name, genome_id, anno_id, reruns - 1)
    except Exception:
        print "ERROR", "saveGFFTypeElementsInDb", sys.exc_info()
        
def updateValues(db_file, anno_table, set_id, seq_id):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("UPDATE " + anno_table + " SET frag_coor=seq_lower_coor ||  \";\" || seq_upper_coor || \";\" WHERE length(frag_coor)=0")
        connection.commit()
    except Exception:
        print "ERROR", "updateValues", "no existing annotation calculation in order to calculate densities"
        sys.exit()
        
def findFormerTallymerCalculationAndRemove(db_file, density_table, set_id):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
            
        create_density_table(density_table, db_file)

        cursor.execute("select * from " + density_table + " where set_id=:set_id", {"set_id": set_id})
        
        entries = cursor.fetchall()
        
        if(len(entries) > 0):
            reCalculate = ""
            while(reCalculate != "y" and reCalculate != "n"):
                print "INFO", "findFormerTallymerCalculationAndRemove", "Overwrite existing calculations? (y/n)"
                reCalculate = raw_input(">")
                reCalculate = reCalculate.strip()
                if(reCalculate == "y"):
                    cursor.execute("delete from " + density_table + " where set_id=:set_id", {"set_id": set_id})
                elif(reCalculate == "n"):
                    return
        connection.commit()

    except Exception:
        print "ERROR", "findFormerTallymerCalculationAndRemove", sys.exc_info()[1]
    
def saveValues(db_name, density_table, set_id, values, elnLenValues, seq_id, win_size, shift, seq_file):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        set_id_N = '%s_win_%s_shift__N_percent' % (win_size, shift)
        set_id_GC = '%s_win_%s_shift__GC_percent' % (win_size, shift)
        N_data = getN_Data(db_name, seq_id, set_id_N, density_table)
        
        if(len(N_data) == 0):
            print "INFO", "saveValues", "No N densities loaded in DB"
            (collect_N, collect_GC) = methods.GC_and_N_percent_sliding_window_calculation(seq_file, win_size, shift, density_table, set_id_GC, set_id_N)
            saveDensityElementsInDb(collect_N, collect_GC, db_name, density_table)
        else:
            pass
        counter = 0
        
        for value in values:
            sql = "INSERT INTO " + density_table + " VALUES (?,?,?,?,?,?,?,?,?,?)"
            counter = counter + 1
            values = ("", (counter), "", (seq_id), (set_id), (elnLenValues[counter - 1]), "", (value), "", "")
            cursor.execute(sql, values)
        
        connection.commit()

    except Exception:
        print "ERROR", "saveValues", sys.exc_info()[1]
        
def getN_Data(db_file, seq_id, set_id, table_name):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    cursor.execute("SELECT DISTINCT * from " + table_name + " where set_id=:set_id and  seq_id=:seq_id order by seq_lower_coor",
    {"seq_id": seq_id, "set_id": set_id})
   
    return cursor.fetchall()

def getAllSeqIds(db_file, density_table):
    entries = []
    
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT DISTINCT seq_id  FROM " + density_table)
            entries = cursor.fetchall()
            
        except Exception:
            print "ERROR", "getAllSeqIds", "loading seq_ids from database"
    except Exception:
        print "ERROR", "getAllSeqIds", sys.exc_info()[1]
    return entries
    
def getSeqIdsAll(db_file, anno_table):
    entries = []
    
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        
        cursor.execute("SELECT DISTINCT seq_id  FROM " + anno_table)
        entries = cursor.fetchall()
    except Exception:
        print "ERROR", "getSeqIds", sys.exc_info()[1]
    finally:
        return entries
    
def getSeqIds(db_file, density_table, set_id):
    entries = []
    
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        
        cursor.execute("SELECT DISTINCT seq_id  FROM " + density_table + " WHERE set_id=:set_id", {"set_id":set_id})
        entries = cursor.fetchall()
    except Exception:
        print "ERROR", "getSeqIds", sys.exc_info()[1]
    finally:
        return entries

    
def getSetIds(db_file, density_table):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    entries = []
    
    try:
        cursor.execute("SELECT DISTINCT set_id  FROM " + density_table + " WHERE NOT set_id LIKE '%N_percent%' ORDER BY set_id  ASC")
        entries = cursor.fetchall()
    
    except Exception:
        pass
    finally:
        return entries

def getAnnoIds(db_file, anno_table):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    entries = []
    
    try:
        cursor.execute("SELECT DISTINCT anno_id  FROM " + anno_table + " ORDER BY anno_id  ASC")
        entries = cursor.fetchall()
    
    except Exception:
        pass
    finally:
        return entries

def getNPercentSetIds(db_file, density_table):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    entries = []
    
    try:
        cursor.execute("SELECT DISTINCT set_id  FROM " + density_table + " WHERE set_id LIKE '%__N_percent%'")
        entries = cursor.fetchall()
    except Exception:
        pass
    finally:
        return entries

def getAllSetIds(db_file, density_table):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    entries = []
    
    try:
        cursor.execute("SELECT DISTINCT set_id  FROM " + density_table + " ORDER BY set_id  ASC")
        entries = cursor.fetchall()
    except Exception:
        pass
    finally:
        return entries

def getTableNames(db_file):
    entries = []
    
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE name LIKE 'density_%'");
        entries = cursor.fetchall()
    except Exception:
        print "ERROR", "getTableNames", sys.exc_info()[1]
    finally:
        return entries

def getAllTableNames(db_file):
    entries = []
    
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE name LIKE 'density_%' or name LIKE 'anno_%'");
        entries = cursor.fetchall()
    except Exception:
        print "ERROR", "getTableNames", sys.exc_info()[1]
    finally:
        return entries

def getAllTableNames2(db_file):
    entries = []
    
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master");
        entries = cursor.fetchall()
    except Exception:
        print "ERROR", "getTableNames", sys.exc_info()[1]
    finally:
        return entries

def getAllColumnNames(db_file, table_name):
    entries = []
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info("+table_name+")")
        entries = cursor.fetchall()
        
    except Exception:
        print "ERROR", "getAllColumnNames", sys.exc_info()[1]
    finally:
        return entries

def getMaxValueFromDatabase(db_file, density_table, set_id, mode):
    entry = None

    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        set_id_N = set_id.split("__")[0]
        set_id_N = set_id_N + "__N_percent"
        if(mode == "% bp"):
            cursor.execute("select MAX(d1.perc) from " + density_table + " d1," + density_table + " d2   where d1.set_id=:set_id and d2.set_id=:set_id_N and d1.name=d2.name and d1.seq_id=d2.seq_id and d2.perc<60", {"set_id":set_id, "set_id_N":set_id_N})
            entry = cursor.fetchone()[0]
        elif(mode == "# per Mb"):
            cursor.execute("select MAX(d1.nmb) from " + density_table + " d1," + density_table + " d2   where d1.set_id=:set_id and d2.set_id=:set_id_N and d1.name=d2.name and d1.seq_id=d2.seq_id and d2.perc<60", {"set_id":set_id, "set_id_N":set_id_N})
            entry = cursor.fetchone()[0]
    except Exception:
        print "ERROR", "getMaxValueFromDatabase", sys.exc_info()[1]
    finally:
        return entry

def exec_command(db_file, cmd):
    entries = []
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute(cmd)
        entries = cursor.fetchall()
    except Exception:
        print "ERROR", "exec_command", sys.exc_info()[1]
    finally:
        return entries

def getAllValuesFromDatabase(db_file, density_table):
    entries = []
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("select * from " + density_table)
        entries = cursor.fetchall()
    except Exception:
        print "ERROR", "getAllValuesFromDatabase", sys.exc_info()[1]
    finally:
        return entries
    
def getValuesFromDatabase(db_file, density_table, set_id, seq_id, bin_start=None, bin_stop=None):
    entries = []
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        if(bin_start == None and bin_stop == None):
            cursor.execute("select DISTINCT * from " + density_table + " where set_id=:set_id and seq_id=:seq_id order by seq_lower_coor,name", {"set_id":set_id, "seq_id":seq_id})
        else:
            cursor.execute("select DISTINCT * from " + density_table + " where set_id=:set_id and seq_id=:seq_id and seq_lower_coor>=:seq_lower_coor and seq_upper_coor<=:seq_upper_coor order by seq_lower_coor,name ", {"set_id":set_id, "seq_id":seq_id, "seq_lower_coor":bin_start, "seq_upper_coor":bin_stop})
        entries = cursor.fetchall()
    except Exception:
        print "ERROR", "getValuesFromDatabase", sys.exc_info()[1]
    finally:
        return entries

def getNPercentFromDatabase(db_file, density_table, set_id, seq_id, bin_start=None, bin_stop=None):
    values = set_id.split("__")
    N_set_id = values[0] + "__N_percent"
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    if(bin_start == None and bin_stop == None):
        cursor.execute("select perc from " + density_table + " where set_id=:set_id and seq_id=:seq_id order by seq_lower_coor,name", {"set_id":N_set_id, "seq_id":seq_id})
    else:
        cursor.execute("select perc from " + density_table + " where set_id=:set_id and seq_id=:seq_id order by seq_lower_coor,name and seq_lower_coor>:seq_lower_coor and seq_upper_coor<:seq_upper_coor", {"set_id":N_set_id, "seq_id":seq_id, "seq_lower_coor":bin_start, "seq_upper_coor":bin_stop})
    entry = cursor.fetchall()
    return entry

def getDensitiesDistribution(db_file, table_name):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("select AVG(perc),set_id FROM " + table_name + " GROUP BY set_id ORDER BY seq_id, set_id ASC")
        return cursor.fetchall()
    except Exception:
        print "ERROR", "getDensitiesDistribution", sys.exc_info()[1]

def getDensitiesDistributionPerChr(db_file, table_name):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("select AVG(perc),set_id,seq_id FROM " + table_name + " GROUP BY seq_id,set_id ORDER BY seq_id,set_id ASC")
    
        return cursor.fetchall()
    except Exception:
        print "ERROR", "getDensitiesDistribution", sys.exc_info()[1]

def getAmountAllAnnotations(db_file, anno_id, table_name):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        
        cursor.execute("select MAX(seq_upper_coor) from " + table_name + " where anno_id=:anno_id",
        {"anno_id": anno_id})
    
        return cursor.fetchone()
    except Exception:
        print "ERROR", "save_conf_file", sys.exc_info()[1]

def getAmountAnnotations(db_file, anno_id, table_name, seq_id):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        
        cursor.execute("select MAX(seq_upper_coor) from " + table_name + " where anno_id=:anno_id and seq_id=:seq_id",
        {"anno_id": anno_id, "seq_id":seq_id})
    
        return cursor.fetchone()
    except Exception:
        print "ERROR", "save_conf_file", sys.exc_info()[1]


def getAnnotations(db_file, anno_id, table_name, seq_id):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        
        cursor.execute("select distinct * from " + table_name + " where anno_id=:anno_id and seq_id=:seq_id",
        {"anno_id": anno_id, "seq_id":seq_id})
    
        return cursor.fetchall()
    except Exception:
        print "ERROR", "save_conf_file", sys.exc_info()[1]

def getAllAnnotations(db_file, anno_id, table_name):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        
        cursor.execute("select distinct * from " + table_name + " where anno_id=:anno_id",
        {"anno_id": anno_id})
    
        return cursor.fetchall()
    except Exception:
        print "ERROR", "save_conf_file", sys.exc_info()[1]

def save_conf_file(db_name, conf_file, set_id):
    try:
        connection = sqlite3.connect(db_name) 
        cursor = connection.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS files (FileName varchar(80), FileContent blob)")
        query = "insert into files (FileName, FileContent) values (?, ?)"
        f = file(conf_file, 'rb')
        k = f.read()
        f.close()
        
        cursor.execute(query, [set_id, sqlite3.Binary(k)])
        connection.commit()
    except Exception:
        print "ERROR", "save_conf_file", sys.exc_info()[1]
    
def get_conf_file(db_name, set_id):
    try:
        connection = sqlite3.connect(db_name) 
        cursor = connection.cursor()
        cursor.execute("select FileContent from files where FileName=:FileName", {"FileName":set_id}) 
        k = 0 
        config_file = cursor.fetchone()
        return config_file
    except:
        return(None)

def get_max_nmb_elements_per_seq_id(db_name,density_table,set_id,seq_ids):
    try:
        nmb_max=-1
        connection = sqlite3.connect(db_name) 
        cursor = connection.cursor()
        for seq_id in seq_ids:
            cmd="SELECT COUNT(*) FROM "+density_table+" WHERE set_id='"+set_id+"' and seq_id='"+seq_id+"'"
            cursor.execute(cmd)
            nmb=cursor.fetchone()[0]
            if(nmb>nmb_max):
                nmb_max=nmb
        return nmb_max
    except:
        return(None)
    
def find_seq_id(db_name, seq_id):
    try:
        connection = sqlite3.connect(db_name) 
        cursor = connection.cursor()
        cursor.execute("select seq_len from seq_ids where seq_id=:seq_id", {"seq_id":seq_id})
        (seq_len) = cursor.fetchone()
        return seq_len[0]
    except Exception:
        return (None)

def get_min_chromosome_length(db_name, genome_id):
    try:
        connection = sqlite3.connect(db_name) 
        cursor = connection.cursor()
    
        cursor.execute("SELECT DISTINCT min_chromosome_length FROM seq_ids WHERE genome_id='" + genome_id + "'")
        result = cursor.fetchone()
        return result[0]
    
    except Exception:
        return - 1
    
def save_seq_id(db_name, seq_id, seq_len, seq_file, min_chromosome_length, genome_id):
    try:
        connection = sqlite3.connect(db_name) 
        cursor = connection.cursor()
    
        cursor.execute("CREATE TABLE IF NOT EXISTS seq_ids (seq_id varchar(80), seq_len int, seq_file varchar(200), min_chromosome_length int, genome_id varchar(80))")
        connection.commit()
        
        sql = "INSERT INTO seq_ids (seq_id, seq_len,seq_file,min_chromosome_length,genome_id) VALUES (?,?,?,?,?)"
        cursor.execute(sql, (seq_id, seq_len, seq_file, min_chromosome_length, genome_id))
        connection.commit()
    except sqlite3.OperationalError:

        print "ERROR", "save_seq_id", sys.exc_info()[1]

def create_density_table(density_table, db_file):
        try:
            connection = sqlite3.connect(db_file)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS " + density_table + " (name TEXT, seq_lower_coor INTEGER, seq_upper_coor INTEGER, seq_id TEXT, set_id TEXT, elmn_len INTEGER, perc_orig DOUBLE, nmb DOUBLE, nmb_orig INTEGER, perc DOUBLE, N DOUBLE, flag INTEGER)") 
            connection.commit()
        except Exception:
            print "ERROR", "create_density_table", sys.exc_info()[1]

def extract_seq_ids(db_file,anno_table,start,stop,seq_id,set_id):
        try:
            connection = sqlite3.connect(db_file)
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM " + anno_table + " WHERE seq_id='"+seq_id+"' AND seq_lower_coor>="+start+" AND seq_upper_coor<="+stop+" AND anno_id='"+set_id+"'")
            results = cursor.fetchall()
            return results
        except Exception:
            print "ERROR", "extract_seq_ids", sys.exc_info()[1]
        
def findFormerCalculationAndRemove(db_file, density_table, amount_densities_expected, set_id_N, set_id_GC, set_id_A, rerun_gc_n_calculation, seq_id, reCalculate):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
            
        create_density_table(density_table, db_file)
      
        cursor.execute("SELECT COUNT(*) FROM " + density_table + " WHERE set_id=:set_id and seq_id=:seq_id", {"set_id":set_id_N, "seq_id":seq_id})
        amount = cursor.fetchone()[0]
        if(amount != amount_densities_expected):
            rerun_gc_n_calculation = 1
        cursor.execute("SELECT COUNT(*) FROM " + density_table + " WHERE set_id=:set_id and seq_id=:seq_id", {"set_id":set_id_GC, "seq_id":seq_id})
        amount = cursor.fetchone()[0]
        if(amount != amount_densities_expected):
            rerun_gc_n_calculation = 1
        cursor.execute("SELECT COUNT(*) FROM " + density_table + " WHERE set_id=:set_id and seq_id=:seq_id", {"set_id":set_id_A, "seq_id":seq_id})
        amount_A = cursor.fetchone()[0]
        
        if(amount_A == amount_densities_expected):
            while(reCalculate != "y" and reCalculate != "n"):
                print "INFO", "findFormerCalculationAndRemove", "Overwrite existing calculations? (y/n)"
                reCalculate = raw_input(">")
                reCalculate = reCalculate.strip()
                if(reCalculate == "y"):
                    cursor.execute("delete from " + density_table + " where set_id=:set_id  and seq_id=:seq_id", {"set_id":set_id_A, "seq_id":seq_id})
                elif(reCalculate == "n"):
                    return
        
        if(rerun_gc_n_calculation == 1):
            cursor.execute("delete from " + density_table + " where set_id=:set_id and seq_id=:seq_id", {"set_id":set_id_N, "seq_id":seq_id})
            cursor.execute("delete from " + density_table + " where set_id=:set_id and seq_id=:seq_id", {"set_id":set_id_GC, "seq_id":seq_id})
        else:
            pass
        
        connection.commit()
    except Exception:
        print "ERROR", "findFormerCalculationAndRemove", sys.exc_info()[1]
    return rerun_gc_n_calculation, reCalculate


def getMaxNmbFromDatabase(db_file, density_table, set_id):
    max = -1
    
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("select MAX(nmb) from " + density_table + " where set_id=:set_id ", {"set_id":set_id})
        max = cursor.fetchone()
    except Exception:
        print "ERROR", "getValuesFromDatabase", sys.exc_info()[1]
    finally:
        return max

if __name__ == "__main__":
    print "main"
    
#db_file="/nfs/plant/data/repeats/heatmaps_Thomas/ChromoWIZ_problems/barley.db"
#density_table="density_barley"
#set_id="80000_win_16000_shift__ryeSNPmarker4R_hvFlcdna_vs_barley_relative"
#mode="# per Mb" 
#a=getMaxValueFromDatabase(db_file, density_table, set_id, mode)
#print a  

