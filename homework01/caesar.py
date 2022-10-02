from string import ascii_lowercase as lower
from string import ascii_uppercase as upper
import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            if char.islower():
                char = lower[(lower.index(char) + shift) % 26]
            else:
                char = upper[(upper.index(char) + shift) % 26]
        ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    return encrypt_caesar(ciphertext, -shift)


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    best_shift = 0
    for shift in range(26):
        decrypted_msg = decrypt_caesar(ciphertext, shift)
        if decrypted_msg in dictionary:
            best_shift = shift
    return best_shift
