#change line 8
#s.bind(('127.0.1.0',12345))


q = "s.bind(('127.0.1.0',12345))"

with open('ecc/main_f.py') as f:
	a = f.read()

b = a.split('\n')
b[8] = q

a = '\n'.join(b)

with open('ecc/main_f.py','w') as f:
	f.write(a)
