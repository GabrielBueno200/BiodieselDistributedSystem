import json
import matplotlib.pyplot as plt
from itertools import cycle

file = open("stats-g.txt", 'r')

all_lines = file.readlines()

results = [[] for _ in range(0,12)]
tanks = []
x_time = [i for i in range(0,3600)]

#get tank names
for line in all_lines:
    json_line = json.loads(line)
    for tank in json_line:
        tanks.append(tank)
        #results.append()
    break

# get values
for line in all_lines:
    json_line = json.loads(line)
    #print(json_line)
    #print(json_line['oil_tank']['occupied_capacity'])
    it = 0
    for tank in json_line:
        if json_line[tank]:
            results[it].append(float(json_line[tank]['occupied_capacity']))
        else:
            results[it].append(0.0)
        it+=1

lstyle = ["-","--","-.",":"]
linecycler = cycle(lstyle)

for i in range(12):
    plt.plot(x_time, results[i], label = tanks[i], linestyle=next(linecycler))

plt.legend()
plt.savefig("allresults.png")
plt.show()