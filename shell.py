import tasks


def hibbard(k: int) -> int:
    '''Формула Хиббарда для сортировки Шелла.

    > k - произвольное число, иначе - шаг сортировки

    Возвращает значение, вычисленное по формуле Хиббарда.
    '''
    return 2 ** k - 1


def compare(element1: str | int, element2: str | int, reverse: bool) -> bool:
    '''Сравнение двух элементов с учетом параметра reverse

    > element1 - первый элемент типа str | int,
    > element2 - второй элемент типа str | int,
    > reverse - булево значение, определяющее, происходит ли
    сравнение для сортировки по возрастанию или по убыванию.

    Возвращает булево значение, обрабатываемое в алгоритме сортировки.
    True - элементы необходимо поменять местами в массиве,
    False - ничего менять местами в массиве не нужно.
    '''
    return element1 < element2 if reverse else element1 > element2


def sort(obj: tasks.Tasks, keys: tuple,
         k: int = 4, reverse1: bool = False,
         reverse2: bool = False) -> None:
    '''Сортировка Шелла.

    > obj - объект класса Tasks, obj.list необходимо отсортировать
    > keys - кортеж (keys[0] - первичный ключ сортировки, keys[1] - вторичный)
    > (опционально) k - номер текущего шага (4 - по умолчанию),
    значение, с помощью hibbard(k) задающее расстояние сравниваемых элементов.
    > (опционально) reverse1 - булево значение, означающее необходимость
    сортировки по убыванию по первичному ключу: (False - по умолчанию)
    > (опционально) reverse2 - булево значение, означающее необходимость
    сортировки по убыванию по вторичному ключу: (False - по умолчанию)

    Возвращает рекурсивный вызов этой же функции с уменьшением номера шага
    или ничего, если сортировка окончена.
    '''

    if k == 0:
        return

    gap = hibbard(k)
    if gap >= len(obj.list):
        return sort(obj, keys, k-1, reverse1, reverse2)

    k1, k2 = keys

    for index1 in range(gap, len(obj.list)):
        temp = obj.list[index1]
        index2 = index1

        while index2 >= gap:
            if obj.list[index2 - gap][k1] == temp[k1]:
                if compare(obj.list[index2 - gap][k2], temp[k2], reverse2):
                    obj.list[index2] = obj.list[index2 - gap]
                    index2 -= gap
                else:
                    break
            elif compare(obj.list[index2 - gap][k1], temp[k1], reverse1):
                obj.list[index2] = obj.list[index2 - gap]
                index2 -= gap
            else:
                break

        obj.list[index2] = temp

    return sort(obj, keys, k-1, reverse1, reverse2)
