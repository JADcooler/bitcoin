with open('UTXOs.txt') as f:
	s = f.read()

with open('UTXO.tmp','w') as f:
	f.write(s)
