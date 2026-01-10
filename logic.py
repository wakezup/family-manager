import interface
import shell
import tasks


class YearError(Exception):
    '''Класс исключения.

    Возникает в случае, когда год принимает отрицательное значение.
    '''
    pass


class DateError(Exception):
    '''Класс исключения.

    Возникает в случае, когда дата имеет некорректный формат.
    '''
    pass


class TimeError(Exception):
    '''Класс исключения.

    Возникает в случае, когда время имеет некорректный формат.
    '''
    pass


class StatusError(Exception):
    '''Класс исключения.

    Возникает в случае, когда статус является некорректным.
    '''
    pass


class ItemsError(Exception):
    '''Класс исключения.

    Возникает в случае, когда не хватает данных о задаче.
    '''
    pass


class LevelError(Exception):
    '''Класс исключения.

    Возникает в случае, когда из уровня программы происходит попытка
    использования команды не предназначенной для этого уровня.
    '''
    pass


class PathError(Exception):
    '''Класс исключения.

    Возникает в случае, когда в пути содержатся недопустимые символы
    или расширением файла является не ".txt".
    '''
    pass


def max_space(obj: tasks.Tasks) -> list:
    '''Формирование данных о максимальной длине значений всех атрибутов.

    obj -> ссылка на объект

    Возвращает список с числовыми значениями максимальных длин.
    '''
    # Такие значения соответствуют либо длине заголовков,
    # либо максимальной длине допустимых значений, они являются минимальными.
    max_space = [2, 16, 16, 11, 6, 10]

    for task in obj.list:
        # При выводе задач дата и время (получения/выполнения) объединяются
        # в одной ячейке, из этого исходят несоответствия индексов у max_space
        # и task.
        max_space[0] = max(max_space[0], len(str(task[0])))
        max_space[3] = max(max_space[3], len(task[5]))
        max_space[4] = max(max_space[4], len(task[6]))

    return max_space


def string(max_space: list, labels: list) -> str:
    '''Формирование строки для вывода информации о задаче.

    > max_space - список с максимальной длиной значений всех атрибутов
    > labels - значения атрибутов конкретной задачи

    Возвращает сформированную строку, содержащую информацию о задаче.
    '''
    string = ''
    for item in range(len(labels)):
        # Определение количества свободного места по бокам от строки
        # со значением атрибута в ячейке для его отцентровки.
        right_space = (max_space[item] - len(labels[item])) // 2
        left_space = max_space[item] - len(labels[item]) - right_space
        if item != 5:
            string += " " * right_space + labels[item] + " " * left_space + "|"
        else:
            # Отцентровка в ячейках 'Статус' происходит только для заголовка
            if labels[item] != "Статус":
                string += labels[item]
            else:
                string += " " * right_space + labels[item] + " " * left_space

    return string


def condition(item: int, rvalue: str | int,
              lvalue: str | int, parse: bool) -> bool:
    '''Формирование условия для поиска по объекту класса Tasks.

    > item - индекс атрибута задачи
    > rvalue - правое значение для сравнения
    > lvalue - левое значение для сравнения
    > parse - логическая переменная, определяющая, как именно
    будет сформировано условие для поиска, подается из функции
    tasks.Tasks.get().

    Возвращает булево значение (True/False) являющееся результатом
    проверки соответствующего условия.
    '''
    match item:
        # Проверка дат ( 1 - дата получения, 3 - дата выполнения )
        case 1 | 3:
            if parse:
                return rvalue == lvalue
            else:
                return rvalue >= lvalue
        # Особое условие для статуса объясняется необходимостью,
        # найти все задачи, находящиеся на исполнении (В процессе, Получена)
        # в function_3()
        case 7:
            return rvalue in lvalue
        case _:
            return rvalue == lvalue


