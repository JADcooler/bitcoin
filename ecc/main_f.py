from socket import *
import ast
import hashlib
from ecdsa import BadSignatureError, VerifyingKey

s=socket(AF_INET, SOCK_DGRAM)
#test node, in deployment we run in s.bind('',12345))
#such that it can listen from 255.255.255.255
s.bind(('127.0.0.1',12345))

#important that s.bind has to be in line 8(0-8) or 9(1-9) for local node scripts

from pprint import pprint

#importing from library
from CommonFunctionLibrary import *


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

	pprint("THIS SAYS THE PERSON WHO GAVE THE SIGNATURE WITH PUBLIC KEY, HAD ACTUALLY USED HIS PRIVATE KEY TO ENCRYPT PREV_TXID AND OUTPUT INDEX")
	pprint("THIS IS USED SUCH THAT ONLY THE PERSON IN POSSESSION OF THE PRIVATE KEY FOR THAT PUBLIC KEY CAN USE HIS FUNDS")
	pprint("---------------------------------------------------------------------------------")
	pprint("THE REST WE HAVE TO DO IS VERIFY THAT THE INPUT REFERENCED EXISTS IN UTXO SET AND IS PAID TO TO HIM AND NOT OTHERS")

	return flag


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
		pprint("NO BLOCK HAS REQUIRED TX")
		return False

	txns = ast.literal_eval(blocks[blockF])
	txn = ast.literal_eval(txns[txid])

	toPop = -1
	outputs = txn['outputs']
	for i in range(len(outputs)):
		if(outputs[i] is not None and outputs[i]['output_no']==on):
			toPop = i
			break
	if(toPop == -1):
		pprint("TXN DOES NOT HAVE REQUIRED OUTPUT INDEX")
		return False
	#we are now about to modify txns string in block dict


	modifyThis = blocks[blockF] #later used as l value
	modifyTxns = ast.literal_eval(modifyThis) #later as l value
	modifyTxn =ast.literal_eval( modifyTxns[txid]) #later uesd as l value


	modifyTxn['outputs'][toPop] = None

	modifyTxns[txid] = str(modifyTxn)
	blocks[blockF] = str(modifyTxns)

	with open(file, 'w') as f:
		f.write(str(blocks))

	print("SUCCESFULLY REMOVED OUTPUT",on," FROM",txid)
	return True


def handleError(args):
	if(args[0]  == (-1,-1)):
		pprint("[FATAL ERROR] INVALID OUTPUT INDEX REFERENCED, DOESN'T EXIST OR HAS BEEN USED \n\n")
		return False
	elif(args[0] == (-1,-2)):
		pprint("[FATAL ERROR] INPUT TXN AND OUTPUT INDEX DON'T EXIST IN UTXO SET")
		return False
	return True


def validateAsUTXO(tr):
	file = 'UTXO/UTXO.tmp'
	#For a transaction to be validated, all its inputs must
	#exist either in a block or in the mempool.

	pk = tr['inputs'][0]['sigScr']['publicKey']
	pk = VerifyingKey.from_string(pk.encode('ISO-8859-1'))
	pk = hashlib.sha256(pk.to_string()).hexdigest()

	a = verifySignature(tr)
	if(a==False):
		pprint("INVALID SIGNATURE")
		return False

	txid = hash_tr(tr)

	file = 'UTXO/UTXO.tmp'

	with open(file, 'r') as f:
		UTXO = f.read()
	UTXO = ast.literal_eval(UTXO) #get dict of blocks


	#checking if all inputs reference the public key of tx maker
	pprint("	\#checking if all inputs reference the public key of tx maker")

	inputx = [ (i['prev_tran'], i['output_index']) for i in tr['inputs'] ]

	result = True
	for block in UTXO:
		txns = ast.literal_eval(UTXO[block])
		for i in inputx:
			if i[0] in txns: #i[0] is txid
				txn = ast.literal_eval(txns[i[0]])
				print(i[1], len(txn['outputs']))
				pprint(txn)
				b = 0
				try:
					b = txn['outputs'][i[1]]['pubkey_scr']
				except IndexError as e:
					print("Referenced output index doesn't exist",e)
				except Exception as e:
					print("UNEXPECTED EXCEPTION ",e)
				#we expect main.py to send valid output no
				#so, the last exception would catch if it's None
				result*= (b == pk)


	if(result == False):
		pprint("NOT ALL INPUTS USED REFERENCE TX SIGNER ")
		return [(-1,-1)] #code (-1,-1) for invalid output index
	#____________________________________________

	inputTxids = [ i['prev_tran']+ str(i['output_index'])   for i in tr['inputs'] ]


	print("Input prev_trans ")
	pprint(inputTxids)
	#approach to combine all transactions with o/p in UTXO and check if
	#set prev tran is subset of all txids in UTXO
	allTxids = {}
	for block in UTXO: #UTXO is of format { 'blockno': str(txns) }
		tnxs = ast.literal_eval(UTXO[block])
		for tnx in tnxs: #tnxs is of format { 'txid' : str(tx data) }
			x = tnxs[tnx]
			x = ast.literal_eval(x)
			for output in x['outputs']:
				if (output is None):
					continue

				allTxids[tnx + str(output['output_no'])] = x['outputs']

	pprint("all txids in UTXO ")


	for i in allTxids:
		pprint(i)



	pprint('all prev trans')
	for i in inputTxids:
		pprint(i)

	bool = set(inputTxids).issubset(set(allTxids.keys()))
	print("they are equal? ",bool)
	if(not bool):
		return [(-1,-2)]

	return [ (i['prev_tran'], i['output_index']) for i in tr['inputs'] ]


