with open('block0.txt') as f:
	a = f.read()
b = {'block0': a}

with open('blockHeaders.txt','w') as f:
	f.write(str(b))
