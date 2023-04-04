
from socket import * #p2p network
from ecdsa import SigningKey
from ecdsa import BadSignatureError, VerifyingKey #signature

from pprint import pprint

import hashlib	# sha256
import sys
import ast #to literal evaluate dictionary


#Importing keys

with open('ecc_private.pem', mode='r') as f:
	private_key=SigningKey.from_pem(f.read()) #private key
with open('ecc_public.pem', mode='r') as f:
	public_key=VerifyingKey.from_pem(f.read()) #public key








#menu options
print('Enter option\n\n0.Show pubkey hash\n')
print('1.Make Transaction\n ')
print('2.check balance\n')
print('3. mine current block\n')
print('4. TEST\n')
print('9. neededUTXO\n')
print('10. Pay\n')

choice = int(input())

pubkeyhash = hashlib.sha256(public_key.to_string()).hexdigest()


def neededUTXO(amount):
	utxos = UTXOs()
	total = 0
	for tr in utxos:
		total+=tr[2]
	if(total < amount):
		return -1
	rList = []
	cur = 0
	for tr in utxos:
		cur += tr[2]
		rList.append(tr)
		if (cur>=amount):
			break
	return rList

def hash_tr(tr):
	hash_lvl1 = hashlib.sha256(str(tr).encode()).hexdigest()
	double_hash = hashlib.sha256(hash_lvl1.encode()).hexdigest()
	txid = double_hash
	return txid



def pay(amount, recv, fees):
	utxos = neededUTXO(int(amount)+int(fees))
	inputs = []



	if(utxos == -1):
		print("NOT ENOUGH BALANCE TO COMPLETE TRANSACTION")
		return

	print("\n\nINPUTS")
	print("------")
	pprint(utxos)
	print("\n\n")
	available = 0
	for i in utxos:
		available += i[2]
		inputs.append(make_inp(i[0],i[1]))
	outputs = make_out(available, amount, recv, fees)
	print("OUTPUTS")
	print("-------")
	pprint(outputs)
	print("\n\n")
	tr =  make_transaction(inputs, outputs)
	#After payment gotta update utxo list, we do that in main_f
	#we just broadcast Transaction
	broadcast(tr)
	print('SUCCESSFULLY BROADCASTED THE TRANSACTION !')



s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

def send(string):
	s.sendto(string.encode(),('255.255.255.255',12345)) #this is sufficient in a Real time environment
	#TEST NODES
	s.sendto(string.encode(),('127.0.0.1',12345))
	s.sendto(string.encode(),('127.0.1.0',12345))

def broadcast(tr):
	print("transmitter txid " + hash_tr(tr))

	send("transaction")
	send(hash_tr(tr))

	send(str(tr))


def make_out(available, amount, recv, fees):
	output1={'output_no': 0, 'amount':amount, 'pubkey_scr':recv, 'locktime': 1 }
	payToSelf = int(available) - int(amount) - fees
	output2={'output_no': 1, 'amount':payToSelf,'pubkey_scr': pubkeyhash, 'locktime':1}
	return [output1,output2]

def make_transaction(inputs, outputs):
	transaction = {}
	transaction['version']=1.0
	#inputs reference UTXO
	#list of inputs

	transaction['inputs']=inputs
	'''
	dict of
		'prev_tran'
		'output_index'
		'sequence'
		'sigScr' dict of
				'signature'
				'publicKey'
	'''

	#outputs
	#list of outputs
	transaction['outputs'] = outputs
	'''
	dict of
		'output_no'
		'pubkey_scr'
		'amount'
		'locktime'
	'''

	return transaction

def make_inp(prev_tran, output_index):
	input = {}
	#needs 4 things
	#prev_tran - 1
	input['prev_tran'] = prev_tran
	#output_index - 2
	input['output_index'] = output_index
	#sequence - 3
	input['sequence'] = '0xFFFFFFFF' #it's a value ignored by bitcoin
	#signature script START
	plainText = str(prev_tran) + str(output_index)

	cipherText = private_key.sign(plainText.encode()) #string to byte
	signature = cipherText.decode('ISO-8859-1') #byte to string
	pkString = public_key.to_string().decode('ISO-8859-1')
	sigScr = {'signature': signature, 'publicKey': pkString}
	d_sign = sigScr['signature'].encode('ISO-8859-1')
	d_publ = sigScr['publicKey'].encode('ISO-8859-1')
	d_publicKey = VerifyingKey.from_string(d_publ)
	x = d_publicKey.verify(d_sign, plainText.encode())
	#signature script END - 4
	input['sigScr'] = sigScr
	return input
	#YAY





transactions_recv= []

latest_block = 'block0.txt'

