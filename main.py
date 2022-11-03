from socket import *
import rsa
import hashlib
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

print('Enter option\n\n0.Show pubkey hash\n')
print('1.Make Transaction\n ')
print('2.check balance\n')
print('3. mine current block\n')
s= int(input())

def transaction(recv_scr,a,b):
	transaction = {}
	transaction['version']=1.0
	#inputs reference UTXO
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
	transaction['version']=1.0
	#inputs reference UTXO
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
	with open('mempool.txt',mode='r') as file:
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
	with open('currentblock.txt',mode ='r') as file:
		listr=[]
		for tran in file:
			listr.append(tran)
	#coinbase transaction
	transaction = {}
	transaction['version']=1.0
	#inputs reference UTXO
	transaction['output_index']= gettxid()
	transaction['sequence']=0
	s=str(transaction['output_index'])+str(transaction['sequence'])
	u=rsa.encrypt(s.encode('UTF-8'),priv)
	w=pub_str
	k={'signature':u, 'public': w }
	transaction['signature_scr']=k
	#outputs
	transaction['output_number']=3
	transaction['amount']=100
	transaction['pubkey_scr']=hashlib.sha256(pub_byt).hexdigest()
	transaction['locktime']=transaction['sequence']

#end
