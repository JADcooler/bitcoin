#objective is to use mempool and mine a value lesser than a threshold


import time #To measure time it took to mine + block timestamp
import ast
import hashlib #to compute merkle root
from pprint import pprint
import sys
import emoji
from ecdsa import VerifyingKey
global BLOCK_REWARD_GLOB

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
		print("merkle tree -> ")
		pprint(resN)
		res = resN.copy()
	return res[0]

#block header contents
#merkle root
#prev block hash
#nonce

def mine():
	#to get merkle root from mempool
	with open('mempool.txt') as f:
		mempool = f.read()
	mem = ast.literal_eval(mempool)
	merkleRoot = merkle(mem)
	print("Merkle root is ", merkleRoot  )

	with open('blocks/blockHeaders.txt') as f:
		d = ast.literal_eval(f.read())
		lastBlock = list(d.items())[-1]
		prevHash = lastBlock[0] #get just the block hash

	difficulty = 7 #no of leading bits that should be zero

	blockHeader = {'merkleRoot': merkleRoot,
			'timeStamp': time.time(), #used to adjust difficulty every 2016 blocks
			'prevHash' : prevHash,
			'nonce'    : 0
			}

	print("STARTING BLOCK MINING 🔴")

	time.sleep(1)


	a = 'fff' #dummy data to pass the loop
	start = time.time()
	while(int(a[:difficulty] , 16)!=0):
		blockHeader['nonce']+=1
		rawData = str(blockHeader).encode()
		a = hashlib.sha256(rawData).hexdigest()
		print(a)
	print("Block hash with required difficulty found 🟢")
	print("time took ",time.time() - start, " seconds")
	print(a)

def coinbase():
	print(pubkeyHash())






#FUNTIONS TO MAKE TX

def pubkeyHash():

	with open('ecc_public.pem') as f:
		public_key = VerifyingKey.from_pem(f.read())
	return hashlib.sha256(public_key.to_string()).hexdigest()

def make_out(recv):
	output1={'output_no': 0, 'amount':BLOCK_REWARD_GLOB, 'pubkey_scr':recv, 'locktime': 100} #locktime of 100 for coinbase UTXOs
	return [output1]

def make_coinbase(outputs):
	transaction = {}
	transaction['version']=1.0
	#inputs reference UTXO
	#list of inputs

	transaction['inputs']=[]
	#list of outputs
	transaction['outputs'] = outputs

	return transaction


#MAIN

coinbase()


