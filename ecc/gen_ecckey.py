from ecdsa import SigningKey
from ecdsa import BadSignatureError

import hashlib

sk = SigningKey.generate()
vk = sk.verifying_key
with open("ecc_private.pem", "wb") as f:
    f.write(sk.to_pem())
with open("ecc_public.pem", "wb") as f:
    f.write(vk.to_pem())
print(str(sk.verifying_key) )
print(str(sk.verifying_key) )


print("new public key hash is ",hashlib.sha256(vk.to_string()).hexdigest() )

#end



