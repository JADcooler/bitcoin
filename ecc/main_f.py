from socket import *
import ast
import hashlib
from ecdsa import BadSignatureError, VerifyingKey

s=socket(AF_INET, SOCK_DGRAM)
s.bind(('',12345))

def hash_tr(tr):
        hash_lvl1 = hashlib.sha256(str(tr).encode()).hexdigest()
        double_hash = hashlib.sha256(hash_lvl1.encode()).hexdigest()
        txid = double_hash
        return txid

def verifySignature(tr):
	print('splitting inputs')
	flag = 1
	for inp in tr['inputs']:
		prev_tran = inp['prev_tran']
		output_index = inp['output_index']
		sigScr = inp['sigScr']

		textToGet = prev_tran + str(output_index)

		pubkey = sigScr['publicKey']
		signature = sigScr['signature']

		dPub = VerifyingKey.from_string(pubkey.encode('ISO-8859-1'))
		dSig = signature.encode('ISO-8859-1')

		x = dPub.verify(dSig, textToGet.encode('ISO-8859-1'))
		print("\t\tTHE RESULT IS ",x)
		if(x == False):
			flag=0

	print("THIS SAYS THE PERSON WHO GAVE THE SIGNATURE WITH PUBLIC KEY, HAD ACTUALLY", "USED HIS PRIVATE KEY TO ENCRYPT PREV_TXID AND OUTPUT INDEX")
	print("THIS IS USED SUCH THAT ONLY THE PERSON IN POSSESSION OF THE PRIVATE KEY", "FOR THAT PUBLIC KEY CAN USE HIS FUNDS")
	print("---------------------------------------------------------------------------------")
	print("THE REST WE HAVE TO DO IS VERIFY THAT THE INPUT REFERENCED EXISTS IN UTXO SET", 	"AND IS PAID TO TO HIM AND NOT OTHERS")

	return flag




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
			del txs[hash_tr(tr)]

		except KeyError:
			print('transaction wasn\'t found'+str(block))
			continue
		print('after',txs)
		UTXO[block] = str(txs) #to str of tx
		with open(file, 'w') as f:
			f.write(str(UTXO)) #to str of blocks

	print("DELETED INPUT")

def validateAsUTXO(tr):
	file = 'UTXO/UTXO.tmp'
	#For a transaction to be validated, all its inputs must
	#exist either in a block or in the mempool.

	a = verifySignature(tr)
	if(a==False):
		print("INVALID SIGNATURE")
		return False

	txid = hash_tr(tr)

	file = 'UTXO/UTXO.tmp'

	with open(file, 'r') as f:
		UTXO = f.read()
	UTXO = ast.literal_eval(UTXO) #get dict of blocks

	inputTxids = [ i['prev_tran'] for i in tr['inputs'] ]


	print("Input prev_trans ", inputTxids)
	#approach to combine all transactions with o/p in UTXO and check if
	#set prev tran is subset of all txids in UTXO
	allTxids = {}
	#TODO append output no in tnxs and compare 
	for block in UTXO:
		tnxs = ast.literal_eval(UTXO[block])
		for tnx in tnxs:
			allTxids[tnx] = tnxs[tnx]

	print("all txids in UTXO ")

	for i in allTxids:
		print(i)

	print('all prev trans')
	for i in inputTxids:
		print(i)

	bool = set(inputTxids.keys()).issubset(set(allTxids.keys()))
	print("they are equal? ",bool)

	#then check if the prev tran existing in UTXO sets
	#has output to the current tx owners public key

	'''
	for block in UTXO: #Iterate over all blocks
		txs = UTXO[block]
		txs = ast.literal_eval(txs) #get dict of tx in block
		txids = txs.keys()

		print('searching ',inputTxids, ' in ',txids)

		flag = 0
		for i in inputTxids:
			if i in txids:
				inputTxids.remove(i)
				flag = 1
		#the above approach is wrong as each prev_tran
		#can be duplicated while output no changes

		#an approach where we account output no TODO
		if(not flag):
			print("not found in ",block)
		print(inputTxids)

	return not len(inputTxids)
	'''
while(1):

	print('waiting..')
	m=s.recvfrom(1024)
	x=m[0].decode()
	print(x)

	if(x=='transaction'): #Start strings
		m=s.recvfrom(2048)[0] #hope 2048 is ok..
		txid = hash_tr(m.decode())

		print('	-> processing transaction \'', end ='' )
		print(txid,'\'') #print txid


		print(m)
		print("\n\n\n")

		tr = ast.literal_eval(m.decode())


		verifySignature(tr)
		#TODO del inputs from UTXO set / UTXO.tmp

		with open('mempool.txt', 'r') as f:
			x = f.read()

		mempool = ast.literal_eval(x)

		#print("MEMPOOL IS ", mempool)

		mempool[txid] = m.decode()

		if(validateAsUTXO(tr) == False):
			print("INVALID TRANSACTION, REJECTED")
			continue

		with open('mempool.txt', 'w') as f:
			f.write(str(mempool))
		print('WRITTEN IN MEMPOOL')


		#with open('mempool.txt',mode='a+') as file:
		#	file.write(str(trans)+'\n')

#END


