from operator import index
import os
import networkx as nx
from numpy import dot
from opcode_catg import opcode_bytecode
from opcode_catg import opcode_assembly
import re

class NodeVectorize: #记得判别native 和 java
    """把每个func文件的内容根据指令分类统计量，得到对应的向量，加入各自的gml文件中
        最终获得两个gml文件：native.gml,java.gml
    """
    def __init__(self, tmp, gml_of_2_parts_path, native_or_java):
        self.tmp_path = tmp
        self.node_vec_path = gml_of_2_parts_path
        self.native_or_java = native_or_java
        
        #self.dest_gml_path = os.path.join(self.node_vec_path, native_or_java + "_fcg.gml")
        
        self.__read_gml()
        
    def __node2vec(self, node, opcode):
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
    
    def __node_vec(self, f):
        dot_content = f.read(-1)
        if self.native_or_java == "java":
            vec = self.__node2vec(dot_content, opcode_bytecode)
        elif self.native_or_java == "native":
            vec = self.__node2vec(dot_content, opcode_assembly)
        return vec
    
    """def __get_func_name_for_concat_path(self, func_name):
        print(func_name)
        #toNative(Lorg/arguslab/native_multiple_interactions/Data; Ljava/lang/String;)V -> toNative (Data String)V
        
        func_name = func_name.replace("<", "_").replace(">", "_")
        
        regex = re.compile("\(\)")"""
        
        
    def __get_java_package_and_func_name(self, label):
        #"Lorg/arguslab/native_multiple_interactions/MainActivity;->propagateImei(Lorg/arguslab/native_multiple_interactions/Data;)V [access_flags=public native] @ 0x0"
        label_split = label.split(";->")
        package_name = label_split[0].lstrip("L")
        java_func_name = label_split[1].split("(")[0].replace("<", "_").replace(">", "_")

        return package_name, java_func_name
    
    def __read_limits_to_get_package_num(self):
        with open(os.path.join(self.tmp_path, r"limits/step1.txt")) as f:
            self.limits = [i.lstrip("^L").rstrip("/.*\n") for i in f.readlines()]
    
    def __get_node_content_for_java(self, package_name, java_func_name):
        """根据包名、函数名以及limit对应的位置找到函数ag文件的位置，这里缺少一种情况：如果包只有一级目录，可能会出错"""

        self.__read_limits_to_get_package_num()
        if "/" in package_name:
            regex = re.compile("[a-zA-z0-9]+\/[a-zA-z0-9]+")
        else:
            regex = re.compile("[a-zA-z0-9]+")
        try:
            index = self.limits.index(regex.findall(package_name)[0])
        except Exception:
            return False
        
        package_path = os.path.join(self.cfgs_path, "java_cfg", str(index), package_name)
        func_ag_names = os.listdir(package_path)
        
        for file_name in func_ag_names:
            if java_func_name in file_name:
                java_func_name = file_name
                
        dot_path = os.path.join(self.cfgs_path, "java_cfg", str(index), package_name, java_func_name)
        
        if not os.path.exists(dot_path):
            return False
        
        with open(dot_path) as f:
            return self.__node_vec(f)
        
        
        
    def __get_node_content(self, func_name):
        if self.native_or_java == "native":
            so_path = self.cg_gml_path[:-4]

            func_path = os.path.join(so_path, func_name + ".dot")
            
            with open(func_path) as f:
                func_vec = self.__node_vec(f)
            return func_vec
        
        else:
            package_name, java_func_name = self.__get_java_package_and_func_name(func_name)
            #print(package_name)
            #从limit文件中读取当前package的编号，找目录
            func_vec = self.__get_node_content_for_java(package_name, java_func_name)
            if func_vec:
                return func_vec
            else:
                return str([0] *22)
            
    
    def __read_gml(self):
        self.cfgs_path = os.path.join(self.tmp_path, self.native_or_java)  #tmp/java
        
        for subdir in os.listdir(self.cfgs_path):
            self.G_new = nx.DiGraph()
            self.cg_gml_path = os.path.join(self.cfgs_path, subdir)

            if not os.path.isdir(self.cg_gml_path):

                G = nx.read_gml(self.cg_gml_path, label="id")

                """for id in G.nodes:
                    node_vec = self.__get_node_content(G.nodes[id]['label'])
                    if node_vec != str([0]*22):
                        self.G_new.add_node(G.nodes[id]['label'], vec=str(node_vec))
                
                G_nodes = list(self.G_new.nodes)
                #G_new.add_edges_from(G.edges, type=0)
                for edge in G.edges:
                    src_node = G.nodes[edge[0]]['label']
                    dest_node = G.nodes[edge[1]]['label']
                    if src_node in G_nodes and dest_node in G_nodes:
                        self.G_new.add_edge(src_node, dest_node)"""
                
                
                for id in G.nodes:
                    node_vec = self.__get_node_content(G.nodes[id]['label'])
                    self.G_new.add_node(G.nodes[id]['label'], vec=str(node_vec))
                
                #G_new.add_edges_from(G.edges, type=0)
                for edge in G.edges:
                    src_node = G.nodes[edge[0]]['label']
                    dest_node = G.nodes[edge[1]]['label']
                    
                    self.G_new.add_edge(src_node, dest_node)
                    
                self.dest_gml_path = os.path.join(self.node_vec_path, subdir)
                nx.write_gml(self.G_new, self.dest_gml_path)
                    

class GetGMLof2Parts:
    def __init__(self, tmp):
        self.node_vec_path = os.path.join(tmp, "native_and_java_gml_path")
        if not os.path.exists(self.node_vec_path):
            os.mkdir(self.node_vec_path)
            
        NodeVectorize(tmp, self.node_vec_path, "java")
        NodeVectorize(tmp, self.node_vec_path, "native")
        
"""if __name__ == "__main__":
    GetGMLof2Parts(r"tmp")
"""