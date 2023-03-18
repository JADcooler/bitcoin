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
	print('splitting inputs of txid',hash_tr(tr))

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

def deleteTxOutputs(txid, on):
	file = 'UTXO/UTXO.tmp'
	#by giving a txn, we remove an output from it as UTXO

	print("DELETING ",txid, " OUTPUT ", on)

	with open(file, 'r') as f:
		blocks = ast.literal_eval(f.read())

	blockF = ''
	for block in blocks:
		txns = blocks[block]
		txns = ast.literal_eval(txns)
		if( txid in txns):
			blockF = block
			break
	if(blockF == ''):
		print("NO BLOCK HAS REQUIRED TX")
		return

	txns = ast.literal_eval(blocks[blockF])
	txn = ast.literal_eval(txns[txid])

	toPop = -1
	outputs = txn['outputs']
	for i in range(len(outputs)):
		if(outputs[i]['output_no']==on):
			toPop = i
			break
	if(toPop == -1):
		print("TXN DOES NOT HAVE REQUIRED OUTPUT INDEX")

	#we are now about to modify txns string in block dict


	modifyThis = blocks[blockF] #later used as l value
	modifyTxns = ast.literal_eval(modifyThis) #later as l value
	modifyTxn =ast.literal_eval( modifyTxns[txid]) #later uesd as l value


	modifyTxn['outputs'].pop(toPop)

	modifyTxns[txid] = str(modifyTxn)
	blocks[blockF] = str(modifyTxns)

	with open(file, 'w') as f:
		f.write(str(blocks))

	print("SUCCESFULLY REMOVED OUTPUT",on," FROM",txid)



def validateAsUTXO(tr):
	file = 'UTXO/UTXO.tmp'
	#For a transaction to be validated, all its inputs must
	#exist either in a block or in the mempool.

	pk = tr['inputs'][0]['sigScr']['publicKey']



	a = verifySignature(tr)
	if(a==False):
		print("INVALID SIGNATURE")
		return False

	txid = hash_tr(tr)

	file = 'UTXO/UTXO.tmp'

	with open(file, 'r') as f:
		UTXO = f.read()
	UTXO = ast.literal_eval(UTXO) #get dict of blocks


	#checking if all inputs reference the public key of tx maker
	print("	\#checking if all inputs reference the public key of tx maker")

	inputx = [ i['prev_tran'] for i in tr['inputs'] ]
	inputOn = [ i['output_index'] for i in tr['inputs'] ]
	inputT = {}

	for block in UTXO:
		txns = ast.literal_eval(UTXO[block])
		for i in inputx:
			if i in txns:
				inputT[i] = ast.literal_eval(txns[i])


	inputTxids = [ i['prev_tran']+ str(i['output_index'])   for i in tr['inputs'] ]


	print("Input prev_trans ", inputTxids)
	#approach to combine all transactions with o/p in UTXO and check if
	#set prev tran is subset of all txids in UTXO
	allTxids = {}
	for block in UTXO: #UTXO is of format { 'blockno': str(txns) }
		tnxs = ast.literal_eval(UTXO[block])
		for tnx in tnxs: #tnxs is of format { 'txid' : str(tx data) }
			x = tnxs[tnx]
			x = ast.literal_eval(x)
			for output in x['outputs']:
				allTxids[tnx + str(output['output_no'])] = x['outputs']

	print("all txids in UTXO ")

	for i in allTxids:
		print(i)

	print('all prev trans')
	for i in inputTxids:
		print(i)

	bool = set(inputTxids).issubset(set(allTxids.keys()))
	print("they are equal? ",bool)

	return [ (i['prev_tran'], i['output_index']) for i in tr['inputs'] ]


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


		params = validateAsUTXO(tr)
		print("params are ",params)

		#TODO del inputs from UTXO set / UTXO.tmp

		for i in params:
			deleteTxOutputs(i[0], i[1])


		with open('mempool.txt', 'r') as f:
			x = f.read()

		mempool = ast.literal_eval(x)

		#print("MEMPOOL IS ", mempool)

		mempool[txid] = m.decode()
		with open('mempool.txt', 'w') as f:
			f.write(str(mempool))
		print('WRITTEN IN MEMPOOL')


		#with open('mempool.txt',mode='a+') as file:
		#	file.write(str(trans)+'\n')

#END


