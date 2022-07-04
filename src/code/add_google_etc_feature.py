import os
import json

exist_json_path = r"G:\gnn\extract_from_cfg\all_json\benign\train"
dest_json_path = r"G:\gnn\extract_from_cfg\all_json\json_with_google8-2-feat1\benign\train"
#f_txt = open(if_has_google_path)
jsons = os.listdir(exist_json_path)
#if_has_google = f_txt.readlines()
all_num = len(jsons)
print(all_num)
rate_of_google = 0.878   #0.234
cnt = 0
for txt in jsons:
    num = txt[:-5]
    f_exist_json = open(os.path.join(exist_json_path, txt), "r")
    f_to_add = open(os.path.join(dest_json_path, txt), "w")
    graph = json.load(f_exist_json)
    nodes = graph["node_features"]
    nodes_new = []
    if cnt <= all_num * rate_of_google:
        for node in nodes:
            nodes_new.append(node + [1])
        cnt += 1
    else:
        for node in nodes:
            nodes_new.append(node + [0])
    graph["node_features"] = nodes_new
    json.dump(graph, f_to_add)
    f_exist_json.close()
    f_to_add.close()

