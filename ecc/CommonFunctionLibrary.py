
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

def deleteTxOutputsFILE(txid, on, file):
        #This verion uses file string from parameter
        #by giving a txn, we remove an output from it as UTXO

        print("DELETING ",txid, " OUTPUT ", on, " FILE PARAMETER COMMONFUNCTIONLIBRARY VERSION")

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
        modifyTxn =ast.literal_eval( modifyTxns[txid]) #later used as l value


        modifyTxn['outputs'][toPop] = None

        modifyTxns[txid] = str(modifyTxn)
        blocks[blockF] = str(modifyTxns)

        with open(file, 'w') as f:
                f.write(str(blocks))

        print("SUCCESFULLY REMOVED OUTPUT",on," FROM",txid)

		

        return True


def handleError(args):
	if(args is None):
		return True
	if(args[0]  == (-1,-1)):
		print("[FATAL ERROR] INVALID OUTPUT INDEX REFERENCED, DOESN'T EXIST OR HAS BEEN USED \n\n")
		return False
	elif(args[0] == (-1,-2)):
		print("[FATAL ERROR] INPUT TXN AND OUTPUT INDEX DON'T EXIST IN UTXO SET")
		return False
	elif(args[0] == (-2,-1)):
		print("[FATAL ERROR] OUTPUT AMOUNT IS GREATER THAN INPUT AMOUNT FOR NON-COINBASE TXN\n\n")
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


def validateAsUTXOFILE(tr, file):
	
	##THIS FUNCTION IS USED TO VALIDATE TRANSACTIONS ONCE BLOCK IS RECEIVED IN MAIN_F(RECEIVER)

	#For a transaction to be validated, all its inputs must
	#exist either in a block or in the mempool.

	#This function is made to validate only non coinbase txns, so if a txn is coinbase, we return None
	#The params returned when used in deleteUTXO should be checked if it is none

	#There are other functions to determine if fees, miner fee and no of coinbase tx is correct
	#in BLOCK VERIFYING SECTION

	if(len(tr['inputs']) == 0 ):#This part is different from validateAsUTXO(tr). only blocks have coinbase
		return None			#This should throw error in normal validateAsUTXO as its coinbase
							#And Coinbase TXNS are not meant to be received in mempool or transaction

	pk = tr['inputs'][0]['sigScr']['publicKey']
	pk = VerifyingKey.from_string(pk.encode('ISO-8859-1'))
	pk = hashlib.sha256(pk.to_string()).hexdigest()
	##GETS PUBLIC KEY FROM INPUT OF TRANSACTION

	a = verifySignature(tr)
	if(a==False):
		pprint("INVALID SIGNATURE")
		return False

	txid = hash_tr(tr)
	##HASH TRANSACTION


	with open(file, 'r') as f:
		UTXO = f.read()
	UTXO = ast.literal_eval(UTXO) #get dict of blocks
	##PARSE IT AS BLOCK_ID: STR TXNS

	#checking if all inputs reference the public key of tx maker
	pprint("	\#checking if all inputs reference the public key of tx maker")

	inputx = [ (i['prev_tran'], i['output_index']) for i in tr['inputs'] ]

	inputAmount = 0	#adding amount validation

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
					inputAmount+=int(txn['outputs'][i[1]]['amount']) #adding amount validation
				except IndexError as e:
					print("Referenced output index doesn't exist",e)
				except Exception as e:
					print("UNEXPECTED EXCEPTION ",e)
				#we expect main.py to send valid output no
				#so, the last exception would catch if it's None
				result*= (b == pk) #RESULT IS TRUE IF try block got executed

	outputAmount = 0 #adding amount validation

	for i in tr['outputs']: #adding amount validation
		outputAmount += int(i['amount']) #adding amount validation

	print("FEES CONTRIBUTED BY THIS TRANSACTION TO MINER IS ",inputAmount - outputAmount)
	#adding amount validation
	if(outputAmount > inputAmount ): #IF MONEY GREATER THAT WHAT WE GET FROM UTXO IS USED, FATAL ERROR
		pprint("INVALID AMOUNT USED FOR NON COINBASE TRANSACTION")
		return [(-2,-1)] #code (-2,-1) for invalid amount

	if(result == False):
		pprint("NOT ALL INPUTS USED REFERENCE TX SIGNER ")
		return [(-1,-1)] #code (-1,-1) for invalid output index
	#____________________________________________

	inputTxids = [ i['prev_tran']+ str(i['output_index'])   for i in tr['inputs'] ]
	#EACH INPUT THAT CAN IDENTIFY AN OUTPUT THAT WAS USED IS USED AS A SINGLE STRING

	

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
	#RETURNING CAUSE VALIDATION IS COMPLETE AND MEANT AS INPUT TO DELETETXOUTPUT

	##NOTE THAT THERE IS AN IMPLICIT TRUST OF THE TX WE USE AS INPUTS. SO WE DON'T CHECK AMOUNT
	##MAYBE WE CAN? CHECK OUTPUTS USED AND INPUT PREV_TRAN OUTPUTS USED AND IF THEY ALLOW fees>=0
