# jibrel_test_assignment

Test assignment for Backend Developer in Jibrel. MIT License

## How to run
Use python3.6 or python3.7:

`python jibrel.py -h`

The project doesn't require installation of any additional requirements to run.
Main dependency manager is poetry, but I also convert all project 
dev-requirements to `pip-requirements.txt` (only dev requirements, really)

## How to develop
python3.7 is a requirement for development.

In the beginning, you need to install all requirements 
(see more info in poetry documentation):

`poetry run install`

Use these checks for all code:

`poetry run mypy .`

`poetry run flake8 .`

Configuration for flake8 and mypy placed in setup.cfg

Use dephell for converting poetry format to requirements.txt format:

`poetry run dephell convert`

## Structure
See readmes in directories and docstrings in modules. 

## Technical task

Вольный пересказ:
 - есть большой лог
 - этот лог нужно распарсить, распределить события по группам и 
 проанализировать
 - посчитать 95 перцентиль времени обработки запросов
 - количество событий определенного типа

Python3.5+, любые библиотеки

## Research

### Базовый парсинг логов
Поверхностное изучение показало, что большинство домашних решений парсит
 логи регулярками.

Есть серьёзная утилита [logparser](https://logparser.readthedocs.io/en/latest/), 
использующая набор алгоритмов для поиска по паттернам, парсинга и анализа логов.

Но для данного задания регулярки будут слишком медленны, а logparser слишком усложняющим —
в лог-файлах в качестве разделителя используется символ табуляции, а последовательность
полей известна заранее. Буду использовать встроенные функции для работы со строками

### Конвертация в python-типы
Было желание взять attrs/dataclassed, но базовые типы должны быть проще и эффективнее
в хранении больших объемов в памяти. Для эффективности по памяти был использован класс 
с слотами.

### Анализ
Просто перебираю Event, мутируя словарик с Request. Полученный набор запросов обрабатываю: 
считаю количество проваленных (у которых не хватает OK от бекенда), считаю персентиль 
(если точно взять индекс не получается, использую среднее арифметическое между двумя ближайшими)

Решил не брать внешнюю библиотеку для расчёта персентиля. 

Изначально backends_group был нулём, к которому прибавлялось-вычиталось при разных событиях, 
но дополнительные данные не помешают

### Throw mode
В обработке участвуют только несколько типов ивентов — я добавил throw mode, который не 
конвертирует ненужные ивенты. Это дало прирост по скорости ~20%:

```
$ time python jibrel.py logs/005.in  
Failed requests: 1627
95% percentile request time 3972.04 ms
python jibrel.py logs/005.in  4.96s user 0.09s system 99% cpu 5.048 total

$ python jibrel.py --throw logs/005.in
Failed requests: 1627
95% percentile request time 3972.04 ms
python jibrel.py --throw logs/005.in  4.06s user 0.09s system 99% cpu 4.160 total
```

### CLI 
Использую встроенный argparse, ответ возвращаю в stdout в читаемом формате.

### Утилиты
Использую проверенный временем комплект из 
 - poetry (пакетный менеджер, который умеет в лок и сложный резолв зависимостей)
 - wemake-python-styleguide (линтер на стероидах поверх flake8)
 - mypy (для проверки типизации)
 