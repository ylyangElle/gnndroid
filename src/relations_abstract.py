from asyncio.log import logger
from cProfile import label
import logging
import os
"""from relations_abstract_j2n import RelationsAbstract_J2N
from relations_abstract_n2j import RelationsAbstract_N2J"""

class RelationAbstract:
    def __init__(self, tmp_path, gml_path):
        self.tmp_path = tmp_path

        self.relations_path = os.path.join(tmp_path, "relations")
        self.gml_path = gml_path
        if not os.path.exists(self.relations_path):
            os.mkdir(self.relations_path)
        self.relations_n2j_path = os.path.join(self.relations_path, "n2j.json")
        self.relations_j2n_path = os.path.join(self.relations_path, "j2n.json")
  
        self.__init_j2n()
        self.__init_n2j()
       
    def __init_j2n(self):
        RelationsAbstract_J2N(self.tmp_path, self.relations_j2n_path, self.gml_path)
    def __init_n2j(self):
        RelationsAbstract_N2J(self.tmp_path, self.relations_n2j_path)
        
        
        
import os
import networkx as nx
import re
import json

class RelationsAbstract_J2N:
    def __init__(self, tmp_path, relations_j2n_path, gml_path):
        self.tmp_path = tmp_path
        self.relations_j2n_path = relations_j2n_path
        self.fcg = os.path.join(self.tmp_path, r"java/callgraph.gml")
        self.cfg = os.path.join(self.tmp_path, r"java/java_cfg")
        #self.relations = os.path.join(tmp_path, "relations")
        self.relation_j2n = {}
        self.gml_path = gml_path

        self.analysis_java_to_native()
        self.__store_j2n_relations_as_json()

    
    def __store_j2n_relations_as_json(self):
        for java_func_id in self.id_native_func.keys():
             self.relation_j2n[java_func_id] = {}
             
             for so_name in self.native_so_name.keys():
                 for native_func_name in self.native_so_name[so_name]:
                     if native_func_name == self.id_native_func[java_func_id]:
                         self.relation_j2n[java_func_id][so_name] = native_func_name
               
        with open(self.relations_j2n_path, "w", encoding='utf-8') as f:
            json.dump(self.relation_j2n, f)
                 
    def __get_java_name_and_native_func_name(self, label):
        #"Lorg/arguslab/native_multiple_interactions/MainActivity;->propagateImei(Lorg/arguslab/native_multiple_interactions/Data;)V [access_flags=public native] @ 0x0"
        if ";->" in label:
            label_split = label.split(";->")
        elif "->" in label:
            label_split = label.split("->")
        package_name = label_split[0].lstrip("L")
        native_func_name = label_split[1].split(" [access_flags")[0]

        return package_name, native_func_name
    
    def __get_gmls(self, so_name):
        with open(os.path.join(self.gml_path, so_name+".gml")) as f:
            return nx.read_gml(f)
        
    #生成可以传递去native部分的内容 主要是so名，及其中的函数名
    def __get_native_so_name(self): #to_native的最重要的一步！！
        self.native_so_name = {} #{so_name:[native_func_name_1, native_func_name_2]}
        
        regex = re.compile("const-string v0, (.*)")
        for smali_file in self.record_lib_id:
            with open(smali_file) as f:
                lines = f.readlines()
                
                flag = 0
                for line in lines:
                    if ".method static constructor <clinit>()V" in line:
                        flag = 1
                    elif ".end method" in line:
                        flag = 0
                    lib_name = regex.findall(line)
                    if flag == 1 and len(lib_name) != 0:
                        #lib_name = "lib" + lib_name[0].strip("\"") + ".so"
                        lib_name = "lib" + lib_name[0].strip("\"")
                        self.native_so_name[lib_name] = []
                        
                        #G_native = self.__get_gmls(lib_name)
                        G_native = nx.read_gml(os.path.join(self.gml_path, lib_name+".gml"))
                    
                        for id in self.record_lib_id[smali_file]:
                            for node in G_native.nodes:
                                if self.id_native_func[id] in node:
                                    self.native_so_name[lib_name].append(self.id_native_func[id])
                        
                
    def analysis_java_to_native(self):
        #读取callgraph.gml,提取native func name以及声明该函数的类(找对应的smali文件以提取对应的so库名)
        #输出：self.id_native_func = {id:jni_func_name},其中id指java fcg中声明该函数的节点（可以直接替换）
        #     self.native_so_name = {so_name:[native_func_name_1, native_func_name_2]}
        
        G_java = nx.read_gml(self.fcg, label="id")
        regex = re.compile("access_flags=.*native.*]")
        #with open(os.path.join(self.relations, "toNative.json"), "w")as f:
        
        self.id_native_func = {} #{id:jni_func_name}
        self.record_lib_id = {} #{smali_name:[native_func_id_1, native_func_id_2]}
        for id in G_java.nodes:
            if regex.findall(G_java.nodes[id]['label']):
                package_name, native_func_name = self.__get_java_name_and_native_func_name(G_java.nodes[id]['label'])
                smali_path = os.path.join(os.path.join(self.tmp_path, r"apk_decompile/smali"), package_name + ".smali")
                #self.__find_native_lib(smali_path)
                #可能存在多个native函数在一个so文件的情况，所以用字典存储要找的smali文件位置
                if smali_path not in self.record_lib_id.keys():
                    self.record_lib_id[smali_path] = [id]
                else:
                    self.record_lib_id[smali_path].append(id)
                    
                jni_func_name = "Java_" + package_name.replace("_", "_1").replace("/", "_") + "_" + native_func_name.split("(")[0]
                self.id_native_func[id] = jni_func_name
        
        self.__get_native_so_name()