def leap_year(year: int) -> bool:
    '''Определение того, является ли год високосным.

    > year - значение года

    Возвращается булево значение (True/False).
    '''
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def date_mask(date: str, user_input: bool = False) -> None:
    '''Проверка даты на корректность.

    > date - дата, которую необходимо проверить
    > user_input - булево значение, определяющее
    вызвана ли эта функция в последствии ввода пользователем
    или была вызвана с технической стороны.

    Ничего не возвращает, а только вызывает ошибку, если дата некорректна.
    '''
    try:
        # Так как для эффективного сравнения дат в объектах они хранятся
        # в формате ГГГГ.ММ.ДД, эта проверка должна учитывать и этот вариант,
        # так как она вызывается при форматировании даты.
        if len(date[: date.find(".")]) == 4 and not user_input:
            year = date[: date.find(".")]
            day = date[date.rfind(".") + 1:]
        else:
            day = date[: date.find(".")]
            year = date[date.rfind(".") + 1:]

        month = date[date.find(".") + 1: date.rfind(".")]

        if len(day) == 2:
            day = int(day)
        else:
            raise DateError(date)

        if len(year) == 4:
            year = int(year)
        else:
            raise DateError(date)

        if len(month) == 2:
            month = int(month)
        else:
            raise DateError(date)

        if 0 <= year < 10000:
            if 0 <= month < 13:
                days_in_months = [31, 28 + leap_year(year), 31, 30,
                                  31, 30, 31, 31,
                                  30, 31, 30, 31]

                if not (0 <= day <= days_in_months[month - 1]):
                    raise DateError(date)
            else:
                raise DateError(date)
        else:
            raise DateError(date)

    except ValueError:
        raise DateError(date)


def time_mask(time: str) -> None:
    '''Проверка времени на корректность.

    > time - время, которое необходимо проверить

    Ничего не возвращает, а только вызывает ошибку, если время некорректно.
    '''
    hours = str(time[: time.find(":")])
    minutes = str(time[time.find(":") + 1:])

    if len(hours) == 2 and len(minutes) == 2:
        try:
            hours = int(hours)
            minutes = int(minutes)
            if not (0 <= hours < 24 and 0 <= minutes < 60):
                raise TimeError(time)

        except ValueError:
            raise TimeError(time)
    else:
        raise TimeError(time)


def status_mask(status: str, user_input: bool = False) -> None:
    '''Проверка статуса на корректность.

    > status - статус, который необходимо проверить
    > user_input - булево значение, определяющее
    вызвана ли эта функция в последствии ввода пользователем
    или была вызвана с технической стороны.

    Ничего не возвращает, а только вызывает ошибку, если статус некорректен.
    '''
    if not user_input:
        # 'a', 'b', 'c', 'd' - это то как статусы хранятся в объекте,
        # это сделано для эффективного сравнения статусов.
        values = ('a', "Провалена", 'b', "Получена",
                  'c', "В процессе", 'd', "Выполнена")
    # Если функция вызвана в последствии ввода пользователем, значит
    # нельзя допустить, чтобы пользователь мог занести в базу данных
    # значения 'a', 'b', 'c', 'd' в качестве статуса, так как это вызовет
    # ошибку при обязательном форматировании в процессе добавления.
    else:
        values = ("Провалена", "Получена",
                  "В процессе", "Выполнена")

    if status not in values:
        raise StatusError(status)


def command_mask(command: str) -> None:
    '''Проверка команды на корректность.

    > command - команда, которую необходимо проверить

    Ничего не возвращает, а только вызывает ошибку, если команда некоррекна.
    '''
    # В синтаксисе хранятся все команды, которые может распознать программа.
    syntax = ["quit", "id", "help", "date", "file",
              "executor", "task", "get_date", "path",
              "get_time", "do_date", "do_time",
              "status", "function", "sort", "show",
              "save", "remove", "add", "edit"]

    if command not in syntax:
        raise SyntaxError(command)


def level_mask(command: str, level: int) -> None:
    '''Проверка соответствия вызванной команды с уровнем программы.

    > command - вызванная команда
    > level - уровень программы, на котором была вызвана программа

    Ничего не возвращает, а только вызывает ошибку, если команда вызвана
    не на том уровне.
    '''
    # Список доступных команд для каждого уровня:
    # level_commands[0] - для первого уровня и т.д.
    level_commands = [["quit", "date", "path", "help"],

                      ["quit", "file", "save", "help",
                       "id", "get_date", "get_time",
                       "do_date", "do_time", "executor",
                       "task", "status", "remove", "edit",
                       "function", "sort", "show"],

                      ["quit", "save", "help", "show",
                       "edit", "add", "remove"]]

    if command not in level_commands[level - 1]:
        raise LevelError(command)


