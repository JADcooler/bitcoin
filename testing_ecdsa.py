from ecdsa import SigningKey
from ecdsa import BadSignatureError, VerifyingKey


vk = VerifyingKey.from_pem(open("ecc_public.pem").read())
print(vk)

with open("ecc_private.pem") as f:
    sk = SigningKey.from_pem(f.read())

message = "txid+outno"
# "txid+outix| signature"

x=sk.sign(message.encode())



print('type of x ',type(x.decode('ISO-8859-1')), x.decode('ISO-8859-1'))

#end of garbage



with open('signature.txt',mode='w') as file:
	file.write(x.decode('ISO-8859-1'))
try:
	vk.verify(x, message.encode())
	print("GOOD SIGNATURE")
except BadSignatureError:
	print("BAD SIGNATURE")



#start of checking
signature = sk.sign(message.encode())
list= [message,signature.decode('ISO-8859-1')]

with open('testing.txt', mode='w') as file:
	file.write(str(list))

with open('testing.txt', mode='r') as file:
	stringlist = file.read()

print(stringlist)
import ast

list =  ast.literal_eval(stringlist)

print(list)


#listext = ast.literal_eval(stringlist)
#print(listext)

#end
