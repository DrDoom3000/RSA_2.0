import random
from sympy import mod_inverse, nextprime
import math


def get_position_mapping(pos, mapping_seed):
    r = random.Random(mapping_seed + pos)
    return r.sample(range(256), 10)

def encrypt_digit_layer(numeric_string, mapping_seed, unicode_table):
    result = []
    for pos, digit_char in enumerate(numeric_string):
        mapping = get_position_mapping(pos, mapping_seed)
        byte_val = mapping[int(digit_char)]
        result.append(unicode_table[byte_val])
    return ''.join(result)

def decrypt_digit_layer(cipher_unicode, mapping_seed, unicode_table):
    result = []
    for pos, char in enumerate(cipher_unicode):
        byte_val = unicode_table.index(char)
        mapping = get_position_mapping(pos, mapping_seed)
        result.append(str(mapping.index(byte_val)))
    return ''.join(result)


def split_and_shuffle(number_str):
    num_blocks = len(number_str) // 15 
    blocks_15 = [number_str[i*15:(i+1)*15] for i in range(num_blocks)]
    shuffled_blocks = []
    perms = []

    for block in blocks_15:
        mini_blocks = [block[i*3:(i+1)*3] for i in range(5)]
        indices = list(range(5))
        random.shuffle(indices)
        shuffled = ''.join([mini_blocks[i] for i in indices])
        perms.append(''.join(str(i) for i in indices))
        shuffled_blocks.append(shuffled)

    return shuffled_blocks, perms

def unshuffle(block, perm_code):
    if len(block) != 15 or len(perm_code) != 5:
        raise ValueError("Invalid Length")
    
    mini_blocks = [block[i*3:(i+1)*3] for i in range(5)]
    permutation = [int(ch) for ch in perm_code]
    
    inverse_perm = [0] * 5
    for i, p in enumerate(permutation):
        inverse_perm[p] = i

    return ''.join([mini_blocks[inverse_perm[i]] for i in range(5)])


def encrypt_block(P, A, F, G, H, BE, n):
    X = P * A
    Y = pow(X, BE, n)
    return (Y * pow(F, 2, n) + pow(G, H, n)) % n


input_number = input("Please enter a 75 digit number: ")

if len(input_number) != 75 or not input_number.isdigit():
    print("Invalid. Please enter exactly 75 digits.")
    exit()

shuffled_blocks, permutations = split_and_shuffle(input_number)

E = 17
B = 5
BE = B * E

while True:
    p = nextprime(10**30 + random.randint(9, 10))
    q = nextprime(10**30 + random.randint(9, 10))
    n = p * q
    phi_n = (p - 1) * (q - 1)
    if math.gcd(BE, phi_n) == 1:
        break

C = mod_inverse(BE, phi_n)

A = random.randint(10**18, n // 10**20 - 1)
F = random.randint(10**18, 10**21)
G = random.randint(10**20, 10**23)
H = random.randint(2, 5)

while math.gcd(A, n) != 1:
    A = random.randint(10**18, n // 10**20 - 1)

while math.gcd(F, n) != 1:
    F = random.randint(10**18, 10**21)

cipher_length = len(str(n))
print(f"Modulus n has {cipher_length} Digits; The numbers will be filled to this length.")

encrypted_blocks = []
for block, perm in zip(shuffled_blocks, permutations):
    P = int(block)
    cipher = encrypt_block(P, A, F, G, H, BE, n)
    encrypted_blocks.append(str(cipher).zfill(cipher_length) + perm)

final_digit_ciphertext = ''.join(encrypted_blocks)

mapping_seed = 12345
unicode_seed = 54321
r = random.Random(unicode_seed)
unicode_table = [chr(i) for i in range(32, 32+256)]
r.shuffle(unicode_table)

final_unicode_ciphertext = encrypt_digit_layer(final_digit_ciphertext, mapping_seed, unicode_table)

print("\nVerschlüsselte Zeichenfolge:")
print(final_unicode_ciphertext)
print("\nA:", A)
print("\nB:", B)
print("\nC:", C)
print("\nE:", E)
print("\nF:", F)
print("\nG:", G)
print("\nH:", H)
print("\nBE:", BE)
print("\nn:", n)
