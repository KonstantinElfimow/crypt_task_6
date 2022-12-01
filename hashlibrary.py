import numpy as np
from my_utils import cyclic_shift, xor_lists, cut_bits_of_number, collect_int_number, cut_uint64_num_into_list_uint16

_ROUNDS: int = 10  # количество проходов по сети Фейстеля


def parse_message_by_blocks(message: bytes) -> list:
    """ Читаем сообщение по 8 байт, разбивая их на блоки по два байта """
    result: list = list()
    count = 0
    while count < len(message):
        m: list = list()
        for _ in range(4):
            m.append(np.uint16(int.from_bytes(message[count:(count + 2)], byteorder="little", signed=False)))
            count += 2
        result.append(m)
    return result


def read_file_message_by_blocks(path_from: str) -> list:
    """ Читаем сообщение по 8 байт, разбивая их на блоки по два байта """
    try:
        with open(path_from, 'rb') as rfile:
            message: list = list()
            while True:
                # Проверка конца файла
                file_eof: bytes = rfile.read(1)
                rfile.seek(rfile.tell() - 1)
                if file_eof == b'':
                    break

                # Блок состоит из 4 частей
                m: list = list()
                for _ in range(4):
                    m.append(np.uint16(int.from_bytes(rfile.read(2), byteorder="little", signed=False)))
                message.append(m)
            return message
    except FileNotFoundError:
        print("Невозможно открыть файл")


def _f1(m0: np.uint16, m1: np.uint16) -> np.uint16:
    """ (m0 <<< 4) + (m1 >> 2) """
    return (cyclic_shift(m0, 16, 4)) + (cyclic_shift(m1, 16, -2))


def _f2(m2: np.uint16, m3: np.uint16) -> np.uint16:
    """ (m2 <<< 7) ^ ~m3 """
    return cyclic_shift(m2, 16, 7) ^ (~m3)


def _Ek(message: list, round_keys: list) -> list:
    #  ...выполняем преобразование по раундам (сжимающая функция) в соответствии с сетью Фейстеля из 1 задания
    cipher: list = [m for m in message]
    for i in range(_ROUNDS):
        cipher[0] = message[2] ^ (~round_keys[i])
        cipher[1] = _f1(message[0] ^ round_keys[i], message[1]) ^ message[3]
        cipher[2] = _f2(cipher[0], cipher[1]) ^ message[1]
        cipher[3] = message[0] ^ round_keys[i]
        message = np.copy(cipher)
    return cipher


def _create_round_keys(iv: np.uint64):
    round_keys: list = list()  # Создаём раундовые ключи по сети Фейстеля из 1 задания
    for index in range(_ROUNDS):
        temp = cyclic_shift(iv, 64, -(index + 1)) ^ iv
        round_keys.append(np.uint16(cut_bits_of_number(temp, 64, 16)))
    return round_keys


def hash(IV: np.uint64, message: bytes = None, path_from: str = None) -> np.uint64:
    if (message is path_from) and (path_from is None or path_from is not None):
        raise ValueError('Передайте message или path_from!')

    if message:
        message: list = parse_message_by_blocks(message)

    elif path_from:
        message: list = read_file_message_by_blocks(path_from)

    # h0, h1, ..., hi - промежуточные хеши; h0 равен вектору инициализации
    h: list = cut_uint64_num_into_list_uint16(IV)
    for m in message:

        # Создаём раундовые ключи
        secret_round_key = np.uint64(collect_int_number(h))
        round_keys: list = _create_round_keys(secret_round_key)

        #  Хеширование в соответствии с вариантом ЗАДАНИЯ!
        h = xor_lists(xor_lists(_Ek(xor_lists(m, h), round_keys), h), m)

    # Итоговый кеш
    result = np.uint64(collect_int_number(h))
    return result
