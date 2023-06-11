import hashlib
text = 'Hello World'
hash_object = hashlib.sha256(f"{text}")
hex_dig = hash_object.hexdigest()

print(hex_dig)
print(hash_object )