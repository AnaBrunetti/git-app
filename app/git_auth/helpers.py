from cryptography.fernet import Fernet

# key generation
# key = Fernet.generate_key()
# print("###################")
# print(key)
   
###################

# using the generated key
key = "753853AD8AAE712874F6BB640ED5DDEA34C861EE15C5C947F481DD7F1953A1F4"
fernet = Fernet(key)
print("###################")
print(fernet)

# opening the original file to encrypt
     
# encrypting the file
token = "teste token encrypt"
encrypted = fernet.encrypt(token.encode())
print("###################")
print(encrypted)
    
###################
 
# decrypting the file
# key2 = "eijfiajfiojiohgsfidhgsiodfhgiosdfjoigjsdi12="
# fernet2 = Fernet(key2)
# decrypted = fernet2.decrypt(encrypted)
decrypted = fernet.decrypt(encrypted)
print("###################")
print(decrypted.decode())