import os
import re
import json

class RelationsAbstract_N2J:
    def __init__(self, tmp_path, relations_n2j_path):
        self.tmp_path = tmp_path
        self.relations_n2j_path = relations_n2j_path
        
        self.native_cfg_path = os.path.join(self.tmp_path, "native")
        self.java_class_regex = re.compile('"([A-Za-z0-9_\/]+)"')
        self.relations_n2j = {}
        
        self.__traverse_all_so()
        self.__store_n2j_relations_as_json()

    def __store_n2j_relations_as_json(self):
        with open(self.relations_n2j_path,'w',encoding='utf-8') as fp:
            json.dump(self.relations_n2j, fp)
        
    def __get_n2j_relations(self, so_name, native_func_name):
        self.relations_n2j[so_name] = {}
        self.relations_n2j[so_name][native_func_name] = []
        #class_name + "->" + func_name for func_name in self.java_class_func[class_name] for class_name in self.java_class_func.keys()
        for class_name in self.java_class_func.keys():
            for func_name in self.java_class_func[class_name]:
                self.relations_n2j[so_name][native_func_name].append("L" + class_name + ";->" + func_name)
    
    #分析每个函数文件，解析其中的java func
    def __func_content_analysis(self, dot_path, so_name):
        
        func_name = os.path.basename(dot_path)[:-4]
        with open(dot_path) as f:
            lines = f.readlines()
        
        self.java_func_para = re.compile('"(\([A-Za-z0-9_\/;]+\)[BCDFJISVZ[])"')
        
        flag = 0
        self.java_class_func = {}
        java_func_name = ""
        
        for line in lines:
            java_class_or_func_name = self.java_class_regex.findall(line)
            java_func_para = self.java_func_para.findall(line)
            
            if "/" in line and len(java_class_or_func_name) != 0:
                flag = 1
                java_class_name = java_class_or_func_name[0]
                self.java_class_func[java_class_name] = [] #每个so文件中可能调用了同一个java类中的多个函数
                
            if flag == 1:               
                if len(java_class_or_func_name) != 0 and "/" not in line:
                #java_class_func[java_class_name[0]].append(java_class_name[0])
                    java_func_name += java_class_or_func_name[0]

                elif len(java_func_para) != 0:
                    java_func_name += java_func_para[0]
                    self.java_class_func[java_class_name].append(java_func_name)
                
            else:
                flag = 0
                java_func_name = ""
                
        if len(self.java_class_func) != 0:
            self.__get_n2j_relations(so_name, func_name)
    
    #对于每一个so文件，遍历其每个函数文件
    def __analyze_every_so_file(self, so_name):
        so_func_content_path = os.path.join(self.native_cfg_path, so_name)
        
        func_contents = os.listdir(so_func_content_path)
        for func_content in func_contents:
            self.__func_content_analysis(os.path.join(so_func_content_path, func_content), so_name)
    
    #遍历so_cfg中的每个文件夹（每个so文件中函数的内容），
    def __traverse_all_so(self):
        files = os.listdir(self.native_cfg_path)
        for so_name in files:
            if os.path.isdir(os.path.join(self.native_cfg_path, so_name)):
                self.__analyze_every_so_file(so_name)
        
"""if __name__ == "__main__":
    RelationAbstract(r"tmp")"""
    
    
