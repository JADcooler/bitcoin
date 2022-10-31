import socket
import rsa

(pubkey, privkey) = rsa.newkeys(512)
with open('privatepublickeys.txt',mode='a+') as file:
	file.write(str(pubkey) + str(privkey))

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

''' end of program '''


