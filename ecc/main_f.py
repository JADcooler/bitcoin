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

def deleteUTXO(tr, blockReceived):
	file = 'UTXO/UTXOs.txt'
	if(blockReceived == False):
		file = 'UTXO/UTXO.tmp'

	with open(file, 'r') as f:
		UTXO = f.read()
	UTXO = ast.literal_eval(UTXO) #get dict of blocks
	for block in UTXO: #Iterate over all blocks
		txs = UTXO[block]
		txs = ast.literal_eval(txs) #get dict of tx in block
		try:
			print('before',txs) 
			del txs[tr]

		except KeyError:
			print('transaction wasn\'t found'+str(block))
			continue
		print('after',txs)
		UTXO[block] = str(txs) #to str of tx
		with open(file, 'w') as f:
			f.write(str(UTXO)) #to str of blocks


ip = input('tr ')
deleteUTXO(ip, False)


while(1):

	print('waiting..')
	m=s.recvfrom(1024)
	x=m[0].decode()
	print(x)

	if(x=='transaction'): #Start strings
		m=s.recvfrom(1024)[0]
		txid = hash_tr(m.decode())

		print('	-> processing transaction \'', end ='' )
		print(txid,'\'') #print txid


		print(m)
		print("\n\n\n")

		with open('mempool.txt', 'r') as f:
			x = f.read()

		mempool = ast.literal_eval(x)

		print("MEMPOOL IS ", mempool)

		mempool[txid] = m.decode()

		with open('mempool.txt', 'w') as f:
			f.write(str(mempool))


		#with open('mempool.txt',mode='a+') as file:
		#	file.write(str(trans)+'\n')

#END



