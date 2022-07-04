#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import shutil

from cfg_java import *
from cfg_so import *

from relations_abstract import RelationAbstract
from graphs_merge import GraphMerging
from nodes_vectorize import GetGMLof2Parts

# 配置日志文件和日志级别
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

apk_path = r"apks/apks/native_multiple_interactions.apk"
#apk_path = r"apks/1115.apk"
tmp_path = r"./tmp"

if not os.path.exists(tmp_path):
    os.mkdir(tmp_path)
JAVA_CFG = GenJavaCFG(apk_path, tmp_path)

so_path = JAVA_CFG.decompile_path
Native_CFG = GenSOCFG(so_path, tmp_path)

os.system("ps -ef | grep r2 | awk '{print $2;}' | xargs kill -9")

gml_path = GetGMLof2Parts(tmp_path).node_vec_path

relations_abstract = RelationAbstract(tmp_path, gml_path)
relations_path = relations_abstract.relations_path

GraphMerging(relations_path, gml_path)

"""if os.path.exists(tmp_path):
    shutil.rmtree(tmp_path)"""