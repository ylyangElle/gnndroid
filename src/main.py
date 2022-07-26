#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import shutil
import argparse

from cfg_java import *
from cfg_so import *

from relations_abstract import RelationAbstract
from graphs_merge import GraphMerging
from nodes_vectorize import GetGMLof2Parts
from store_native_and_java_gmls import StoreGMLsForAPK
    
def process_single_apk(apk, apk_path, tmp_path, graphs_path, good_or_mal):
    
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
        
    if not os.path.exists(graphs_path):
        os.mkdir(graphs_path)
    JAVA_CFG = GenJavaCFG(apk_path, tmp_path)

    so_path = JAVA_CFG.decompile_path
    Native_CFG = GenSOCFG(so_path, tmp_path)

    os.system("ps -ef | grep r2 | awk '{print $2;}' | xargs kill -9")

    gml_path = GetGMLof2Parts(tmp_path).node_vec_path

    relations_abstract = RelationAbstract(tmp_path, gml_path)
    relations_path = relations_abstract.relations_path

    GraphMerging(relations_path, gml_path, graphs_path, apk)
    
    dst_path = os.path.join(r"graphs_to_train", good_or_mal, apk)
    StoreGMLsForAPK(gml_path, dst_path)
    
    if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)

def main(Args):
    # 配置日志文件和日志级别
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    
    logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

    MalDir = Args.maldir
    GoodDir= Args.gooddir
    OutputPath = Args.output_path
    if not os.path.exists(OutputPath):
        os.mkdir(OutputPath)
        
    TmpPath = Args.tmp_path
    #apk_path = r"apks/apks/native_multiple_interactions.apk"
    #apk_path = r"apks/1115.apk"
    
    for dir in [MalDir, GoodDir]:
        for apk in os.listdir(dir):
            apk_path = os.path.join(dir, apk)
            try:
                process_single_apk(apk[:-4], apk_path, \
                    tmp_path=TmpPath, graphs_path=os.path.join(OutputPath, os.path.basename(dir)), good_or_mal = os.path.basename(dir))
            except Exception as e:
                print(e)
                if os.path.exists(TmpPath):
                    shutil.rmtree(TmpPath)
                pass
                

            

    
    
def ParseArgs():
    Args = argparse.ArgumentParser(description="Input APKs and Output GMLs of Android Applications.")
    
    Args.add_argument("--maldir", default="apks/malware", help="Path to directory containing malware apks.")
    Args.add_argument("--gooddir", default="apks/benign", help="Path to directory containing benign apks.")
    #Args.add_argument("--ncpucores", type= int, default= psutil.cpu_count(),help= "Number of CPUs that will be used for processing")
    Args.add_argument("--output_path", default="graphs/", help="Path to directory of output graphs.")
    Args.add_argument("--tmp_path", default="tmp/", help="Path to directory for temperary files.")
    
    return Args.parse_args()

if __name__ == "__main__":
    main(ParseArgs())