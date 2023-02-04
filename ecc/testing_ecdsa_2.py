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


print('starting testing')
str = 'garbage'
print('plain text',str)

sign = sk.sign(str.encode())
signStr = sign.decode('ISO-8859-1')

print('signature in string',signStr)

pubStr = vk.to_string().decode('ISO-8859-1')
print('publickey in string',pubStr)


newPub = VerifyingKey.from_string(pubStr.encode('ISO-8859-1'))
x = newPub.verify(sign,str.encode()) 
print(x)


