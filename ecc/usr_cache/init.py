# the following program is used to iniitialize user cache
# place where UTXOs are stored
# list where block hashes are keys, UTXOs txids are values

asd = {0: [0,0,0] }

with open('balances.txt', mode ='w') as f:
	f.write(str(asd))

with open('balances.txt', mode ='r') as f:
	qwe = f.read()

import ast

qwe = ast.literal_eval(qwe)

print(qwe,type(qwe), qwe[0])

#end

