import numpy as np


def add_to_file(path_to: str, data: list) -> bool:
    try:
        with open(path_to, 'rb+') as f:
            f.seek(0, 2)  # перемещение курсора в конец файла
            for d in data:
                f.write(d)  # собственно, запись
            return True
    except FileNotFoundError:
        print("Невозможно открыть файл")
        return False


def save_in_file(path_to: str, data: bytes) -> bool:
    try:
        with open(path_to, 'wb') as f:
            f.write(data)
            return True
    except FileNotFoundError:
        print("Невозможно открыть файл")
        return False


def save_list_in_file(path_to: str, data_l: list) -> bool:
    try:
        with open(path_to, 'wb') as f:
            for e in data_l:
                f.write(e)
            return True
    except FileNotFoundError:
        print("Невозможно открыть файл")
        return False


def entropy(labels: bytearray) -> float:
    """ Вычисление энтропии вектора из 0-1 """
    n_labels = len(labels)

    if n_labels <= 1:
        return 0

    counts = np.bincount(labels)
    probs = counts[np.nonzero(counts)] / n_labels
    n_classes = len(probs)

    if n_classes <= 1:
        return 0
    return - np.sum(probs * np.log(probs)) / np.log(n_classes)


def xor_lists(l1: list, l2: list) -> list | None:
    if len(l1) != len(l2):
        return None
    temp: list = list()
    for i in range(4):
        temp.append(np.uint16(l1[i] ^ l2[i]))
    return temp


def collect_int_number(l_of_np_numbers: list) -> int:
    """ Из списка целых чисел (в моём случае, беззнаковых np.uint16) собирается целое длинное число. """
    result = ""
    for integer in l_of_np_numbers:
        if isinstance(integer, np.uint16):
            result += to_bits(integer, 16)
    result = int(result, base=2)
    return result


def cut_uint64_num_into_list_uint16(value: np.uint64) -> list:
    """ По сути эта функция для разбиения uint64 на равное количество бит для функции xor_lists (очередной костыль) """
    result: list = list()
    binary: str = to_bits(value, 64)
    for i in range(4):
        result.append(np.uint16(int((binary[(16 * i):(16 * (i + 1))]), base=2)))
    return result


def cyclic_shift(value, width: int, shift: int):
    """ Побитовый циклический сдвиг числа.
        value < 0 - циклический сдвиг вправо.
        value > 0 - циклический сдвиг влево"""
    shift %= width
    if shift == 0:
        return value
    # Преобразование числа в его битовое представление
    result = to_bits(value, width)
    # Циклический сдвиг (с помощью слайсов) и преобразование из строки в тип value
    result = type(value)(int(result[shift:] + result[:shift], base=2))
    return result


def cut_bits_of_number(value, width_old_big: int, width_new_less: int) -> int:
    """ Функция создана с целью преобразования из длинных
        беззнаковых целых чисел в более короткие беззнаковые
        целые числа """
    # Преобразование числа в его бинарное представление, начиная с младшего разряда
    binary = '{:0{width}b}'.format(value, width=width_old_big)[::-1]
    result: int = 0
    i = 0
    while i < len(binary) and i < width_new_less:
        result += int(binary[i]) * (2 ** i)
        i += 1
    return result


def to_bits(value, width: int) -> str:
    """ Преобразование числа в его битовое представление, начиная со старшего разряда """
    return '{:0{width}b}'.format(value, width=width)[::1]
