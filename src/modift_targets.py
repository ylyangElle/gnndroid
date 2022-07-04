import os
import json

raw_path = r"G:\gnn\extract_from_cfg\all_json\malware\train"
dest_path = r"G:\gnn\extract_from_cfg\all_json\malware\train_new"
jsons = os.listdir(raw_path)
for file in jsons:
    file_path = os.path.join(raw_path, file)
    dest_file_path = os.path.join(dest_path, file)
    
    f = open(file_path, "r")
    f_new = open(dest_file_path, "w")
    
    graph_json = json.load(fp=f)
    graph_json["target"] = 1
    json.dump(obj=graph_json, fp=f_new)
    
    f.close()
    f_new.close()
    