with open('UTXOs.txt') as f:
	s = f.read()

with open('UTXO.tmp','w') as f:
	f.write(s)

a=  {'0':'0'}

with open('../mempool.txt','w') as f:
	f.write(str(a))
