import os
import json
import networkx as nx

class GraphMerging:
    def __init__(self, relations_path, gmls_path, output_path, apk):
        self.relations_j2n_path = os.path.join(relations_path, "j2n.json")
        self.relations_n2j_path = os.path.join(relations_path, "n2j.json")
        self.gmls_path = gmls_path
        #self.graph_final = r"graph_final.gml"
        self.graph_final = os.path.join(output_path, apk+".gml")
        
        if not os.path.exists(self.graph_final):
            self.graph_merging()
    
    #字典中根据值求键的索引
    def __get_key(self, d, value):
        k = [k for k, v in d.items() if v == value]
        return int(k[0])

    #首先将java gml加入到G_final中
    def __merge_java_gml_to_new_gml(self):

        for id in self.G_java.nodes:
            #不涉及调用native部分的节点，可以直接加入G_final中
            if str(id) not in self.relations_j2n.keys():
                self.G_final.add_node(self.G_java.nodes[id]['label'], vec = self.G_java.nodes[id]['vec'])
            else:
                #如果声明了native方法，则将对应lib文件中的native方法的向量添加到当前节点中（直接替换vec）
                target_so_name = list(self.relations_j2n[str(id)].keys())[0]
                G_native = self.G_natives[target_so_name]
                id_native = self.relations_j2n[str(id)][target_so_name]
                
                #self.G_final.add_node(self.G_java.nodes[id]['label'], vec = G_native.nodes[id_native]['vec'])
                self.G_final.add_node(G_native.nodes[id_native]['label'], vec = G_native.nodes[id_native]['vec'])
        #加边
        for edge in self.G_java.edges:

            if str(edge[0]) in self.relations_j2n.keys() and str(edge[1]) in self.relations_j2n.keys():
                target_so_name_0 = list(self.relations_j2n[str(edge[0])].keys())[0]
                G_native_0 = self.G_natives[target_so_name_0]
                id_native_0 = self.relations_j2n[str(edge[0])][target_so_name_0]
                
                target_so_name_1 = list(self.relations_j2n[str(edge[1])].keys())[0]
                G_native_1 = self.G_natives[target_so_name_1]
                id_native_1 = self.relations_j2n[str(edge[1])][target_so_name_1]
                
                src_node = G_native_0.nodes[id_native_0]['label']
                dest_node = G_native_1.nodes[id_native_1]['label']
            
            elif str(edge[0]) in self.relations_j2n.keys() and not str(edge[1]) in self.relations_j2n.keys():
                target_so_name_0 = list(self.relations_j2n[str(edge[0])].keys())[0]
                G_native_0 = self.G_natives[target_so_name_0]
                id_native_0 = self.relations_j2n[str(edge[0])][target_so_name_0]
                
                src_node = G_native_0.nodes[id_native_0]['label']
                dest_node = self.G_java.nodes[edge[1]]['label']
            
            elif str(edge[1]) in self.relations_j2n.keys() and not str(edge[0]) in self.relations_j2n.keys():
                src_node = self.G_java.nodes[edge[0]]['label']
                
                target_so_name_1 = list(self.relations_j2n[str(edge[1])].keys())[0]
                G_native_1 = self.G_natives[target_so_name_1]
                id_native_1 = self.relations_j2n[str(edge[1])][target_so_name_1]
                dest_node = G_native_1.nodes[id_native_1]['label']
            else:
                src_node = self.G_java.nodes[edge[0]]['label']
                dest_node = self.G_java.nodes[edge[1]]['label']

            self.G_final.add_edge(src_node, dest_node, type=0)

    """生成最终的图G_final

        self.__get_relations_j2n() ：
            首先找出将j2n关系中native方法对应的gml图节点编号，为了后续方便融合，改变relations的结构（内容不变），也就是说有两个relations字典
            分别是self.relations_j2n和self.relations_j2n_for_merge
            self.relations_j2n_for_merge = {lib_name:{java_node_id: native_node_id}
            self.relations_j2n = {java_node_id: {lib_name: native_node_id}}
            后续可以优化
            
        self.__merge_java_gml_to_new_gml()：
            将java_gml加入到G_final中
            
        后面一个大循环，是将self.G_natives中的每个native图加入到G_final中，因为在self.__merge_java_gml_to_new_gml()中就已经把调用的native函数
    加入到G_final中了，所以遇到这个函数的节点就直接跳过，native图中的其他节点顺序前移；添加边时要注意区分边的起始和终点是不是与跨语言调用相关的，
    如果是的话，就把不在本native方法内的节点label找出来，加入到G_final中。
        至此，java2native部分的调用全部找完，接下来需要添加native2java的调用边了。
        
    """
    def __java_to_native_merge(self):
        self.__get_relations_n2j()
        
        
        for so_name, G_native in self.G_natives.items():
            if so_name not in self.relations_j2n_for_merge.keys():
                continue
            
            native_target_id = self.relations_j2n_for_merge[so_name]
            
            for id in G_native.nodes:
                if id not in native_target_id.values():
                    self.G_final.add_node(G_native.nodes[id]['label'], vec = G_native.nodes[id]['vec'])
                else:
                    continue
                
            for edge in G_native.edges:
                if edge[0] in native_target_id.values() and edge[1] in native_target_id.values():
                    #这里有点子问题，应该加self.G_java的节点还是self.G_final的？
                    src_node = self.G_java.nodes[self.__get_key(native_target_id, edge[0])]['label']
                    dest_node = self.G_java.nodes[self.__get_key(native_target_id, edge[1])]['label']
                
                elif edge[0] in native_target_id.values() and not edge[1] in native_target_id.values():
                    src_node = self.G_java.nodes[self.__get_key(native_target_id, edge[0])]['label']
                    dest_node = G_native.nodes[edge[1]]['label']
                
                elif edge[1] in native_target_id.values() and not edge[0] in native_target_id.values():
                    src_node = G_native.nodes[edge[0]]['label']
                    dest_node = self.G_java.nodes[self.__get_key(native_target_id, edge[1])]['label']
                else:
                    src_node = G_native.nodes[edge[0]]['label']
                    dest_node = G_native.nodes[edge[1]]['label']
                
                self.G_final.add_edge(src_node, dest_node, type=1)
                
            if so_name in self.relations_n2j.keys():
                for native_caller, java_callees in self.relations_n2j[so_name].items():
                    src_node = native_caller
                    
                    for java_callee in java_callees:
                        node_id, dest_node = self.__get_node_id_from_label("java", java_callee)
                        
                        self.G_final.add_edge(src_node, dest_node, type=2)
                              
                
    def __get_node_id_from_label(self, gml, label):
        
        if "lib" not in gml:
            for id in self.G_java.nodes:
                if label in self.G_java.nodes[id]['label']:
                    return id, self.G_java.nodes[id]['label']
    
        else:
            for id in self.G_natives[gml].nodes:
                if label in self.G_natives[gml].nodes[id]['label']:
                    return id
    
    
    def __get_relations_n2j(self):
        with open(self.relations_n2j_path) as f:
            self.relations_n2j = json.load(f)
        
    def __get_relations_j2n(self):
        """
            读取java2native的json文件，获取java节点对应的native节点编号
        """
        with open(self.relations_j2n_path) as f:
            self.relations_j2n = json.load(f)

        if len(self.relations_j2n.keys()) == 0:
            return False
        
        #print(self.relations_j2n)
                    
        #改变关系的存储方式：
        """self.relations_j2n_for_merge = {lib_name:{
            java_node_id: native_node_id
            }
        }"""
        
        
        self.relations_j2n_for_merge = {}
        for java_node_id in self.relations_j2n.keys():
            lib_name = list(self.relations_j2n[java_node_id].keys())[0]
            native_node_id = self.__get_node_id_from_label(lib_name, \
                self.relations_j2n[java_node_id][lib_name])
            
            if lib_name not in self.relations_j2n_for_merge.keys():
                self.relations_j2n_for_merge[lib_name] = \
                    {java_node_id: native_node_id}
            else:
                self.relations_j2n_for_merge[lib_name][java_node_id] = \
                    native_node_id

                    
        for java_node_id in self.relations_j2n.keys():
            
            lib_name = list(self.relations_j2n[java_node_id].keys())[0]
            native_node_id = self.__get_node_id_from_label(lib_name, \
                self.relations_j2n[java_node_id][lib_name])
            
            self.relations_j2n[java_node_id][lib_name] = native_node_id
        
        return True
            
            
                       
    def __read_Gs_from_files(self):

        """
            读取所有的gml文件中的图，因为lib文件不止一个，所以用一个列表存储
            得到：
                self.G_java
                self.G_natives = {"so_name": G_native}
        """   
        gmls = os.listdir(self.gmls_path)
        self.G_natives = {}
        for index in range(len(gmls)):
            if gmls[index] == "callgraph.gml":
                self.G_java = nx.read_gml(os.path.join(self.gmls_path, gmls[index]), label='id')
            else:
                self.G_natives[gmls[index][:-4]] = nx.read_gml(os.path.join(self.gmls_path, gmls[index]), label='id')

    
    def __delete_zero_vec(self):
        self.G_final_f = nx.DiGraph()
        
        for label in self.G_final.nodes:
            if 'vec' in self.G_final.nodes[label].keys():
                if self.G_final.nodes[label]['vec'] != str([0]*22):
                    self.G_final_f.add_node(label, vec = self.G_final.nodes[label]['vec'])
        
        for edge in self.G_final.edges:

            if edge[0] in self.G_final_f.nodes and edge[1] in self.G_final_f.nodes:
                self.G_final_f.add_edge(edge[0], edge[1], type=self.G_final.edges[edge[0], edge[1]]['type'])
                
    def graph_merging(self):
        self.G_final = nx.DiGraph()
        self.__read_Gs_from_files()
        
        j2n_flag = self.__get_relations_j2n()
        #n2j_flag = self.__get_relations_n2j()
        self.__merge_java_gml_to_new_gml()
        
        if j2n_flag:
            self.__java_to_native_merge()
            
        self.__delete_zero_vec()
        nx.write_gml(self.G_final_f, self.graph_final)

    
if __name__ == "__main__":
    #relations_path, gmls_path, output_path, apk
    GraphMerging(r"tmp/relations", r"tmp/native_and_java_gml_path", r"graphs", "1")