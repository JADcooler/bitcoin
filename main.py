from socket import *
import rsa
import hashlib

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


#checking private and public keys
'''
print(priv.save_pkcs1().decode('utf-8'))
print(publ.save_pkcs1().decode('utf-8'))
'''

print('enter option\n1.Make Transaction\n ')
s=int(input())

if(s==1):
	print('Enter pubkey hash of reciever')
	recv_scr= input()
	transaction = {}
	transaction['version']=1.0
	#inputs reference UTXO
	transaction['output_index']= 0
	transaction['sequence']=0
	s=str(transaction['output_index'])+str(transaction['sequence'])
	k={'signature': rsa.encrypt(k.encode('UTF-8'),priv), 'public':pub_str.encode('base64') }
	transaction['signature_scr']=k
	#outputs
	transaction['output_number']=3
	transaction['amount']=100
	transaction['pubkey_scr']=hashlib.sha256(pub_byt).hexdigest()
	transaction['locktime']=transaction['sequence']
	with open('mempool.txt',mode='a+') as file:
		print(str(transaction))
		x=str(transaction).encode('base64')
		print(x)
		file.write(x)
	s=socket(AF_INET, SOCK_DGRAM)
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	tran_message = str(transaction)
	s.sendto('transaction'.encode(),('255.255.255.255',12345))
	s.sendto(tran_message.encode(),('255.255.255.255',12345))


#end

