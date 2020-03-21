file = open("JACK6.DAT", "r")
n = int(file.readline())

r = []
p = []

for i in range(n):
    bufor = file.readline()
    space = bufor.split(" ")
    r.append(int(space[0]))
    p.append(int(space[1]))

cMaxN = 0;  #C max naruralne 

for i in range(n):
    cMaxN=max(cMaxN,r[i]) + p[i]

order = sorted(range(n),key = r.__getitem__)

print(order)
cMaxO = 0

for l in range(n):
    k = order[l]
    cMaxO=max(cMaxO,r[k]) + p[k]

print(cMaxO)
print(r)
print(p)
print(n)
file.close()