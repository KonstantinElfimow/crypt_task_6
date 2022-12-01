import random
import my_utils
from hashlibrary import hash
import numpy as np
from Crypto.Protocol.KDF import scrypt

IV: np.uint64 = np.uint64(random.randint(1, 18446744073709551616))


def task() -> float:
    password: bytes = b'-give me your password. -password?.. -yes, your password'

    h1 = hash(np.uint64(IV + 1), message=password)
    h2 = hash(IV, message=password)

    salt: str = str(IV)

    """ пароль (строка) — секретная фраза-пароль, из которой создаются ключи.
    
        соль (строка) — строка, используемая для лучшей защиты от атак по словарю. 
        Это значение не нужно держать в секрете, но оно должно выбираться случайным образом для каждого вывода.
        Рекомендуется иметь длину не менее 16 байт.
        
        key_len (integer) — длина в байтах каждого производного ключа.
        
        N (целое число) - параметр стоимости процессора/памяти. Оно должно быть степенью 2 и меньше 232.
        
        r (целое число) - параметр размера блока.
        
        p (целое число) - Параметр распараллеливания. Оно должно быть не больше, чем (232−1)/(4r).
        
        num_keys (целое число) — количество ключей для получения. Каждый ключ имеет длину key_len байт. 
        По умолчанию генерируется только 1 ключ. 
        Максимальная совокупная длина всех ключей составляет (232−1)∗32 (то есть 128 ТБ)."""
    key_1 = int.from_bytes(scrypt(str(h1), salt, 16, N=2 ** 14, r=8, p=1), byteorder='little', signed=False)
    key_2 = int.from_bytes(scrypt(str(h2), salt, 16, N=2 ** 14, r=8, p=1), byteorder='little', signed=False)

    print(key_1, key_2)

    width: int = 128
    key_1 = my_utils.to_bits(key_1, width)
    key_2 = my_utils.to_bits(key_2, width)

    coincidence = 0
    for i in range(width):
        if key_1[i] == key_2[i]:
            coincidence += 1

    return coincidence / width


def main():
    print(task())


if __name__ == '__main__':
    main()
