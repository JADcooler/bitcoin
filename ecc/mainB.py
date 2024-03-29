#objective is to use mempool and mine a value lesser than a threshold


import time #To measure time it took to mine + block timestamp
import ast
import hashlib #to compute merkle root
from pprint import pprint
import sys
import emoji
from ecdsa import VerifyingKey

from socket import *
#LOCAL FILE IMPORTS
from CommonFunctionLibrary import hash_tr
from CommonFunctionLibrary import DIFFICULTY
BLOCK_REWARD_GLOB = 10
from CommonFunctionLibrary import MINER_PUBLIC_KEY

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

#block header contents
#merkle root
#prev block hash
#nonce


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

txidByFees = [] #approach to sort txids by fees and include X amount of txs
# approach to send transactions to main_f and he subtracts inputs and marks as UTXO
# by default all txns in mempool are valid, but in cases of race condition
# where one input is used for different transactions by same user, the one
# with higher fee is valid and the next one should not be

# in the implementation, the first one is considered valid, that approach is wrong


def sumOfFee(mem):

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


def mine(mem):
	#to get merkle root from mempool
	# with open('mempool.txt') as f:
	# 	mempool = f.read()
	# mem = ast.literal_eval(mempool)
	merkleRoot = merkle(mem)
	print("Merkle root is ",end ='')
	pprint( merkleRoot  )

	with open('blocks/blockHeaders.txt') as f:
		d = ast.literal_eval(f.read())
		lastBlock = list(d.items())[-1]
		prevHash = lastBlock[0] #get just the block hash

	#no of leading bits that should be zero is difficulty
	difficulty = DIFFICULTY[0]
	blockHeader = {'merkleRoot': merkleRoot,
			'timeStamp': time.time(), #used to adjust difficulty every 2016 blocks
			'prevHash' : prevHash,
			'nonce'    : 0
			}

	pprint("STARTING BLOCK MINING 🔴")

	time.sleep(1)


	a = 'fff' #dummy data to pass the loop
	start = time.time()
	while(int(a[:difficulty] , 16)!=0):  #sleeek
		blockHeader['nonce']+=1
		rawData = str(blockHeader).encode()
		a = hashlib.sha256(rawData).hexdigest()
		pprint(a)


	pprint("Block hash with required difficulty found 🟢")
	print("time took ",time.time() - start, " seconds")
	pprint(a)

	return blockHeader



def start(w):
	with open('mempool.txt') as f:
		mempool = f.read()
	mem = ast.literal_eval(mempool)

	print("OLD MEM IS ")
	pprint(mem)
	print("\n")

	sumOfFee(mem) #txid to str(tx data)
	txidByFees.sort(reverse=True)

	includeTxns = txidByFees[:w]
	pprint(includeTxns)

	output = make_out(MINER_PUBLIC_KEY, includeTxns)

	fees = 0
	for i in includeTxns:
		fees+=i[0]

	newTxids = []
	for i in includeTxns:
		newTxids.append(i[1])
	
	#mempool is just txid: str(tx)
	coinbaseTx = make_coinbase(output)
	print("\n\nTHE COINBASE TRANSACTION IS ")
	print("--------------------------- ")
	print("\nThe BLOCK REWARD IS ",10)
	print("\nMINER FEES FROM TRANSACTION ADDED IS ",fees,"\n")
	pprint(coinbaseTx)

	coinbaseTxid = hash_tr(coinbaseTx)
	#right now, we have list of txid we want to include and the coinbase txn
	#The plan is to create new mem (dict of txid: str(tx)) with fee sort and coinbase

	newMem = {}
	

	for txid, tx in mem.items():
		if txid in newTxids:
			newMem[txid] = str(tx)

	newMem[coinbaseTxid] = str(coinbaseTx) #added last to preserve coinbase even on txid collision
	
	print("NEW MEM IS ")
	pprint(newMem)
	print("\n")

	#starting to mine
	blockHeader = mine(newMem)

	rawData = str(blockHeader).encode()
	blockHash = hashlib.sha256(rawData).hexdigest()

	block = [blockHash , blockHeader, newMem]

	broadcast(block)

#FUNTIONS TO MAKE TX

def pubkeyHash():

	with open('ecc_public.pem') as f:
		public_key = VerifyingKey.from_pem(f.read())
	return hashlib.sha256(public_key.to_string()).hexdigest()

def make_out(recv, feeTXID):
	txfees = 0
	for i in feeTXID:
		txfees += i[0]

	output1={'output_no': 0, 'amount':BLOCK_REWARD_GLOB + txfees, 'pubkey_scr':recv, 'locktime': 100} #locktime of 100 for coinbase UTXOs
	return [output1,]

def make_coinbase(outputs):
	transaction = {}
	transaction['version']=1.0
	#inputs reference UTXO
	#list of inputs

	transaction['inputs']=[]
	#list of outputs
	transaction['outputs'] = outputs

	return transaction


s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)


def send(string):
	s.sendto(string.encode(),('255.255.255.255',12345)) #this is sufficient in a Real time environment
	#TEST NODES
	s.sendto(string.encode(),('127.0.0.1',12345))
	s.sendto(string.encode(),('127.0.1.0',12345))

def broadcast(bl):
	print("Sending block ")
	send("block")
	bl = [str(i) for i in bl]
	#bl is a list, first parameter contains block Hash and second one has block Header
	#third is list of transactions in block, includes coinbase
	send(bl[0])
	send(bl[1])
	send(bl[2])
	


#MAIN

def Init():
	w = input("Enter number of transactions to include ")
	start(int(w))



Init()
