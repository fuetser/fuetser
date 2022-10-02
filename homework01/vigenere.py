from string import ascii_lowercase as lower


table = [[lower[(lower.index(char) + shift) % 26] for char in lower] for shift in range(26)]


def encrypt_vigenere(plaintext: str, keyword: str, encode: bool = True) -> str:
    ciphertext = []
    for index, char in enumerate(plaintext.lower()):
        if char.isalpha():
            keyword_char = keyword[index % len(keyword)].lower()
            keyword_char_index = lower.index(keyword_char)
            if encode:
                char = table[keyword_char_index][lower.index(char)]
            else:
                table_char_index = table[keyword_char_index].index(char)
                char = lower[table_char_index]
            if plaintext[index].isupper():
                char = char.upper()
        ciphertext.append(char)
    return "".join(ciphertext)


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    return encrypt_vigenere(ciphertext, keyword, encode=False)
