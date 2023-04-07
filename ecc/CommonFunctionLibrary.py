
import time #To measure time it took to mine + block timestamp
import ast
import hashlib #to compute merkle root
from pprint import pprint
import sys
import emoji
from ecdsa import VerifyingKey

from socket import *

DIFFICULTY = (3,)


def getAmount(txid, on):
	#Tx from blocks
	with open('blocks/blockHeaders.txt') as f:
		b = f.read()
	b = ast.literal_eval(b)
	for block in b:
		txns = b[block]
		txns = ast.literal_eval(txns)
		if txid in txns:
			tx = ast.literal_eval(txns[txid])
			if (on >= len(tx['outputs']) ):
				return (-1,-1)
			return tx['outputs'][on]['amount']

	#reaches here if referenced txid and on don't exist in blocks
	with open('mempool.txt') as f:
		m = f.read()
	m = ast.literal_eval(m)
	if txid in m:
		tx = ast.literal_eval(m[txid])
		if (on >= len(tx['outputs'])):
			return (-1,-1)
		return tx['outputs'][on]['amount']
	return (-1,-2)

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
                print("TXN DOES NOT HAVE REQUIRED OUTPUT INDEX")
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
		print("[FATAL ERROR] INVALID OUTPUT INDEX REFERENCED, DOESN'T EXIST OR HAS BEEN USED \n\n")
		return False
	elif(args[0] == (-1,-2)):
		print("[FATAL ERROR] INPUT TXN AND OUTPUT INDEX DON'T EXIST IN UTXO SET")
		return False
	return True


def hash_tr(tr):
        hash_lvl1 = hashlib.sha256(str(tr).encode()).hexdigest()
        double_hash = hashlib.sha256(hash_lvl1.encode()).hexdigest()
        txid = double_hash
        return txid


def sumOfFee(mem):
	txidByFees = []
	for txid in mem:
		tx = ast.literal_eval(mem[txid])
		pprint(tx)
		if(tx == 0):
			continue
		inputs =tx['inputs']
		outputs = tx['outputs']
		inputAmount = 0
		outputAmount = 0
		for i in inputs:
			if i is None:
				continue
			inputAmount+=getAmount(i['prev_tran'],i['output_index'])
		for i in outputs:
			if i is None:
				continue
			outputAmount += int(i['amount'])

		fee = inputAmount - outputAmount
		txidByFees.append((fee, txid))
	return txidByFees

def merkle(mem):
	x = mem.copy()
	res = []
	for i in x:
		text = str(i) + str(x[i])
		res.append(text)

	while(len(res)!=1):
		resN = []
		if(len(res)%2 == 1):
			res.append(res[0])
		for i in range(1,len(res), 2):
			x = res[i] + res[i-1]
			hash = hashlib.sha256(x.encode()).hexdigest()
			resN.append(hash)
		print("Length of merkle tree -> ",len(resN))
		pprint("merkle tree -> ")
		pprint(resN)
		res = resN.copy()
	return res[0]

BLOCK_REWARD_GLOB = 10

def validateAsUTXO(tr, file):
	def validateAsUTXO(tr):

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