def path_mask(path: str) -> None:
    '''Проверка пути на корректность.

    > path - путь к файлу, который необходимо проверить

    Ничего не возвращает, а только вызывает ошибку, если путь некорректен.
    '''
    # Символы, недопустимые для названия файла в Windows.
    # Этим, соответственно, пресекается возможность указывания пути к файлам,
    # находящимся не в директории с исполняемым файлом.
    inappropriate_symbols = ['/', '\\', ':', '*',
                             '?', '"', '|', '<', '>']

    for symbol in inappropriate_symbols:
        if symbol in path:
            raise PathError(path)

    # Единственное допустимое расширение файла - .txt для читаемости
    # результата записи в файл.
    if path[path.rfind(".") + 1:] != "txt":
        raise PathError(path)


def date_format(date: str, user_input: bool = False) -> str:
    '''Форматирование даты.

    > date - дата, которую необходимо отформатировать
    > user_input - булево значение, необходимое для date_mask()

    Возвращает отформатированную дату.
    '''
    date_mask(date, user_input)

    first = date[: date.find(".")]
    second = date[date.find(".") + 1: date.rfind(".")]
    third = date[date.rfind(".") + 1:]

    # По сути, меняет местами первый и последние значения даты (год и день).
    # Это нужно для хранения более эффективных для сравнения дат в объекте.
    date = f"{third}.{second}.{first}"

    return date


def status_format(status: str, user_input: bool = False) -> str:
    '''Форматирование статуса задачи.

    > status - статус задачи
    > user_input - булево значение, необходимое для функции status_mask()

    Возвращает отформатированный статус задачи.
    '''
    status_mask(status, user_input)

    # Хранение статусов в виде 'a','b','c','d' необходимо для более
    # эффективного сравнения в последствии.
    match status:
        case 'a': status = "Провалена"
        case 'b': status = "Получена"
        case 'c': status = "В процессе"
        case 'd': status = "Выполнена"
        case "Провалена": status = 'a'
        case "Получена": status = 'b'
        case "В процессе": status = 'c'
        case "Выполнена": status = 'd'

    return status


def items_format(items: list) -> list:
    '''Форматирование значений всех атрибутов задачи.

    > items - список значений всех атрибутов задачи

    Возвращает отформатированный список значений атрибутов задачи.
    '''
    items[1] = date_format(items[1])
    items[3] = date_format(items[3])
    items[7] = status_format(items[7])

    return items


def function_request() -> str | None:
    '''Требование ввода номера функции.

    Ничего не принимает.

    Возвращает строку, если пользователь ввел корректное значение, или None,
    если пользователь предпочел выйти из цикла, с помощью "quit".
    '''
    while True:
        function = str(input(interface.text["function_request"]))
        if function == "quit":
            break
        try:
            function = int(function)
            if function in range(1, 4):
                return str(function)
            else:
                print("Некорректный номер функции")
        except ValueError:
            print("Некорректный номер функции")

    return None


def day_request() -> int | None:
    '''Требование ввода количества дней для function_1()

    Ничего не принимает.

    Возвращает число, если пользователь ввел корректное значение, или None,
    если пользователь предпочел выйти из цикла, с помощью "quit".
    '''
    while True:
        day = str(input(interface.text["day_request"]))
        if day == "quit":
            break
        try:
            day = int(day)
            if day >= 0:
                return day
            else:
                print("N должно быть неотрицательным!")
        except ValueError:
            print("N должно быть целым и неотрицательным!")

    return None


def date_request() -> str | None:
    '''Требование ввода даты.

    Ничего не принимает.

    Возвращает строку, если пользователь ввел корректное значение, или None,
    если пользователь предпочел выйти из цикла, с помощью "quit".
    '''
    while True:
        date = str(input(interface.text["date_request"]))
        if date == "quit":
            break
        try:
            date = date_format(date, user_input=True)
            return date
        except DateError as exception:
            print(f"Некорректный формат даты: {exception.args[0]}")

    return None


def date_and_day_request() -> tuple | None:
    '''Последовательное требование ввода даты и количества дней.

    Ничего не принимает.

    Возвращает кортеж, если пользователь ввел корректное значение, или None,
    если пользователь предпочел выйти из цикла, с помощью "quit".
    '''
    date = date_request()
    if date is not None:
        day = day_request()
        if day is not None:
            return (date, day)
        else:
            return None
    else:
        return None


