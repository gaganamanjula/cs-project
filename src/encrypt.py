from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
import base64
from urllib.parse import quote

# The public key string
public_key_str = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4dGQ7bQK8LgILOdLsYzf
ZjkEAoQeVC/aqyc8GC6RX7dq/KvRAQAWPvkam8VQv4GK5T4ogklEKEvj5ISBamdD
Nq1n52TpxQwI2EqxSk7I9fKPKhRt4F8+2yETlYvye+2s6NeWJim0KBtOVrk0gWvE
Dgd6WOqJl/yt5WBISvILNyVg1qAAM8JeX6dRPosahRVDjA52G2X+Tip84wqwyRpU
lq2ybzcLh3zyhCitBOebiRWDQfG26EH9lTlJhll+p/Dg8vAXxJLIJ4SNLcqgFeZe
4OfHLgdzMvxXZJnPp/VgmkcpUdRotazKZumj6dBPcXI/XID4Z4Z3OM1KrZPJNdUh
xwIDAQAB
-----END PUBLIC KEY-----
"""

# Convert the key string to an object

# Number to be encrypted
number_to_encrypt = 454


def encrypt_data(public_key_str, number):
  pub_key = serialization.load_pem_public_key(public_key_str.encode(),
                                              backend=default_backend())
  # Encrypt the number using RSA-OAEP with SHA-256 hash
  encrypted = pub_key.encrypt(
      bytes(str(number), 'utf-8'),
      padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                   algorithm=hashes.SHA256(),
                   label=None))
  # Encode the encrypted data in Base64
  encrypted_base64 = base64.b64encode(encrypted).decode()
  # print(len(encrypted_base64))
  # Display the encrypted data in Base64
  #print("Encrypted (Base64):", encrypted_base64)
  url_encoded_string = quote(encrypted_base64, safe='')
  # print("ciper_text", url_encoded_string, len(url_encoded_string))
  return url_encoded_string

json = {"kty":"RSA","e":"AQAB","use":"enc","n":"wVFUxZoVNrnuMk1q6Tc4JXmfaEWqQLgE031UK-TlA7NMOoZ3m9oU0i1eU7J0JqdWEwDjLLWwQb5eGeKC6Vw-uUzu_Oiuu0g3owt7R1I1IJy_Yby3rFM23oNCagrLqQJWwuFbMGlaBKMZhI0ksISmZ0nsIGCnwkc3IHKv5iVFNU8VnlRU_LJSWUbpByDPxInC2zWxxq-L4Uma1GfMleOMFaTg6ePa7rTh9VjcZBAsnalBdvANccYaZU4uWnhbz5E9KriMX9Ua-m3z7Ox_8TmTAmRu4GwYI3D0SCesO-c3fnBmYNKSgbsrRbhOSmB3szY86PsMrQshJctfZpcSntFO3w"}

def gen_public_key(json):
  # Constructing the RSA public key
  modulus = int.from_bytes(base64.urlsafe_b64decode(json['n'] + '=='), 'big')
  exponent = int.from_bytes(base64.urlsafe_b64decode(json['e'] + '=='), 'big')
  public_numbers = rsa.RSAPublicNumbers(exponent, modulus)
  public_key = public_numbers.public_key(default_backend())

  # Exporting the public key in PEM format
  pem = public_key.public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()

  return pem

print(gen_public_key(json))
