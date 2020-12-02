
file = open('alpha_star_names.htm', 'rb')

for i in range(58):
	file.readline()

tableData = ''
tr = file.readline().strip()
while tr.find('</tbody>') == -1:
	tableData += tr
	tr = file.readline().strip()

stars = []
start = 0
end = tableData.find('</tr>', start)
#for i in range(6):
while end != -1:
	row = tableData[start + 4:end]
	data = []
	tdStart = 0
	tdEnd = row.find('</td>', tdStart)
	tds = []
	while tdEnd != -1:
		td = row[tdStart + 4:tdEnd]
		tds.append(td)
		tdStart = tdEnd + 5
		tdEnd = row.find('</td>', tdStart)

	name = tds[3]

	# I don't understand why, but the strings are coming back separated by chr(160) ( accented 'a')
	names = name.split(chr(160))
	name = ''
	for i in range(len(names)):
		sub = names[i]
		names[i] = sub[0].upper() + sub[1:].lower()
	name = ' '.join(names)

	magnitude = tds[8]

	star = ( name, magnitude )
	stars.append(star)

	start = end + 5
	end = tableData.find('</tr>', start)

file.close()

file = open('starNames.xml', 'w')
print >> file, '<stars>'
for name, mag in stars:
	print >> file, "\t<star><name>%s</name><mag>%s</mag></star>" % ( name, mag )
print >> file, '</stars>'
file.close()
