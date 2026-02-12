from pathlib import Path

def merge(file_a,file_b,file_c):
    with open(file_a,'r') as f:
        a = f.readlines()
    with open(file_b,'r') as f:
        b = f.readlines()
    c = "\n".join([x.strip('\n')+y.strip('\n') for x,y in zip(a,b)])
    with open(file_c,'w') as f:
        f.write(c)

folder = Path("data/")
files = [p.name for p in folder.iterdir() if p.is_file()]
# print(files)

mp = {}
for file in files:
    segs = file.split('.')[0].split('_')
    key = segs[0]+'_'+segs[1]
    if key not in mp:
        mp[key] = set()
    if 'std' in segs:
        mp[key].add('std')
    elif 'mer' in segs:
        mp[key].add('mer')
    else:
        mp[key].add('in')

for key,f in mp.items():
    if ('in' in f) and ('std' in f):
        merge(folder / f"{key}.txt",folder / f"{key}_std.txt",folder / f"{key}_mer.txt")