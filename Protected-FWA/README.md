### Инструкция по сборке и запуску приложения
> pip install flask

### Комментарии к исправлениям
xss: http://127.0.0.1:8081/xss?name=<script>alert('xss')</script>
Чтобы избавиться от уязвиостей типа xss нужно экранировать пользовательский вход, чтобы исключить выполнение вредоносного кода в html. В пайтон имеется полезная функция 'from markupsafe import escape'.
Лучшим вариантом защиты от атак типа xss - это экранирвоание, валидация пользовательского ввода и правильная настройка CSP.


idor: http://127.0.0.1:8081/users?id=1
Реализовать механизмы авторизации и аутентификации, чтобы у каждого пользователя были свои индивидуальные права доступа.
Не показывать идентификаторы прямо в url.

sqli: http://127.0.0.1:8081/sql injection in /user/' OR 1=1 --
Нужно использовать строго параметризированные sql запросы и опять таки экранировать и валидировать пользовательский ввод.

os injection: http://127.0.0.1:8081/os_inj?hostname=id
Используем метод subprocess.check_output() для выполнения операционных команд, но в безопасном виде. Вместо передачи команды в виде строки и использования shell=True, мы передаем команду и ее аргументы как список, где каждый элемент списка представляет одну часть команды.
Также использовать фильтрацию/валидацию пользовательских входных данных.

path traversal: http://127.0.0.1:8081/read_file?filename=/../../../../../../etc/passwd
Лля создания абсолютного пути используем функцию os.path.join. Добавляем проверку наличия подобного файла перед его открытием. Написали функцию is_safe_filename, чтобы убедиться, что имя файла содержит разрешенные символы и имеет разрешенное расширение.


brute force: http://127.0.0.1:8081/login?username=admin&password=superadmin
Внедрить аутентификацию идентификацию.
Нужно убедиться, что злоумышленние не сможет просто перебрать пароль, нужно ввести ограниченное кол-во попыток после чего заблокировать запрошенный аккаунт. Так же хотелось бы учесть, что избавиться от атак типа "Брут форс" - очень сложно.
...

### Дополнительные комментарии
> Опциональный раздел

...