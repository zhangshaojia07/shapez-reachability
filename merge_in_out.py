from pathlib import Path

def diff(file_out,content):
    count = 0
    for i in range(len(content)-1):
        sub = content[i:i+2]
        if sub == 'yn' or sub == 'ny':
            count += 1
            line_id = content[:i].count('\n') + 1
            print(f"{file_out} @ {line_id} : {sub}")
            if count >= 3:
                break
    if count == 0:
        print(f"passed {file_out}")

def merge(file_out,*args):
    content = []
    for file_in in args:
        with open(file_in,'r') as f:
            content.append(f.readlines())
    content = "\n".join(["".join(j.strip('\n') for j in i) for i in zip(*content)])
    diff(file_out,content)
    with open(file_out,'w') as f:
        f.write(content)

folder = Path("data/")
folder2 = Path("output/")
files = [p.name for fl in [folder,folder2] for p in fl.iterdir() if p.is_file()] 
# print(files)

mp = {}
for file in files:
    segs = file.split('.')[0].split('_')
    # if int(segs[1])>=6:
    #     continue
    key = segs[0]+'_'+segs[1]
    if key not in mp:
        mp[key] = set()
    if 'std' in segs:
        mp[key].add('std')
    elif 'mer' in segs:
        mp[key].add('mer')
    elif 'my' in segs:
        mp[key].add('my')
    else:
        mp[key].add('in')

for key,f in mp.items():
    cand = []
    count = 0
    if ('in' in f):
        cand.append(folder / f"{key}.txt")
        count += 1
    if ('std' in f):
        cand.append(folder / f"{key}_std.txt")
        count += 1
    if ('my' in f):
        cand.append(folder2 / f"{key}_my.txt")
        count += 1
    if count != 3:
        continue 
    merge(
        folder2 / f"{key}_mer.txt",
        *cand
        )