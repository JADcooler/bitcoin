from socket import *
import ast
s=socket(AF_INET, SOCK_DGRAM)
s.bind(('',12345))
m=s.recvfrom(1024)
x=m[0].decode()
print(x)

if(x=='transaction'):
	m=s.recvfrom(1024)[0]
	print(m)
	print(type(m))
	trans = ast.literal_eval(m.decode())
	print(type(trans))
	with open('mempool.txt',mode='a+') as file:
		file.write(str(trans)+'\n')

print('contents of mempool.txt')
x=1
with open('mempool.txt') as file:
	for tran in file:
		print(x)
		x+=1
		print(tran,'\n')
#end


