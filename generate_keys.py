import rsa

pub, pri = rsa.newkeys(512)
with open('public_key.pem',mode='w') as file:
	pub_byt = pub.save_pkcs1()
	pub_str = pub_byt.decode('UTF-8')
	file.write(pub_str)
with open('private_key.pem',mode='w') as file:
	pri_byt = pri.save_pkcs1()
	pri_str = pri_byt.decode('UTF-8')
	file.write(pri_str)
#end


