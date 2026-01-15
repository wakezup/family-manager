import logic as log


class TaskNotFoundError(Exception):
    '''Класс исключения.

    Возникает при попытке получить доступ к несуществующей задаче.
    '''
    pass


class Tasks:
    '''Класс списка задач.

    Представляет из себя двумерный массив, каждый из элементов которого
    является отдельной задачей.
    Класс помогает структурировать список задач, сделать удобным
    взаимодействие с ним.
    '''
    def __init__(self) -> None:
        '''Инициализация объекта.

        > self - ссылка на инициализируемый объект

        Инициализирует список объекта.

        Ничего не возвращает.
        '''
        self.list = []

    def items_check(self, items) -> bool:
        '''Проверка атрибутов задачи.

        > self - ссылка на объект
        > items - атрибуты задачи

        Проверка атрибутов задачи на корректность:
        (даты получения и выполнения, время, статус и т.д.).

        Возвращает булево значение (True/False),
        означающее соответствуют ли атрибуты правилам.
        '''
        # У каждой задачи должно быть 8 атрибутов
        if len(items) != 8:
            raise log.ItemsError()

        # Форматирование даты для эффективного сравнения строк в сортировке
        try:
            items[1] = log.date_format(items[1])
        except log.DateError as exception:
            date = exception.args[0]
            print(f"Задача ID:{items[0]} -> Некорректная дата: {date}")
            return False

        try:
            items[3] = log.date_format(items[3])
        except log.DateError as exception:
            date = exception.args[0]
            print(f"Задача ID:{items[0]} -> Некорректная дата: {date}")
            return False

        # Проверка на корректность времени
        try:
            log.time_mask(items[2])
        except log.TimeError as exception:
            time = exception.args[0]
            print(f"Задача ID:{items[0]} -> Некорректное время: {time}")
            return False

        try:
            log.time_mask(items[4])
        except log.TimeError as exception:
            time = exception.args[0]
            print(f"Задача ID:{items[0]} -> Некорректное время: {time}")
            return False

        # Дата выполнения не может быть меньше даты получения
        if items[3] < items[1]:
            print(f"Задача ID:{items[0]} -> Невозможное соотношение дат")
            return False
        # Если даты равны, то сравнивается время получения и выполнения
        elif items[3] == items[1]:
            if items[4] < items[2]:
                print(f"Задача ID:{items[0]} -> Невозможное соотношение дат")
                return False

        if len(items[5]) == items[5].count(" "):
            print(f"Задача ID:{items[0]} -> Пустое значение 'Исполнитель'")
            return False

        if len(items[6]) == items[6].count(" "):
            print(f"Задача ID:{items[0]} -> Пустое значение 'Задача'")
            return False

        # Проверка на корректность статуса
        try:
            items[7] = log.status_format(items[7])
        except log.StatusError as exception:
            status = exception.args[0]
            print(f"Задача ID:{items[0]} -> Некорректный статус: {status}")
            return False

        return True

    def copy(self):
        '''Копирование объекта.

        > self - ссылка на объект

        Создается новый объект класса Tasks,
        список задач копируется в новый объект.

        Возвращает копию объекта класса Tasks.
        '''
        copy = Tasks()
        for task in self.list:
            copy.list.append(task[:])

        return copy

    def add(self, items: list, index: int = None) -> bool:
        '''Добавление задачи в список.

        > self - ссылка на объект
        > items - атрибуты задачи
        > index - желательный индекс задачи в списке (None - по умолчанию)

        Происходит проверка атрибутов задачи.
        Если index = None, то ему присваивается значение длины списка задач,
        то есть минимальное возможное.

        Возвращает булево значение (True/False), означающее добавилась ли
        задача в список задач.
        '''
        good_items = self.items_check(items)

        if index is None:
            index = len(self.list)

        if good_items:
            self.list.insert(index, items)

        return good_items

    def remove(self, index: int) -> bool:
        '''Удаление задачи из списка задач.

        > self - ссылка на объект
        > index - значение атрибута 'ID' задачи

        По значению атрибута 'ID' осуществляется доступ
        к задаче, которую необходимо удалить.

        Возвращает булево значение (True/False), означающее
        удалилась ли задача из списка задач.
        '''
        removed = False

        for task in self.list:
            # 0 - индекс, по которому в задаче всегда находится атрибут 'ID'
            if task[0] == index:
                self.list.remove(task)
                removed = True
                break

        return removed

    def edit_item(self, index: int, item: int, value: str) -> bool:
        '''Редактирование значения атрибута задачи.

        > self - ссылка на объект
        > index - значение атрибута 'ID' задачи
        > item - индекс, по которому в задаче находится атрибут
        > value - новое значение указанного атрибута задачи

        Найдя задачу с нужным 'ID' и сохранив ее индекс в списке
        задач, формируется новый список атрибутов для добавления
        новой задачи (старый список атрибутов, лишь с одним измененным
        значением). Старая задача удаляется, измененная добавляется
        по тому же индексу.

        Защита от некорректного значения атрибута обеспечивается
        средой, из которой вызывается этот метод.

        Защита от изменения непосредственно значения атрибута 'ID'
        обеспечивается средой, из которой вызывается этот метод.

        Возвращает булево значение (True/False), означающее было ли
        изменено значение необходимого атрибута задачи.
        '''
        edited = False

        for task_index in range(len(self.list)):
            # 0 - индекс, по которому в задаче всегда находится атрибут 'ID'
            if self.list[task_index][0] == index:
                items = log.items_format(self.list[task_index])
                items[item] = value
                self.remove(index)
                edited = self.add(items, task_index)
                break

        return edited

    def edit_task(self, index: int, items: list) -> bool:
        '''Редактирование задачи целиком.

        > self - ссылка на объект
        > index - значение атрибута 'ID' задачи
        > items - список измененных значений атрибутов задачи

        Найдя задачу с соответствующим 'ID' и сохранив ее индекс
        в списке задач, удаляется старая задача и добавляется новая
        по этому же индексу.

        Защита от некорректности значений атрибутов обеспечивается
        средой, из которой вызывается этот метод.

        Возвращается булево значение (True/False), означающее
        была ли изменена задача.
        '''
        edited = False

        for task_index in range(len(self.list)):
            if self.list[task_index][0] == index:
                self.remove(index)
                edited = self.add(items, task_index)
                break

        return edited

    def print(self) -> None:
        '''Вывод содержимого списка задач на экран.

        > self - ссылка на объект

        Собирается информация о предпочтительном формировании
        строк с данными из списка задач.

        Таким образом, пользователь увидит ровную таблицу задач.

        Ничего не возвращает.
        '''
        # Информация о максимальной длине значений для каждого атрибута
        if len(self.list) != 0:
            max_space = log.max_space(self)

            header_labels = [
                "ID", "Получена",
                "Выполнить", "Исполнитель",
                "Задача", "Статус"
                ]

            print("\n"+log.string(max_space, header_labels))

            for task in self.list:
                # Для каждой задачи значения атрибутов форматируются
                task_labels = [
                    str(task[0]), f"{log.date_format(task[1])} {task[2]}",
                    f"{log.date_format(task[3])} {task[4]}", task[5],
                    task[6], log.status_format(task[7])
                    ]

                print(log.string(max_space, task_labels))
        else:
            print("Список задач пуст!")

    def get(self, item: int, value: str | int):
        '''Получение копии объекта с задачами, подходящими по условию.

        > self - ссылка на объект
        > item - индекс атрибута в задаче, по которому задается условие
        > value - значение атрибута, по которому задается условие

        Создается новый объект, задачи, подходящие по условию добавляются
        в список задач нового объекта в виде копий.

        Возвращает копию объекта класса Tasks с задачами, подходящими по
        условию.
        '''
        tasklist = Tasks()

        for task in self.list:
            if log.condition(item, task[item], value):
                tasklist.list.append(task[:])

        return tasklist

    def get_task(self, item: int, value: str | int) -> list:
        '''Поиск первой подходящей по значению задачи.

        > self - ссылка на объект
        > item - индекс атрибута задачи
        > value - значение атрибута задачи, по которому происходит поиск

        Возвращает список значений атрибутов найденной задачи, если
        же задача не была найдена вызывает исключение TaskNotFoundError.
        '''
        found = False

        for task in self.list:
            if task[item] == value:
                found = True
                return task

        if not found:
            raise TaskNotFoundError((item, value))

    def read(path: str):
        '''Чтение из файла в объект класса Tasks.

        > path - путь, по которому находится файл

        Создается новый объект класса Tasks, читается файл,
        формируя значения всех атрибутов каждой задачи в необходимом
        виде, после добавляя задачи в новый объект, если значения
        даны в корректном виде.

        Возвращает новый объект класса Tasks с данными из
        прочитанного файла.
        '''
        obj = Tasks()

        file = open(path, "r", encoding="utf-8")

        strings = file.readlines()
        index = 0
        for string in strings:
            index += 1
            items = string.split("|")
            items.insert(0, index)
            try:
                items[7] = items[7].strip()
                try:
                    obj.add(items)
                except log.ItemsError:
                    print(f"Задача ID:{index} -> Слишком много данных!")
            except IndexError:
                print(f"Задача ID:{index} -> Не хватает данных!")
        file.close()

        return obj

    def write(self, path: str) -> None:
        '''Запись данных из объекта в файл.

        > self - ссылка на объект
        > path - путь, по которому необходимо записать файл

        Формирует данные обратно в необходимые для считывания из файла.
        Записывает сформированные данные в файл по заданному пути.

        Ничего не возвращает.
        '''
        file = open(path, "w", encoding="utf-8")

        for task in self.list:
            string = ''
            for item in range(len(task)):
                if item == 1 or item == 3:
                    string += f"{log.date_format(task[item])}|"
                elif item == 7:
                    string += f"{log.status_format(task[item])}\n"
                elif item != 0:
                    string += f"{task[item]}|"

            file.write(string)
        file.close()
