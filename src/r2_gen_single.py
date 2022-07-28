from cProfile import label
import os
import r2pipe
import pydot
import time
import signal
import timeout_decorator
import networkx as nx

#@timeout_decorator.timeout(7)
def deal_with_node(addr, func_name, r2, node_num_to_addr, G, r2_path):
    func_cfgs_path = os.path.join(r2_path, "func_cfgs")
    node_num_to_addr[addr] = func_name
    r2.cmd("s " + addr)
    
    G.add_node(func_name)
    if not os.path.exists(func_cfgs_path):
        os.mkdir(func_cfgs_path)
    node_save_to_file = os.path.join(func_cfgs_path, func_name+".dot")

    r2.cmd("pdfd > " + node_save_to_file)
        
def agCd_gen_graph(r2_path, has_func_names, r2, cfg_cur_path):
    node_num_to_addr = {}
    graphs_of_one_dot = pydot.graph_from_dot_file(cfg_cur_path)
    for graph in graphs_of_one_dot:
        G = nx.DiGraph()
        
        nodes = graph.get_nodes()
        edges = graph.get_edges()
        func_names = []

        for node in nodes:
            if node.get('label') in func_names:
                continue
            else:
                func_names.append(node.get('label'))
                
            if "0x0" in node.get_name():
                try:
                    addr = node.get_name().strip("\"")
                    func_name = node.get('label').strip("\"")
                    
                    deal_with_node(addr, func_name, r2, node_num_to_addr, G, r2_path)

                except Exception as e:
                    print(e)
                    continue
        has_func_names += func_names
        
        for edge in edges:
            edge_src_num = node_num_to_addr[edge.get_source().strip("\"")]
            edge_dest_num = node_num_to_addr[edge.get_destination().strip("\"")]
            #line = "(" + edge_src_num + "," + edge_dest_num + ""
            G.add_edge(edge_src_num, edge_dest_num)
            
    return G, has_func_names

def afl_gen_graph(afl_lines, func_names, G, r2):
    node_num_to_addr = {}
    for line in afl_lines:
        l = line.split(" ")
        addr = l[0]
        func_name = l[-1].rstrip("\n")
        if not func_name in func_names:
            
            func_names.append(func_name) 
            deal_with_node(addr, func_name, r2, node_num_to_addr, G, r2_path)
          
    return G
         
r2 = r2pipe.open()
r2.cmd('aaa')

r2_path = FLAGS
cfg_cur_path = os.path.join(r2_path, 'cfg_cur.dot')
afl_cur_path = os.path.join(r2_path, "afl.txt")
if not os.path.exists(r2_path):
    os.mkdir(r2_path)
    
f_dot = open(cfg_cur_path, "w")
f_dot.write(r2.cmd('agCd'))
f_dot.close()

f_dot = open(afl_cur_path, "w")
f_dot.write(r2.cmd('afl'))
f_dot.close()

func_names = []

with open(afl_cur_path, "r") as f_afl:
    afl_lines = f_afl.readlines()
#f_block = open(r"/root/gnn/codes/node_feature_cur.txt", "w")
G, func_names = agCd_gen_graph(r2_path, func_names, r2, cfg_cur_path)
G = afl_gen_graph(afl_lines, func_names, G, r2)

nx.write_gml(G, os.path.join(r2_path, "callgraph.gml"))


r2.cmd("q!!")
r2.quit()
