from socket import * #p2p network
import rsa #for keys
import hashlib	# sha256
import sys
import ast #to literal evaluate dictionary
'''
(pubkey, privkey) = rsa.newkeys(512)
with open('privatepublickeys.txt',mode='a+') as file:
	file.write(str(pubkey) + str(privkey))'''

with open('private_key.pem') as file:
	pri_str = file.read()
	pri_byt = pri_str.encode('UTF-8')
	priv = rsa.PrivateKey.load_pkcs1(pri_byt)

with open('public_key.pem') as file:
	pub_str = file.read()
	pub_byt = pub_str.encode('UTF-8')
	publ = rsa.PublicKey.load_pkcs1(pub_byt)



pubkeyhash = hashlib.sha256(pub_byt).hexdigest()
#checking private and public keys
'''
print(priv.save_pkcs1().decode('utf-8'))
print(publ.save_pkcs1().decode('utf-8'))
'''
#menu options
print('Enter option\n\n0.Show pubkey hash\n')
print('1.Make Transaction\n ')
print('2.check balance\n')
print('3. mine current block\n')
s=2 # int(input())

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


transactions_recv= []

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

if(s==0):
	print(hashlib.sha256(pub_byt).hexdigest())

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
	check_balance()


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

#end

