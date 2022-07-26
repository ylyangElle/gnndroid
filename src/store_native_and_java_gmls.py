import os, shutil

class StoreGMLsForAPK:
    def __init__(self, gmls_path, dst_path) -> None:
        if not os.path.exists(dst_path):
            shutil.copytree(gmls_path,dst_path)