def path_request(banned_path: str = None) -> str | None:
    '''Требование ввода пути к файлу.

    > banned_path - недопустимый путь к файлу, необходим для того, чтобы
    пользователь не смог перезаписать открытый файл из уровня 2 программы

    Возвращает строку, если пользователь ввел корректное значение, или None,
    если пользователь предпочел выйти из цикла, с помощью "quit".
    '''
    while True:
        path = str(input(interface.text["path_request"]))
        if path == "quit":
            break
        try:
            path_mask(path)
            if path != banned_path:
                return path
            else:
                print(interface.text["banned_path"])
        except PathError as exception:
            print(f"Некорректное имя файла: {exception.args[0]}")

    return None


def confirmation_request(arg: str = "") -> bool:
    '''Требование ввода подтверждения.

    > arg - значение, определяющее какое сообщение будет отображено

    Возвращает булево значение, если пользователь ввел корректное значение.
    '''
    while True:
        confirmation = str(input(interface.text[arg + "confirmation"]))

        if confirmation == "y":
            confirmation = True
            break

        elif confirmation == "n":
            confirmation = False
            break

        else:
            print(f"Некорректный ответ: {confirmation}")

    return confirmation


def id_request(obj: tasks.Tasks) -> int | None:
    '''Требование ввода значения атрибута 'ID' задачи.

    > obj - ссылка на объект, для проверки существования индекса

    Возвращает число, если пользователь ввел корректное значение, или None,
    если пользователь предпочел выйти из цикла, с помощью "quit".
    '''
    while True:
        index = str(input(interface.text["id_request"]))
        if index == "quit":
            break
        try:
            index = int(index)
            try:
                obj.get_task(0, index)
                return index
            except tasks.TaskNotFoundError as exception:
                print(f"Задачи c ID:{exception.args[0][1]} не сущесвует!")

        except ValueError:
            print("Некорректный ID!")

    return None


def item_request() -> int | None:
    '''Требование ввода индекса атрибута задачи.

    Ничего не принимает.

    Возвращает число, если пользователь ввел корректное значение, или None,
    если пользователь предпочел выйти из цикла, с помощью "quit".
    '''
    while True:
        item = str(input(interface.text["item_request"]))
        if item == "quit":
            break
        try:
            item = int(item)
            if item in range(1, 8):
                return item
            else:
                print(f"Некорректный номер варианта: {item}")
        except ValueError:
            print(f"Некорректный номер варианта: {item}")

    return None


def status_request() -> str | None:
    '''Требование ввода статуса задачи.

    Ничего не принимает.

    Возвращает строку, если пользователь ввел корректное значение, или None,
    если пользователь предпочел выйти из цикла, с помощью "quit".
    '''
    while True:
        status = str(input(interface.text["status_request"]))
        if status == "quit":
            break
        try:
            status = status_format(status, user_input=True)
            return status
        except StatusError:
            print("Некорректный статус задачи!")

    return None


def executor_request(obj: tasks.Tasks) -> str | None:
    '''Требование ввода исполнителя задачи.

    > obj - ссылка на объект, для проверки существования исполнителя

    Возвращает строку, если пользователь ввел корректное значение, или None,
    если пользователь предпочел выйти из цикла, с помощью "quit".
    '''
    while True:
        executor = str(input(interface.text["executor_request"]))
        if executor == "quit":
            break
        try:
            obj.get_task(5, executor)
            return executor
        except tasks.TaskNotFoundError:
            print("Такого исполнителя нет в базе данных!")

    return None


def key_request(number: int) -> tuple | None:
    '''Требование ввода ключа сортировки.

    > number - номер ключа (1 - первичный ключ, 2 - вторичный ключ),
    для отображения соответствующего сообщения

    Возвращает кортеж, если пользователь ввел корректное значение, или None,
    если пользователь предпочел выйти из цикла, с помощью "quit".
    '''
    print(interface.text["key_list"])
    while True:
        key = str(input(interface.text[f"key_{number}_request"]))
        if key == "quit":
            break
        try:
            key = int(key)
            if key in range(0, 8):
                break
            else:
                print("Некорректное значение ключа!")
        except ValueError:
            print("Некорректное значение ключа!")

    if key == "quit":
        return None

    while True:
        reverse = str(input(interface.text["reverse_request"]))
        if reverse == "quit":
            break
        try:
            reverse = int(reverse)
            if reverse == 1:
                reverse = False
                break
            elif reverse == 2:
                reverse = True
                break
            else:
                print("Некорректный ответ!")
        except ValueError:
            print("Некорректный ответ!")

    if reverse == "quit":
        return None

    return (key, reverse)


