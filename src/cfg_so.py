import logging
import os
import timeout_decorator
import shutil

class GenSOCFG:
    def __init__(self, decompile_path, tmp_path, process_id):
        self.so_path = os.path.join(decompile_path, r"lib/armeabi")
        self.so_cfg_path = os.path.join(tmp_path, "native")
        self.r2_gen_path = "./src/r2_gen_single.py"
        self.r2_tmp = os.path.join(tmp_path, "r2")
        self.process_id = process_id
        self.tmp_path = tmp_path
        
        self.cp_r2_path = os.path.join(tmp_path, "r2_gen_single" + self.process_id + ".py")
        self.copy_r2_path_and_modify()
        self.get_so_cfg_of_apk()
        
        self.__rm_tmp_r2_dir()
    
    def copy_r2_path_and_modify(self):
        shutil.copyfile(self.r2_gen_path, self.cp_r2_path)
#string = 'r\"tmp9561\/r2\"'
        replace_text = 'r\"' + self.tmp_path + '\/r2\"'
        os.system("sed -i 's/{}/{}/g' {}".format("FLAGS", replace_text, self.cp_r2_path))

        
    @timeout_decorator.timeout(15)
    def __r2_cmd(self, so_path):
        os.system("r2 -i " + self.cp_r2_path + " " + so_path)

    def __rm_tmp_r2_dir(self):
        if os.path.exists(self.r2_tmp):
            shutil.rmtree(self.r2_tmp)
        
    def get_cfg_of_one_so(self, so_path):
        #得到只有地址的cfg的dot
        try:
            self.__r2_cmd(so_path)
        except Exception as e:
            print(e)
            return
        
        so_name = os.path.basename(so_path)[:-3]
        #复制到so目录
        so_cfg_path = os.path.join(self.so_cfg_path, so_name + ".dot")
        so_callgraph_gml_path = os.path.join(self.so_cfg_path, so_name + ".gml")
        #os.system("cp tmp/r2/cfg_cur.dot " + so_cfg_path)
        os.system("cp {}/callgraph.gml ".format(self.r2_tmp) + so_callgraph_gml_path)
        
        dest_path = os.path.join(self.so_cfg_path, so_name)
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
        os.system("cp -r {}/func_cfgs/* ".format(self.r2_tmp) + dest_path)

        
        
    def get_so_cfg_of_apk(self):

        if os.path.isdir(self.so_path) and not os.path.exists(self.so_cfg_path):
            os.mkdir(self.so_cfg_path)
            
            all_so_of_one_apk = os.listdir(self.so_path)
            for so in all_so_of_one_apk:
                print(so)
                so_path = os.path.join(self.so_path, so)
                os.rename(so_path, so_path.replace("-", "_"))
                
                so_path = so_path.replace("-", "_")
                if os.path.getsize(so_path) <= 500000:
                    self.get_cfg_of_one_so(so_path)
                    

"""if __name__ == "__main__":
    a = GenSOCFG(r"tmp/apk_decompile", r"tmp")"""
    