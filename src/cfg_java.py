import os
import logging
import timeout_decorator


# 配置日志文件和日志级别
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

class GenJavaCFG:
    def __init__(self, apk_path, tmp_path) -> None:
        self.apk_path = apk_path
        self.__apk_num = os.path.basename(self.apk_path)[:-4]
        self.decompile_path = os.path.join(tmp_path, "apk_decompile")
        self.limit_path = os.path.join(tmp_path, "limits")
        self.java_relat = os.path.join(tmp_path, "java")
        if not os.path.exists(self.java_relat):
            os.mkdir(self.java_relat)
        
        self.java_cfg_path = os.path.join(self.java_relat, "java_cfg")
        #dirs = ['apk_decompile', 'limits', 'java_cfg']
        
        self.apk_decompile()
        self.limit_gen()
        self.Gen_Java_CFG()

    def apk_decompile(self):        
            
        if not os.path.exists(self.decompile_path):
            print("正在反编译" + self.__apk_num)
            logging.info("正在反编译" + self.__apk_num)
            cmd = r"java -jar apktool_2.6.0.jar d -f " + self.apk_path + " -o " + self.decompile_path
            os.system(cmd)
        else:
            logging.info("{}反编译已存在".format(self.__apk_num))
            print("{}反编译已存在".format(self.__apk_num))
            
    def __get_apk_package_dir(self, smali_path, f, limit_list):
        subdir = os.listdir(smali_path)
        
        for dir in subdir:
            abs_dir = os.path.join(smali_path, dir)
            if os.path.isdir(abs_dir):
                self.__get_apk_package_dir(abs_dir, f, limit_list)
            else:
                file_path = os.path.split(abs_dir)[0]
                limit_raw = file_path.split("smali")[1].lstrip('/').split('/')[:2]

                concat = "/"
                limit_step1 = concat.join(limit_raw)
                
                if "google" in limit_step1 or "facebook" in limit_step1 \
                        or "amaz" in limit_step1 or "dropbox" in limit_step1 or \
                            "android" in limit_step1 or "tencent" in limit_step1 \
                                or "jaxen" in limit_step1:
                                    continue
                                
                limit_regex = "^L" + limit_step1 + "/.*"
                
                if limit_regex not in limit_list:
                    print(limit_regex)        
                    limit_list.append(limit_regex)
                    f.write(limit_regex + "\n")
  
                return
            
            
    """def __find_androguard_limit_para(self, txt_path, limits_step2_path):

        f = open(txt_path, "r")
        fp = open(limits_step2_path, "w+")
        packages = []
        for line in f.readlines():
            line = line.strip()
            package = line.split(".")
            if len(package) >= 2:
                para_limit = "^L" + package[0] + "/" + package[1] + "/.*"
            else:
                para_limit = "^L" + package[0] + "/.*"
    
            if para_limit not in packages:
                fp.write(para_limit + "\n")
                packages.append(para_limit)

        f.close()
        fp.close()   """    
                     
    def limit_gen(self):
        if not os.path.exists(self.limit_path):
            os.mkdir(self.limit_path)
        
        apk_smali_path = os.path.join(self.decompile_path, "smali")
        limit_step1_txt_path = os.path.join(self.limit_path, "step1.txt")

        if not os.path.exists(apk_smali_path):
            print("{} 没有smali文件夹".format(self.__apk_num))
            logging.error("{} 没有smali文件夹".format(self.__apk_num))
            
        if not os.path.exists(limit_step1_txt_path):
            logging.info("正在提取limit信息-{}".format(self.__apk_num))
            print("正在提取limit信息-{}".format(self.__apk_num))
            
            limit_list = []
            
            with open(limit_step1_txt_path,"w",encoding="utf-8") as f:
                self.__get_apk_package_dir(apk_smali_path, f, limit_list)
            f.close()
            
            #self.__find_androguard_limit_para(limit_step1_txt_path, os.path.join(self.limit_path, 'step2.txt'))
            
            logging.info("{} - limit信息提取完成".format(self.__apk_num))
            print("{} - limit信息提取完成".format(self.__apk_num))
        else:
            logging.info("limit信息已存在-{}".format(self.__apk_num))
            print("limit信息已存在-{}".format(self.__apk_num))

    def __androguard_gen_cfg(self, limit_path, output_path):
        cmd = "androguard decompile -f dot -i " + self.apk_path + " -o " + output_path + " --limit " + limit_path
        os.system(cmd)
        
    def __androguard_gen_fcg(self):
        cmd = "androguard cg " + self.apk_path + " -o " + os.path.join(self.java_relat, "callgraph.gml")
        os.system(cmd)

    @timeout_decorator.timeout(1200)
    def Gen_Java_CFG(self):

        if os.path.exists(self.java_cfg_path):
            logging.info("Java CFGs已存在-{}".format(self.__apk_num))
            print("Java CFGs信息已存在-{}".format(self.__apk_num))
            
            return
        else:
            os.mkdir(self.java_cfg_path)
            limit_path = os.path.join(self.limit_path, "step1.txt")
            
            if os.path.exists(limit_path):
                logging.info("正在生成Java CFGs-{}".format(self.__apk_num))
                print("正在生成Java CFGs-{}".format(self.__apk_num))
                
                limit_file = open(limit_path)
                limits_for_apk = limit_file.readlines()
                i = 0
                for limit in limits_for_apk:
                    print(limit)
                    if "google" in limit or "facebook" in limit or "amaz" in limit or "dropbox" in limit or "android" in limit or "tencent" in limit or "jaxen" in limit:
                        #if_apk_has_google += 1
                        continue
                    else:
                        output_path = os.path.join(self.java_cfg_path, str(i))
                        self.__androguard_gen_cfg(limit, output_path)
                    
                    i += 1
                limit_file.close()
                
                self.__androguard_gen_fcg()
                
                logging.info("已生成Java CFGs-{}".format(self.__apk_num))
                print("已生成Java CFGs-{}".format(self.__apk_num))
                
