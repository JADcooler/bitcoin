from socket import * #p2p network
from ecdsa import SigningKey
from ecdsa import BadSignatureError, VerifyingKey #signature

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
s= int(input())

pubkeyhash = hashlib.sha256(public_key.to_string()).hexdigest()


def neededUTXO(amount):
	amount = int(amount)
	utxos = UTXOs()
	total = 0
	for tr in utxos:
		total+=tr[2]
	if(total < amount):
		return 0
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
	utxos = neededUTXO(amount)
	inputs = []
	available = 0
	for i in utxos:
		available += i[2]
		inputs.append(make_inp(i[0],i[1]))
	outputs = make_out(available, amount, recv, fees)
	return make_transaction(inputs, outputs)
	#After payment gotta update utxo list
	#TODO

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
	transaction['trans_identifier']=prev_tran
	transaction['output_index']= index
	transaction['sequence']=1
	s=str(transaction['output_index'])+str(transaction['trans_identifier'])
	s=rsa.encrypt(s.encode('UTF-8'),priv)
	w=pub_str
	k={'signature':s, 'public': w }
	transaction['signature_scr']=k
	'''

	#outputs
	#list of outputs
	transaction['outputs'] = outputs 

	'''
	output={'output_no': 0, 'amount':100, 'pubkey_scr':recv_scr, 'locktime': transaction['sequence'] }
	transaction['outputs'].append(output)

	output={'output_no': 1, 'amount':total_amount - amount - tran_fee, 'pubkey_scr':pubkeyhash  , 'locktime': 0 }
	transaction['outputs'].append(output)
	'''
	'''
	transaction['output_number']=3
	transaction['amount']=100
	transaction['pubkey_scr']=recv_scr
	transaction['locktime']=transaction['sequence']
	'''
	return transaction

#We have the requirement to find spent and unspent transacion outputs.
#To start things off, we are gonna make a function to spend UTXOs

	'''
	transaction['trans_identifier']=prev_tran
	transaction['output_index']= index
	transaction['sequence']=1
	s=str(transaction['output_index'])+str(transaction['trans_identifier'])
	s=rsa.encrypt(s.encode('UTF-8'),priv)
	w=pub_str
	k={'signature':s, 'public': w }
	transaction['signature_scr']=k
	'''
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
	print(sigScr)
	d_sign = sigScr['signature'].encode('ISO-8859-1')
	d_publ = sigScr['publicKey'].encode('ISO-8859-1')
	d_publicKey = VerifyingKey.from_string(d_publ)
	x = d_publicKey.verify(d_sign, plainText.encode())
	print(x)
	#signature script END - 4
	input['sigScr'] = sigScr
	return input
	#YAY





transactions_recv= []

latest_block = 'block0.txt'

def UTXOs():
	with open('usr_cache/balances.txt', mode='r') as f:
		dict_str = f.read()
	balances = ast.literal_eval(dict_str) #check if cache of utxo stored

	if latest_block in balances:
		print('CACHE HIT')
		global transactions_recv
		transactions_recv = balances[latest_block]
		#print(transactions_recv)
		return balances[latest_block]

	with open('blocks/'+latest_block, mode='r') as f:
		block_str = f.read()
	block = ast.literal_eval(block_str)
	for item in block.items():
		tr_data = ast.literal_eval(item[1])
		outputs = tr_data['outputs']
		for output in outputs:
			if(output['pubkey_scr']==publickey_hash):
				transactions_recv.append((item[0],output['output_no'],output['amount']))
	balances[latest_block] = transactions_recv
	with open('usr_cache/balances.txt', mode='w') as f:
		f.write(str(balances))
	return transactions_recv


def check_balance():
	#first we check all transactions recieved to us
	print(pubkeyhash,'\n')
	with open('blocks.txt', mode = 'r') as file:
		x=file.read()
		print('readed line ',x)
		trans = ast.literal_eval(x)[1]
		for y in trans.items():
			i=y[1]


			tr = ast.literal_eval(i)
			#print(type(tr),tr)
			print('trans: ',y[0])
			for x in tr['outputs']:
				print(x['output_no'],x['pubkey_scr'])
				if(x['pubkey_scr']==pubkeyhash):
					transactions_recv.append((y[0],x['output_no']))
	print(transactions_recv)
	UTXO={}
	for i in transactions_recv:
		UTXO[i]=0
	tranrecv_outputs=[]
	test = transactions_recv[0]
	sigscript(test[0],test[1]  )



	'''
	combos=[]
	with open('mempool.txt') as file:
		for tran in file:
			tr=ast.literal_eval(tran)
			if(tr['pubkey_scr']==pubkeyhash):
				combos.append((tr['output_index'],tr['sequence'],tr['amount']))
	freqc = {}
	for combo in combos:
		freqc[combo]=0
	print(freqc)
	with open('mempool.txt') as file:
		for tran in file:
			tr=ast.literal_eval(tran)
			combo=((int(tr['output_index']),int(tr['sequence']),int(tr['amount'])))
			freqc[combo]+=1

	balance=0
	print(freqc)
	for key,val in freqc.items():
		if(val==1):
			 balance+=key[2]
	print('\nBALANCE IS ',balance)
	'''

def gettxid():
	x=0
	with open('mempool.txt') as file:
		x+=1
	return x

if(s==4):
	print('Enter parameters')
	print('txid')
	txid = input()
	print('output index')
	outputIndex = input()
	make_inp(txid, outputIndex);

if(s==0):
	print(hashlib.sha256(public_key.to_string()).hexdigest())

elif(s==1):
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

elif(s==2):
	print(UTXOs())
	sum = 0
	#print('asd', transactions_recv)
	for tr in transactions_recv:
		sum += tr[2]
	print("\n\nnet balance is ",sum)

elif(s==3):
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


if(s==9):
	x = input('Enter amount ')
	x = neededUTXO(x)
	print(x)

if(s==10):
	x=input('amount ')
	y=input('receiver ')
	z=pay(x,y, 3)
	print('starts here')
	print(str(z))
#end

