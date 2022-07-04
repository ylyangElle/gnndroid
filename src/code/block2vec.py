import os
import opcode_catg
import json

def node2vec(node, opcode):
    vec = [0] * 22
    for catg in opcode:
        if len(opcode) == 16:
            idx = 0
        elif len(opcode) == 6:
            idx = 16
        idx += opcode.index(catg)
        cnt = 0
        if type(catg) == str:
            cnt = node.count(catg)
        elif type(catg) == list:
            for op in catg:
                cnt += node.count(op)
        vec[idx] += cnt
    return vec

def deal_with_nodes_txt(apk_path, nodes_path):
    f = open(nodes_path)

    f_new = open(os.path.join(apk_path, "nodes_new.txt"), "w+")
    lines = f.readlines()

    graph_all_nodes = []
    opcode_bytecode = opcode_catg.opcode_bytecode
    opcode_assembly = opcode_catg.opcode_assembly
    for node in lines:
        node_num = int(node.split(",")[0][1:])
        #if node[0] == "(" and node[-1] == ")\n":
        if "v0" in node or "v1" in node or "v2" in node or "v3" in node or "v4" in node or "v5" in node: #这一行是字节码
            vec = node2vec(node, opcode_bytecode)
        else:
            vec = node2vec(node, opcode_assembly)
        if node_num <= len(graph_all_nodes):
            graph_all_nodes[node_num - 1] = vec
        else:
            graph_all_nodes.append(vec)

    f_new.write(json.dumps(graph_all_nodes))
            
    f_new.close()
    f.close()
