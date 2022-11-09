from socket import *
import rsa
import hashlib
#ccfd4aa0bdead15520508713f2943e8e40e76cd596ae748fc5ec97a53d361d80

with open('public_key.pem') as file:
	pub_str = file.read()
	pub_byt = pub_str.encode('UTF-8')
	publ = rsa.PublicKey.load_pkcs1(pub_byt)
	pubh = hashlib.sha256(pub_byt).hexdigest()


tr={}
tr['version'] = 1.0

tr['inputs']=[]
tr['outputs']=[]


output={'output_no': 0, 'amount':100, 'pubkey_scr':pubh}
tr['outputs'].append(output)


output={'output_no': 1, 'amount':10, 'pubkey_scr':pubh }
tr['outputs'].append(output)

tr['locktime']=0

hash1 = hashlib.sha256( str(tr).encode() ).hexdigest()
hash2= hashlib.sha256( hash1.encode() ).hexdigest()

print(hash1)
print(hash2)
txid = hash2
blocks = {txid: str(tr) }

print(blocks)
#first transaction done

tr={}
tr['version'] = 1.0
tr['inputs']=[]
tr['outputs']=[]

output={'output_no': 0, 'amount':20, 'pubkey_scr':pubh}
tr['outputs'].append(output)

tr['locktime']=0


hash1 = hashlib.sha256( str(tr).encode() ).hexdigest()
hash2= hashlib.sha256( hash1.encode() ).hexdigest()
txid=hash2

blocks[txid]=str(tr)
#second done


#now for backup 

tr={}
tr['version'] = 1.0
tr['inputs']=[]
tr['outputs']=[]

output={'output_no': 0, 'amount':120, 'pubkey_scr':'8a9898e05379d5516e6e315518c911e36e93b82e19c2d95f9df24d6c2d5bcb72'}
tr['outputs'].append(output)

output={'output_no': 1, 'amount':20, 'pubkey_scr':'8a9898e05379d5516e6e315518c911e36e93b82e19c2d95f9df24d6c2d5bcb72'}
tr['outputs'].append(output)

tr['locktime']=0

h1= hashlib.sha256( str(tr).encode() ).hexdigest()
txid = hashlib.sha256( h1.encode()  ).hexdigest()

blocks[txid]=str(tr)

#thrd done

#fourth start


tr={}
tr['version'] = 1.0
tr['inputs']=[]
tr['outputs']=[]

output={'output_no': 0, 'amount':200, 'pubkey_scr':'8a9898e05379d5516e6e315518c911e36e93b82e19c2d95f9df24d6c2d5bcb72'}
tr['outputs'].append(output)


tr['locktime']=0

h1= hashlib.sha256( str(tr).encode() ).hexdigest()
txid = hashlib.sha256( h1.encode()  ).hexdigest()

blocks[txid]=str(tr)


#fourth end

#fifth ah ima leave

#print(pubh)

print('blocks is ' )
print(blocks)

blockheader = {'prevbh': '0', 'merkle': 'tbd', 'nonce': 0}


txids = list(blocks.keys())
hashes=[]




for i in range(1,len(txids),2):
	s=hashlib.sha256( (txids[i]+txids[i-1]).encode() ).hexdigest()
	hashes.append(s)

print(hashes)
for i in range(1,len(hashes),2):
	s=hashlib.sha256( (txids[i]+txids[i-1]).encode() ).hexdigest()
	print('%isnideT% : ',s)
	blockheader['merkle']=s



print('block header is ',blockheader)

string_bh = str(blockheader)

#print(string_bh)

q=string_bh.encode()
print(q)

for i in range(1000000000):
	blockheader['nonce']=i
	bh = str(blockheader)
	x= bh.encode()
	x = hashlib.sha256(x).hexdigest()
	print(x)
	if(int(x[:4],base=16) ==0):
		blockheader['nonce']=i
		print('SUCCESS')
		break


print('nonce is ', blockheader['nonce'])
x = hashlib.sha256(str(blockheader).encode()).hexdigest()
print('blockheader hash is ',x)

blocktoentry = []
blocktoentry.append(blockheader)
blocktoentry.append(blocks)

#contents


with open('blocks.txt',mode='w') as file:
	file.write(str(blocktoentry)+'\n')
#genesis block, its a list
#first element contains block header
#second element cointains transactions


#end of program