def time_request() -> str | None:
    '''Требование ввода времени.

    Ничего не принимает.

    Возвращает строку, если пользователь ввел корректное значение, или None,
    если пользователь предпочел выйти из цикла, с помощью "quit".
    '''
    while True:
        time = str(input(interface.text["time_request"]))
        if time == "quit":
            break
        try:
            time_mask(time)
            return time
        except TimeError:
            print("Некорректное время!")

    return None


def task_request() -> str | None:
    '''Требование ввода задачи.

    Ничего не принимает.

    Возвращает строку, если пользователь ввел корректное значение, или None,
    если пользователь предпочел выйти из цикла, с помощью "quit".
    '''
    while True:
        task = str(input(interface.text["task_request"]))
        if task == "quit":
            break

        if len(task) != task.count(" "):
            return task
        else:
            print("Значение не может быть пустым!")

    return None


def edit_item(obj: tasks.Tasks, item: int, index: int) -> None:
    '''Редактирование значения определенного атрибута задачи.

    > obj - ссылка на объект
    > index - значение атрибута 'ID' задачи
    > item - индекс атрибута задачи

    Ничего не возвращает.
    '''
    # Список ключей для получения сообщений для соответствующего атрибута.
    requests = ["date_request", "time_request", "date_request",
                "time_request", "executor_request", "task_request",
                "status_request"]

    while True:
        value = str(input(interface.text[requests[item - 1]]))
        if value == "quit":
            break

        if obj.edit_item(index, item, value):
            print("База данных успешно изменена.")
            break


def edit_task(obj: tasks.Tasks, index: int) -> None:
    '''Редактирование задачи целиком.

    > obj - ссылка на объект
    > index - значение атрибута 'ID' задачи

    Ничего не возвращает.
    '''
    print(interface.text["items_example"])

    while True:
        task = str(input(interface.text["items_request"]))
        if task == "quit":
            break

        items = task.split("|")
        # Ввод осуществляется без 'ID' задачи, так что он добавляется вручную.
        items.insert(0, index)

        try:
            if obj.edit_task(index, items):
                print("База данных успешно изменена.")
                break
        except ItemsError():
            print("Некорректное количество данных.")


def free_id(obj: tasks.Tasks) -> int:
    '''Нахождение минимального свободного 'ID' для новой задачи.

    > obj - ссылка на объект

    Возвращает число - значение минимального свободного 'ID'.
    '''
    # Сортировка по 'ID' задачи по возрастанию для эффективности поиска.
    shell.sort(obj, (0, 0))
    min_id = 1

    for task in obj.list:
        if min_id == task[0]:
            min_id += 1

    return min_id


def add_task(obj: tasks.Tasks) -> None:
    '''Добавление новой задачи в список задач.

    > obj - ссылка на объект

    Ничего не возвращает.
    '''
    index = free_id(obj)
    print(interface.text["items_example"])

    while True:
        task = str(input(interface.text["items_request"]))
        if task == "quit":
            break

        items = task.split("|")
        # Ввод осуществляется без 'ID', так что он добавляется вручную.
        items.insert(0, index)

        try:
            if obj.add(items):
                print("База данных успешно изменена.")
                break
        except ItemsError:
            print("Некорректное количество данных!")


