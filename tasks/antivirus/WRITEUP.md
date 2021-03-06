# Антивирус: Write-up

Таск — вариация на тему Local File Inclusion.

Заходим на сайт с антивирусом. Здесь мы видим возможность загрузить произвольный файл на проверку, а также выбор расширения файла. Загрузив произвольный файл, мы получаем отчёт.

Уязвимость заключалась в недостаточной проверке поля `ext` (расширение файла). Сделав запрос с неверным расширением, можно получить такое сообщение об ошибке:

```
Не удалось проверить файл /tmp/uploads/example.txt плагин /app/plugins/test.py не найден 
```

Такие запросы можно выполнять любым удобным способом; автор пользовался функцией "Edit and Resend" в Firefox, которая позволяет отредактировать и отправить произвольный запрос из вкладки инспектора "Network".

Таким образом мы получили сразу два пути: путь к загруженному файлу и путь к несуществующему плагину. Становится понятно, что антивирус динамически загружает модули, отвечающие за проверку файлов того или иного типа.

Осталось лишь попробовать загрузить наш собственный файл в качестве модуля. Сделав запрос с `ext=/tmp/uploads/test`, и приложив файл `test.py` с кодом `print("Hello, world!")`, получаем:

```
Hello, world! Не удалось проверить файл /tmp/uploads/test.py 
```

На этом этапе мы можем выполнять произвольный код на стороне сервера. Осталось изучить файловую систему, пользуясь стандартными функциями Python. Искомый флаг находится, по традиции, в файле `/etc/passwd`. Получить его можно, например, однострочником на Python:

```python
print(open("/etc/passwd").read())
```

Флаг: **ugra_who_checks_the_checker_49e6dac45e8f**
