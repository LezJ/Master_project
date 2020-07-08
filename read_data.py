TS = [[],[],[]]
FS = [[],[],[]]
PS = [[],[],[],[]]

f = open('D:\Py\Vrep\Data\data.txt', 'r')

for line in f:
    if 'Grasp' in line:
        g = int(line[6]) - 1
        for i in range(3):
            TS[i].append([])
            FS[i].append([])
            PS[i].append([])
        PS[3].append([])
    else:
        num = int(line[2])
        content = line[4:]
        if 'TS' in line:
            TS[num][g].append(list(eval(content)))
        if 'FS' in line:
            FS[num][g].append(list(eval(content)))
        if 'PS' in line:
            PS[num][g].append(list(eval(content)))
            
f.close()