def checkCoinbaseCount(mem):
	c = 0
	for txid in mem:
		tx = mem[txid]
		if(len(tx['inputs']) == 0):
			c+=1
	return c
	

def findCoinbase(mem):
	for txid in mem:
		tx = mem[txid]
		if(len(tx['inputs'] == 0)):
			return txid
	return -1



while(1):

	pprint('waiting..')
	m=s.recvfrom(1024)
	x=m[0].decode()
	pprint(x)

	if(x=='transaction'): #Start strings
		m=s.recvfrom(1024)[0]
		RECV_txid = m.decode()


		m=s.recvfrom(2048)[0] #hope 2048 is ok..
		txid = hash_tr(m.decode())

		if(RECV_txid != txid):
			pprint("FATAL: SENT TXID AND COMPUTED TXID DON'T MATCH")
			continue

		print('	-> processing transaction', end ='' )
		pprint(txid) #print txid
		pprint(m)
		pprint("\n\n\n")

		tr = ast.literal_eval(m.decode())


		params = validateAsUTXO(tr)
		print("params are ",params)

		cont = handleError(params)

		if(not cont):
			continue

		flag = 1
		for i in params:
			bool = deleteTxOutputs(i[0], i[1])
			if(not bool):
				pprint("DELETE TX FAILED for (txid, on) ",i)
				flag = 0
		if(not flag):
			continue

		with open('mempool.txt', 'r') as f:
			x = f.read()

		mempool = ast.literal_eval(x)

		mempool[txid] = m.decode()
		with open('mempool.txt', 'w') as f:
			f.write(str(mempool))
		pprint('WRITTEN IN MEMPOOL')

		with open('UTXO/UTXO.tmp','r') as f:
			u = f.read()
			u = ast.literal_eval(u)

		with open('UTXO/UTXO.tmp','w') as f:
			if('mempool' in u):
				txns = ast.literal_eval(u['mempool'])
				txns[txid] = m.decode()
			else:
				txns = {txid: m.decode()}


			u['mempool'] = str(txns)
			f.write(str(u))


		#with open('mempool.txt',mode='a+') as file: 
		#	file.write(str(trans)+'\n')
	elif(x=='block'):
		m=s.recvfrom(1024)[0] #block Hash
		RECV_blHash = m.decode()


		m=s.recvfrom(2048)[0] #We are just receiving the block Header
		
		blockHash = hashlib.sha256(m).hexdigest()
		blockHeader = ast.literal_eval(m.decode())
		print("RECEIVED ",blockHash)

		if(RECV_blHash != blockHash):
			print("Unequal block hashes")
		
		m=s.recvfrom(25048)[0] #LAARRGE Data, may need attention in the near future. is block TXNS
		#----------------------------------------------------------------------------------------		
		#									BLOCK VERIFYING
		#----------------------------------------------------------------------------------------
		mem = ast.literal_eval(m.decode())

		CoinbaseCount = checkCoinbaseCount(mem)
		if( CoinbaseCount != 1):
			print("invalid coinbase transaction count, Expected one. found ", CoinbaseCount )
			continue

		difficulty = DIFFICULTY[0]
		if(int(blockHash[:difficulty] ,16) != 0):
			print("BLOCK HEADER HASH IS NOT BELOW THE THRESHOLD")
			continue

		merkleRoot = merkle(mem)
		bl_merkle = blockHeader['merkle']
		if(merkleRoot != bl_merkle):
			print("MERKLE TREES DON'T MATCH")
			continue

		feeList = sumOfFee(mem)
		fees = 0
		for f in feeList:
			fees += f[0]
		coinbaseTxid = findCoinbase(mem)
		if(coinbaseTxid == -1):
			print("COINBASE TRANSACTION DOESN'T EXIST")
		coinbaseTx = ast.literal_eval(mem[coinbaseTxid])
		co_fees = coinbaseTx['outputs'][0]['amount'] - BLOCK_REWARD_GLOB
		if(co_fees != fees):
			print("INVALID COINBASE TRANSACTION [OUTPUT AMOUNT IS DIFFERENT THAN EXPECTED] ")

		#----------------------------------------------------------------------------------------		
		#									BLOCK VERIFYING
		#----------------------------------------------------------------------------------------


#END