def get_last_date(days: int, curr_date: str) -> str:
    '''Нахождение даты, на определенное количество дней в прошлом.

    > days - количество дней
    > curr_date - дата, от которой ведется отсчет дней

    Возвращается строка - такая дата.
    '''
    # Текущая дата вводится в том же формате, в каком и хранится в объекте.
    curr_day = int(curr_date[curr_date.rfind(".") + 1:])
    curr_month = int(curr_date[curr_date.find(".") + 1: curr_date.rfind(".")])
    curr_year = int(curr_date[: curr_date.find(".")])

    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    curr_day -= days

    while curr_day <= 0:
        curr_month -= 1

        if curr_month == 0:
            curr_month = 12
            curr_year -= 1
            if curr_year < 0:
                raise YearError()

        days_in_current_month = days_in_months[curr_month - 1]

        if curr_month == 2 and leap_year(curr_year):
            days_in_current_month += 1

        curr_day += days_in_current_month

    # Форматирование даты так, чтобы она соответствовала виду: ГГГГ.ММ.ДД
    if curr_year < 10:
        last_year = f"000{curr_year}"
    elif curr_year < 100:
        last_year = f"00{curr_year}"
    elif curr_year < 1000:
        last_year = f"0{curr_year}"
    else:
        last_year = f"{curr_year}"

    if curr_month < 10:
        last_month = f"0{curr_month}"
    else:
        last_month = f"{curr_month}"

    if curr_day < 10:
        last_day = f"0{curr_day}"
    else:
        last_day = f"{curr_day}"

    last_date = last_year + "." + last_month + "." + last_day

    return last_date


def function_1(obj: tasks.Tasks, days: int, curr_date: str):
    '''Первая функция, которая должна поддерживаться программой по условию.

    obj - ссылка на объект
    days - количество дней, чтобы найти дату на это количество дней в прошлом
    curr_date - дата, от которой ведется отсчет

    Возвращает отсортированную копию объекта класса Tasks из модуля tasks.
    '''
    last_date = get_last_date(days, curr_date)
    # Получение списка задач, дата получения которых >= last_date.
    to_sort = obj.get(1, last_date)

    shell.sort(to_sort, (1, 7), reverse1=True, reverse2=True)

    return to_sort


def function_2(obj: tasks.Tasks, executor: str):
    '''Вторая функция, которая должна поддерживаться программой по условию.

    obj - ссылка на объект
    executor - имя исполнителя

    Возвращает отсортированную копию объекта класса Tasks из модуля tasks.
    '''
    # Получение списка проваленых задач определенного исполнителя.
    to_sort = obj.get(5, executor).get(7, "a")

    shell.sort(to_sort, (3, 6), reverse1=True)

    return to_sort


def function_3(obj: tasks.Tasks):
    '''Третья функция, которая должна поддерживаться программой по условию.

    obj - ссылка на объект

    Возвращает отсортированную копию объекта класса Tasks из модуля tasks.
    '''
    # Получение списка задач, находящихся на исполнении (В процессе/Получена).
    to_sort = obj.get(7, "bc")

    shell.sort(to_sort, (5, 3))

    return to_sort


