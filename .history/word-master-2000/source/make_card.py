import sys

filename = sys.argv[1]

lines = open(filename, 'r').readlines()
items = []
item = []
for line in lines:
	line = line.strip()
	if line.isnumeric():
		if len(item):
			items.append(item)
		item = [int(line)]
	else:
		item.append(line)

items = sorted(items, key=lambda item: item[0])

out = """
q | a 
--|--
"""
for item in items:
        out += f"{item[1]}\t\t| {item[2]}\n"

print(out)
name, ext = filename.split('.')
filename_md = f"../{name}.{items[0][1]}-{items[-1][1]}.md"
f_md = open(filename_md, 'w')
f_md.write(out)
f_md.close()
