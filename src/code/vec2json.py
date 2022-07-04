import os
import json

raw_path = r"G:\gnn\extract_from_cfg\malware"
dest_path = r"G:\gnn\extract_from_cfg\all_json\malware"
apk_num_list = os.listdir(raw_path)

for apk_num in apk_num_list:
    print(apk_num)
    apk_path = os.path.join(raw_path, apk_num)
    graph_path = os.path.join(dest_path, apk_num + ".json")
    if not os.path.exists(graph_path):
        f_nodes = open(os.path.join(apk_path, "nodes_new.txt"))
        f_edges = open(os.path.join(apk_path, "edges.txt"))
        f_graphs = open(graph_path, "w")
        
        nodes = json.load(f_nodes)
        edges = f_edges.readlines()
        
        edges_json = []
        for edge in edges:
            if edge[0] == "(" and edge[-2:] == ")\n":
                edge = str(edge.strip("\n"))
                edge = tuple(eval(edge))
                if int(edge[0]) >= len(nodes) or int(edge[1]) >= len(nodes):
                    continue
                else:
                    edges_json.append(edge)
        """{
        'node_features': <A list of features representing every nodes in the graph>,
        'graph': <A list of edges>
        'target': <0 or 1 representing the vulnerability>
        }"""
        graph_json = {}
        graph_json['node_features'] = nodes
        graph_json['graph'] = edges_json
        graph_json['target'] = 1
        
        json.dump(obj=graph_json, fp=f_graphs)
        f_graphs.close()
        f_nodes.close()
        f_edges.close()