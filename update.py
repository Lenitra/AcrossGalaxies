import yaml
import os
import datetime



li = os.listdir("data/players")
for e in li:
    with open(f'data/players/{e}', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    player = e.split(".")[0]

    for k, v in data.items():
        if k != "pinf":
            data[int(k)]["shield"] = datetime.datetime.now()



    with open(f'data/players/{e}', 'w', encoding='utf8') as f:
        data = yaml.dump(data, f)