


with open('../blocks/block0.txt') as f:
	x = f.read()


UTXOs = {'block0': x}

with open('UTXOs.txt', 'w') as f:
	f.write(str(UTXOs))
print(x)
#END

