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
s= int(input())

def make_transaction(recv_scr,a,b):
	transaction = {}
	transaction['version']=1.0
	#inputs reference UTXO
	#list of inputs
	transaction['trans_identifier']=123;
	transaction['output_index']= a
	transaction['sequence']=b
	s=str(transaction['output_index'])+str(transaction['trans_identifier'])
	s=rsa.encrypt(s.encode('UTF-8'),priv)
	w=pub_str
	k={'signature':s, 'public': w }
	transaction['signature_scr']=k
	#outputs
	#list of outputs
	transaction['output_number']=3
	transaction['amount']=100
	transaction['pubkey_scr']=recv_scr
	transaction['locktime']=transaction['sequence']

def check_balance():
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
def gettxid():
	x=0
	with open('mempool.txt') as file:
		x+=1
	return x

if(s==0):
	print(hashlib.sha256(pub_byt).hexdigest())

elif(s==1):
	combos = []
	with open('mempool.txt') as file:
		for tran in file:
			tr=ast.literal_eval(tran)
			if(tr['pubkey_scr']==pubkeyhash):
				combos.append((tr['output_index'],tr['sequence'],tr['amount']))




	print('Enter pubkey hash of reciever')
	recv_scr= input()

	print('combos are ')
	for combo in combos:
		print(combo[:2], 'amount : ',combo[2])

	print('Enter UTXO to use')
	a=input()
	b=input()
	transaction = {}

	'''
	transaction['version']=1.0
	#inputs reference UTXO
	transaction['trans_identifier']=123;
	transaction['output_index']= a
	transaction['sequence']=b
	s=str(transaction['output_index'])+str(transaction['sequence'])
	u=rsa.encrypt(s.encode('UTF-8'),priv)
	w=pub_str
	k={'signature':u, 'public': w }
	transaction['signature_scr']=k
	#outputs
	transaction['output_number']=3
	transaction['amount']=100
	transaction['pubkey_scr']=recv_scr
	transaction['locktime']=transaction['sequence']
	'''

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

	'''
	x=1
	balance = 0 
q	with open('mempool.txt',mode='r') as file:
		trans=file.read().split('\n')
		print(trans)
		trans=trans[:-1]
		print(len(trans))
		for tran in trans:
			print('checking transaction ',x)
			x+=1
			print(tran,'\n')
			print(type(tran))
			tr = ast.literal_eval(tran)
			#print(type(tr))

			print(tr)
			digest = tr['pubkey_scr']
			if(hashlib.sha256(pub_byt).hexdigest()==digest):
				balance+=tr['amount']
			#signed_content=str(tr['output_index'])+str(tr['sequence'])
		print('\n\nBALANCE IS ',balance)
	'''

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

