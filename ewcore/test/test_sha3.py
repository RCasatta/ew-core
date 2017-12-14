import sys
import sha3

print(sys.version_info)

s = sha3.sha3_512()
data_ = b"data"
s.update(data_)
hexdigest = s.hexdigest()
print('sha3_512')
print(hexdigest)
print()

assert ('ceca4daf960c2bbfb4a9edaca9b8137a801b65bae377e0f534ef9141c8684c0fedc1768d1afde9766572846c42b935f61177eaf97d355fa8dc2bca3fecfa754d' == hexdigest)

s = sha3.keccak_512()
s.update(data_)
hexdigest = s.hexdigest()
print("keccak_512")
print(hexdigest)
print()

assert ('1065aceeded3a5e4412e2187e919bffeadf815f5bd73d37fe00d384fe29f55f08462fdabe1007b993ce5b8119630e7db93101d9425d6e352e22ffe3dcb56b825' == hexdigest)

fd = open("../../report_wolfway.pdf", "rb")
s1 = sha3.sha3_512()
s2 = sha3.keccak_512()
chunk = True
while chunk != b'':
    chunk = fd.read(2 ** 20)
    s1.update(chunk)
    s2.update(chunk)

print("s1")
print(s1.hexdigest())
print()

print("s2")
print(s2.hexdigest())
print()
