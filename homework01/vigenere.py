from caesar import decrypt_caesar, encrypt_caesar


def encrypt_vigenere(plaintext: str, keyword: str, encode: bool = True) -> str:
    ciphertext = []
    for index, char in enumerate(plaintext.lower()):
        shift = ord(keyword[index % len(keyword)].lower()) - 97
        if encode:
            ciphertext.append(encrypt_caesar(char, shift))
        else:
            ciphertext.append(decrypt_caesar(char, shift))
        if plaintext[index].isupper():
            ciphertext[-1] = ciphertext[-1].upper()
    return "".join(ciphertext)


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    return encrypt_vigenere(ciphertext, keyword, encode=False)
