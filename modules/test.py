import json
a = {'id': 'adfirgor', 'asdf': 'asdfsd'}
empty = {}
data = {}
dest = 'music_downloader/modules/sec.json'
open(dest,'w')
with open(dest, "w") as f:
    json_pbj = json.dump(a, f)
    f.close()
with open(dest,'r') as f:
    data = json.load(f)
print(data,"Before empty")
with open(dest,'w') as outfile:
    json.dump(empty, outfile)
with open(dest,'r') as f:
    data = json.load(f)
print(data,"After empty")