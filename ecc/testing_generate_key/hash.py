from ecdsa import VerifyingKey

with open('ecc_public.pem',mode='r') as file:
	s = file.read()
	vk = VerifyingKey.from_pem(s)


#print(vk)
#print(vk.to_string())


import hashlib
print('hash is ')
print(hashlib.sha256(vk.to_string()).hexdigest() )
#end


