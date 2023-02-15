from socket import *
import ast
import hashlib
s=socket(AF_INET, SOCK_DGRAM)
s.bind(('',12345))

def hash_tr(tr):
        hash_lvl1 = hashlib.sha256(str(tr).encode()).hexdigest()
        double_hash = hashlib.sha256(hash_lvl1.encode()).hexdigest()
        txid = double_hash
        return txid


while(1):

	print('waiting..')
	m=s.recvfrom(1024)
	x=m[0].decode()
	print(x)

	if(x=='transaction'):
		print('	-> processing transaction \'', end ='' )
		m=s.recvfrom(1024)[0]
		h = hash_tr(m.decode())
		print(h,'\'')
		print(m)
		print(type(m))
		trans = ast.literal_eval(m.decode()) #bytes to string
		print(type(trans))
		#with open('mempool.txt',mode='a+') as file:
		#	file.write(str(trans)+'\n')

#END



