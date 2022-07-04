import json
from tqdm import tqdm

path = r"G:\gnn\extract_from_cfg\all_json\train_GGNNinput.json"
fp = open(path)
f = open(r"G:\gnn\extract_from_cfg\all_json\1.txt", "w")
train_data = json.load(fp)
for entry in tqdm(train_data):
    f.write(str(entry))
    print(entry["target"])
    print(type(entry["target"]))
fp.close()
f.close()