from cProfile import label
import os
import r2pipe
import pydot
import time
import signal
import timeout_decorator
import networkx as nx

#@timeout_decorator.timeout(7)
def deal_with_node(node, r2, count, node_num_to_addr, G):

    addr = node.get_name().strip("\"")
    
    func_name = node.get('label').strip("\"")
    node_num_to_addr[addr] = func_name
    r2.cmd("s " + addr)
    
    #G.add_node(count, func=func_name)
    G.add_node(func_name)
    if not os.path.exists(r"tmp/r2/func_cfgs"):
        os.mkdir(r"tmp/r2/func_cfgs")
    node_save_to_file = os.path.join(r"tmp/r2/func_cfgs", func_name+".dot")

    r2.cmd("pdfd > " + node_save_to_file)
        

r2 = r2pipe.open()
r2.cmd('aaa')

if not os.path.exists(r"tmp/r2/"):
    os.mkdir(r"tmp/r2/")
    
f_dot = open(r"tmp/r2/cfg_cur.dot", "w")
f_dot.write(r2.cmd('agCd'))
f_dot.close()

f_dot = open(r"tmp/r2/cfg_cur.dot", "r")
#f_block = open(r"/root/gnn/codes/node_feature_cur.txt", "w")
node_num_to_addr = {}
graphs_of_one_dot = pydot.graph_from_dot_file(r"tmp/r2/cfg_cur.dot")

for graph in graphs_of_one_dot:
    G = nx.DiGraph()
    
    nodes = graph.get_nodes()
    edges = graph.get_edges()

    count = 0

    func_names = []

    for node in nodes:
        if node.get('label') in func_names:
            continue
        else:
            func_names.append(node.get('label'))
            
        if "0x0" in node.get_name():
            try:
                node_feature = deal_with_node(node, r2, count, node_num_to_addr, G)
                count += 1
            except Exception as e:
                print(e)
                continue

    for edge in edges:
        edge_src_num = node_num_to_addr[edge.get_source().strip("\"")]
        edge_dest_num = node_num_to_addr[edge.get_destination().strip("\"")]
        #line = "(" + edge_src_num + "," + edge_dest_num + ""
        G.add_edge(edge_src_num, edge_dest_num)
    
    nx.write_gml(G, r"tmp/r2/callgraph.gml")

f_dot.close()

r2.cmd("q!!")
r2.quit()
