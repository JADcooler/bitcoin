import socket
import rsa
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
	transaction['signature_scr']=
	#outputs
	transaction['output_number']=3
	transaction['amount']=
	transaction['pubkey_scr']=
	transaction['locktime']=transaction['sequence']


#end

