with open("output/correct_streams.txt") as f:
    content = f.readlines()

filtered = []
for c in content:
	if "RIGHT" not in c:
		filtered.append(c[6:len(c)-1])
length = 0
for line in filtered:
	length += len(line)
print length/len(filtered)
#print filtered