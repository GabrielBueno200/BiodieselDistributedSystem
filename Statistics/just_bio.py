import json
from unittest import result
import matplotlib.pyplot as plt

file = open("stats-g.txt", 'r')
file2 = open("stats-w.txt", 'r')
file3 = open("stats-g2.txt", 'r')

all_lines = file.readlines()
all_lines2 = file2.readlines()
all_lines3 = file3.readlines()

results = []
results2 = []
results3 = []
tanks = "biodiesel_tank"
x_time = [i for i in range(0,3600)]

for line in all_lines:
    json_line = json.loads(line)
    #print(json_line)
    #print(json_line['oil_tank']['occupied_capacity'])
    if json_line[tanks]:
        results.append(float(json_line[tanks]['occupied_capacity']))
    else:
        results.append(0.0)

for line in all_lines2:
    json_line = json.loads(line)
    #print(json_line)
    #print(json_line['oil_tank']['occupied_capacity'])
    if json_line[tanks]:
        results2.append(float(json_line[tanks]['occupied_capacity']))
    else:
        results2.append(0.0)


for line in all_lines3:
    json_line = json.loads(line)
    #print(json_line)
    #print(json_line['oil_tank']['occupied_capacity'])
    if json_line[tanks]:
        results3.append(float(json_line[tanks]['occupied_capacity']))
    else:
        results3.append(0.0)

plt.plot(x_time, results, label = f'Max: {results[-1]}')
plt.plot(x_time, results2, label = f'Max: {results2[-1]}')
plt.plot(x_time, results3, label = f'Max: {results3[-1]}')
plt.legend()
plt.title("Produção de Biodiesel")
plt.savefig("biodiesel.png")
plt.show()
