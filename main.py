import random
from sympy import mod_inverse, nextprime

def split_and_shuffle(number_str):
    blocks_20 = [number_str[i*20:(i+1)*20] for i in range(5)]
    shuffled_blocks = []
    perms = []

    for block in blocks_20:
        mini_blocks = [block[i*4:(i+1)*4] for i in range(5)]
        indices = list(range(5))
        random.shuffle(indices)
        shuffled = ''.join([mini_blocks[i] for i in indices])
        perm_code = ''.join(str(i) for i in indices)
        shuffled_blocks.append(shuffled)
        perms.append(perm_code)

    return shuffled_blocks, perms

def unshuffle(block, perm_code):
    if len(block) != 20 or len(perm_code) != 5:
        raise ValueError("Block or permutation code has an invalid length.")
    
    mini_blocks = [block[i*4:(i+1)*4] for i in range(5)]
    permutation = [int(ch) for ch in perm_code]
    if sorted(permutation) != list(range(5)):
        raise ValueError(f"Invalid permutation code: {perm_code}")

    inverse_perm = [0] * 5
    for i, p in enumerate(permutation):
        inverse_perm[p] = i

    original_order = [mini_blocks[inverse_perm[i]] for i in range(5)]
    return ''.join(original_order)

def encrypt_block(P, A, F, G, H, BE, n):
    X = P * A
    Y = pow(X, BE, n)
    cipher = (Y * pow(F, 2, n) + pow(G, H, n)) % n
    return cipher

def decrypt_block(cipher, A, F, G, H, C, n):
    inverse_F2 = mod_inverse(pow(F, 2, n), n)
    Y = (cipher - pow(G, H, n)) * inverse_F2 % n
    X = pow(Y, C, n)
    P_recovered = X // A
    return P_recovered

input_number = input("Please enter a 100 digit number:")

if len(input_number) != 100 or not input_number.isdigit():
    print("Invalid entry; Please enter exactly 100 digits.")
    exit()
shuffled_blocks, permutations = split_and_shuffle(input_number)

p = nextprime(10**30 + random.randint(9, 10))
q = nextprime(10**30 + random.randint(9, 10))
n = p * q
phi_n = (p - 1) * (q - 1)

E = 17
B = 5
BE = B * E
C = mod_inverse(BE, phi_n)
A = random.randint(10**20, 10**23)
F = random.randint(10**20, 10**23)
G = random.randint(10**20, 10**23)
H = random.randint(2, 5)

cipher_length = len(str(n))
print(f"Modulus n has {cipher_length} Digits; The numbers will be filled to this length")

encrypted_blocks = []
for block, perm in zip(shuffled_blocks, permutations):
    P = int(block)
    cipher = encrypt_block(P, A, F, G, H, BE, n)
    cipher_str = str(cipher).zfill(cipher_length)
    combined = cipher_str + perm
    encrypted_blocks.append(combined)

final_ciphertext = ''.join(encrypted_blocks)
print("\nEncrypted number: ")
print(final_ciphertext)

block_size = cipher_length + 5
split_ciphers = [final_ciphertext[i*block_size:(i+1)*block_size] for i in range(5)]

decrypted_blocks = []
for cipher_block in split_ciphers:
    cipher_str = cipher_block[:cipher_length]
    perm_code = cipher_block[cipher_length:]
    cipher = int(cipher_str)
    P_recovered = decrypt_block(cipher, A, F, G, H, C, n)
    recovered_str = str(P_recovered).zfill(20)
    original_block = unshuffle(recovered_str, perm_code)
    decrypted_blocks.append(original_block)

reconstructed_number = ''.join(decrypted_blocks)

print("\nRebuilt 100digit number: ")
print(reconstructed_number)