def lifecycle(level: int = 1, path: str = "db.txt",
              obj: tasks.Tasks = None) -> None:
    '''Жизненный цикл программы, получающий и выполняющий команды.

    > level - уровень программы (по умолчанию - 1)
    > path - путь к файлу, который необходимо прочитать
    > obj - ссылка на объект (при запуске на первый уровень она не требуется)

    Ничего не возвращает.
    '''
    # Спрайт приветственного меню.
    if level == 1:
        print(interface.sprite)

    # Если уровень программы не 1, то во временный объект копируются данные
    # из исходного объекта (изменения в исходном объекте необратимы).
    if level != 1:
        temp_obj = obj.copy()
        temp_obj.print()

    while True:
        command = str(input("> "))
        try:
            command_mask(command)
            try:
                level_mask(command, level)
                match command:
                    # quit - перемещает пользователя на один уровень назад.
                    case "quit":
                        if level == 1:
                            break
                        elif confirmation_request():
                            if level == 2:
                                print(interface.sprite)
                            break

                    # file - перемещает пользователя на 3 уровень.
                    # После того, как программа вернется на второй уровень,
                    # снова считывает файл в исходный объект, для того, чтобы
                    # сразу отобразить изменения, произошедшие на 3 уровне.
                    case "file":
                        if confirmation_request():
                            lifecycle(3, path, obj)
                            obj = tasks.Tasks.read(path)
                            temp_obj = obj.copy()
                            temp_obj.print()

                    # После чтения файла пользователь перемещается в 2 уровень
                    case "path":
                        print(f"База данных будет прочитана из файла: {path}")
                        if confirmation_request("path_"):
                            print(f"Чтение {path}...")
                            try:
                                obj = tasks.Tasks.read(path)
                                lifecycle(2, path, obj)
                            except FileNotFoundError:
                                print("Такого файла не существует.")
                        else:
                            new_path = path_request()
                            if new_path is not None:
                                print(f"Чтение {new_path}...")
                                try:
                                    obj = tasks.Tasks.read(new_path)
                                    if confirmation_request("path_"):
                                        path = new_path
                                        lifecycle(2, path, obj)
                                except FileNotFoundError:
                                    print("Такого файла не существует.")

                    case "help":
                        print(interface.text["help_"+str(level)])

                    # Записывает временный объект в выбранный файл.
                    case "save":
                        if level == 2:
                            new_path = path_request(path)
                            if new_path is not None:
                                if confirmation_request("path_"):
                                    temp_obj.write(new_path)
                        else:
                            print(f"База данных будет записана в: {path}")
                            if confirmation_request("path_"):
                                temp_obj.write(path)
                            else:
                                new_path = path_request()
                                if new_path is not None:
                                    if confirmation_request("path_"):
                                        temp_obj.write(new_path)

                    case "remove":
                        index = id_request(temp_obj)

                        temp_obj.remove(index)
                        temp_obj.print()

                    case "edit":
                        index = id_request(temp_obj)
                        if level == 2 and index is not None:
                            print(interface.text["item_list"])
                            item = item_request()
                            if item is not None:
                                edit_item(temp_obj, item, index)
                        if level == 3 and index is not None:
                            edit_task(temp_obj, index)

                        temp_obj.print()

                    case "add":
                        add_task(temp_obj)

                        temp_obj.print()

                    case "show":
                        temp_obj = obj.copy()

                        temp_obj.print()

                    case "function":
                        function = function_request()
                        if function is not None:
                            print(interface.text["function_"+function])
                            if function == "1":
                                date_and_day = date_and_day_request()
                                if date_and_day is not None:
                                    date = date_and_day[0]
                                    day = date_and_day[1]
                                    temp_obj = function_1(obj, day, date)
                            elif function == "2":
                                executor = executor_request(obj)
                                if executor is not None:
                                    temp_obj = function_2(obj, executor)
                            elif function == "3":
                                input(interface.text["press_enter"])
                                temp_obj = function_3(obj)

                        temp_obj.print()

                    case "sort":
                        key1 = key_request(1)
                        if key1 is not None:
                            key2 = key_request(2)
                            if key2 is not None:
                                shell.sort(temp_obj, (key1[0], key2[0]),
                                           reverse1=key1[1], reverse2=key2[1])
                        temp_obj.print()

                    # Далее все команды возвращают вхождения задач,
                    # значения атрибутов которых соответствуют условию.
                    case "id":
                        index = id_request(obj)
                        if index is not None:
                            temp_obj = obj.get(0, index)

                        temp_obj.print()

                    case "get_date":
                        get_date = date_request()
                        if get_date is not None:
                            temp_obj = obj.get(1, get_date, parse=True)

                        temp_obj.print()

                    case "get_time":
                        get_time = time_request()
                        if get_time is not None:
                            temp_obj = obj.get(2, get_time)

                        temp_obj.print()

                    case "do_date":
                        do_date = date_request()
                        if do_date is not None:
                            temp_obj = obj.get(3, do_date, parse=True)

                        temp_obj.print()

                    case "do_time":
                        do_time = time_request()
                        if do_time is not None:
                            temp_obj = obj.get(4, do_time)

                        temp_obj.print()

                    case "executor":
                        executor = executor_request(obj)
                        if executor is not None:
                            temp_obj = obj.get(5, executor)

                        temp_obj.print()

                    case "task":
                        task = task_request()
                        if task is not None:
                            temp_obj = obj.get(6, task)

                        temp_obj.print()

                    case "status":
                        status = status_request()
                        if status is not None:
                            temp_obj = obj.get(7, status)

                        temp_obj.print()

            except LevelError as exception:
                wrong_command = exception.args[0]
                print(f"Команду {wrong_command} здесь использовать нельзя")

        except SyntaxError as exception:
            print(f"Неизвестная команда: {exception.args[0]}")