def checkUserFromTXNS(txns):
	utxo = []
	#public_key that we import in the start
	pkhash = hashlib.sha256(public_key.to_string()).hexdigest()

	for txid in txns:
		tr = ast.literal_eval(txns[txid])
		for w in range(len(tr['outputs'])):
			i = tr['outputs'][w]
			if ( i is None):
				continue
			if (i['pubkey_scr']==pkhash):
				print("APPENDED TR WITH TXID ",hash_tr(tr), "WITH OUTPUT INDEX",w )
				utxo.append((txid, w, tr['outputs'][w]['amount'] ))
				print(utxo)
	return utxo

def UTXOs():
	with open('UTXO/UTXO.tmp') as f:
		UTXO = f.read()
	UTXO = ast.literal_eval(UTXO)
	userUTXO = []
	for block in UTXO:
		txns = ast.literal_eval(UTXO[block])
		print("PROCESSING ",block)
		userTXNS = checkUserFromTXNS(txns)
		[ userUTXO.append(i) for i in userTXNS]
		print(userUTXO)

	return userUTXO



if(choice==4):
	print('Enter parameters')
	print('txid')
	txid = input()
	print('output index')
	outputIndex = input()
	make_inp(txid, outputIndex);

if(choice==0):
	print(hashlib.sha256(public_key.to_string()).hexdigest())

elif(choice==1):
	print('Enter receiver pubkey hash')
	recrhash= input()
	selfhash = pubkeyhash

	print('Enter amount to send (integer)')
	amount= input()

	print('Enter transaction fees (integer)')
	tran_fee = input()


	#start code to find belonging UTXOs


	total_amount
	#end

#	s=str(transaction['output_index'])+str(transaction['trans_identifier'])
	s='2'
	s=rsa.encrypt(s.encode('UTF-8'),priv)
	w=pub_str
	k={'signature':s, 'public': w }

	input = {'trans_identity': 1,'outputnoofprev': 1,'sequence': 1 ,'sigscript':k}

	all_outpust=[]


	output={'output_no': 0, 'amount':amount, 'pubkey_scr':recrhash, 'locktime': transaction['sequence'] }
	all_outputs.append(output)

	output={'output_no': 1, 'amount':total_amount - amount - tran_fee, 'pubkey_scr':selfhash  , 'locktime': 0 }
	all_outputs.append(output)


	transaction = make_transaction()


	#finding hash of transaction to store it in a dictioanry / hash table
	trans_string = str(transaction)
	trans_byt = trans_string.encode()
	transaction_hash=hashlib.sha256(trans_byte).hexdigest()

	#broadcasting transaction
	s=socket(AF_INET, SOCK_DGRAM)
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	tran_message = str(transaction)
	print(sys.getsizeof('transaction'))
	print(sys.getsizeof(tran_message))
	s.sendto('transaction'.encode(),('255.255.255.255',12345))
	s.sendto(tran_message.encode(),('255.255.255.255',12345))

elif(choice==2):
	print(UTXOs())
	sum = 0
	#print('asd', transactions_recv)
	for tr in transactions_recv:
		sum += tr[2]
	print("\n\nnet balance is ",sum)

elif(choice==3):
	make_transaction()
	listr.insert(0,str(transaction))
	blockheaders=[]
	with open('blocks.txt',mode='r') as blocks:
		for block in blocks:
			blockheaders=ast.literal_eval(block)[0]
	prevheader=blockheaders[-1] #get last header
	t1=str(listr[0])+str(listr[1])
	t1=hashlib.sha256(t1).hexdigest()
	t2=str(listr[2])+str(listr[3])
	t2=hashlib.sha256(t2).hexdigest()
	t3=str(listr[4])+str(listr[5])
	t3=hashlib.sha256(t3).hexdigest()
	t12=t1+t2
	t12=hashlib.sha256(t12).hexdigest()
	t123=t12+t3
	t123=hashlib.sha267(t123).hexdigest()
	merkleroot = t123

	nonce=0
	for n in range(100000000):
		blockheader = [prevheader,merkleroot,n]
		check = hashlib,sha256(blockheader.encode()).hexdigest()
		if(hexdigest[0]=='0' and hexdigest[1]=='0'):
			nonce = n
			break
	block = [blockheader, prevheader, merkleroot, nonce]

	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	tran_message = str(transaction)
	print(sys.getsizeof('transaction'))
	print(sys.getsizeof(tran_message))
	s.sendto('block'.encode(),('255.255.255.255',12345))
	s.sendto(block.encode(),('255.255.255.255',12345))


if(choice==9):
	x = input('Enter amount ')
	x = neededUTXO(x)
	print(x)

if(choice==10):
	x=input('amount ')
	y=input('receiver ')
	w=input('fees ')
	z=pay(x,y, int(w))
	print('starts here')
	print(str(z))
#end

