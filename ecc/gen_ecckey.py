from ecdsa import SigningKey
from ecdsa import BadSignatureError


sk = SigningKey.generate()
vk = sk.verifying_key
with open("ecc_private.pem", "wb") as f:
    f.write(sk.to_pem())
with open("ecc_public.pem", "wb") as f:
    f.write(vk.to_pem())
print(str(sk.verifying_key) )
print(str(sk.verifying_key) )
#end



