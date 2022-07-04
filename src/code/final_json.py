import os
import json

benign_path = r"G:\gnn\extract_from_cfg\all_json\json_with_google8-2-feat1\benign\train"
malware_path = r"G:\gnn\extract_from_cfg\all_json\json_with_google8-2-feat1\malware\train"

f_train = open(r"G:\gnn\extract_from_cfg\all_json\json_with_google8-2-feat1\train_GGNNinput.json", "w")
benign_jsons = os.listdir(benign_path)
malware_jsons = os.listdir(malware_path)
graph_list = []
def graph_list_gen(graph_list, jsons, path):
    for file in jsons:
        json_path = os.path.join(path, file)
        f_json = open(json_path)
        graph = json.load(f_json)
        graph_list.append(graph)
        f_json.close()
    return graph_list

graph_list = graph_list_gen(graph_list, benign_jsons, benign_path)
graph_list = graph_list_gen(graph_list, malware_jsons, malware_path)

json.dump(graph_list, f_train)
f_train.close()