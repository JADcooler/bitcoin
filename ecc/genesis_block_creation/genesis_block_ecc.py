from ecdsa import SigningKey
from ecdsa import BadSignatureError, VerifyingKey



def make_transaction(outputs):
	tr={}
	tr['version'] = 1.0
	tr['inputs']=[]
	tr['outputs']=outputs
	tr['locktime']=0
	return tr

def make_output(no, amount, pubkey_scr):
	output={'output_no': no, 'amount': amount, 'pubkey_scr':pubkey_scr }
	return output

import hashlib

def hash_tr(tr):
	hash_lvl1 = hashlib.sha256(str(tr).encode()).hexdigest()
	double_hash = hashlib.sha256(hash_lvl1.encode()).hexdigest()
	txid = double_hash
	return txid

hash = '3035e4f326b5b95cadf396cd038e99f02a99fb1ddb5d5e6d521e3584db6ad6ab'


block = {} # key = txid, val = string of transaction


#start of first transaction
o1 = make_output(0,100,hash)
o2 = make_output(1, 25,hash)

outputs = [o1,o2]

tr = make_transaction(outputs)

block[hash_tr(tr)] = str(tr)
#end of first transaction


#start of 2nd transaction
o1 = make_output(0,200,hash)

outputs = [o1,]

tr = make_transaction(outputs)

block[hash_tr(tr)] = str(tr)
#end of 2nd transaction




#inserting contents of block into block.txt


print("writing block with content "+str(block)+" into file blocks.txt")
with open('blocks.txt', mode = 'w') as f:
	f.write(str(block))

#end
