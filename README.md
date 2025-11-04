## Книжковий інтернет магазин HomeBook

Даний додаток складається з наступних сервісів:  

- **Вебсервіс** - відповідає за відображення всього вмісту магазину
- **Celery** - для асинхронного відправлення електронних листів.
- **Postgresql** - база даних.
- **RabbitMQ** - черга завдань для Celery.
- **Nginx** - зворотній проксі сервер для перенаплавення запитів

Всі вище перераховані сервіси упаковані в doker comose.

### **Вебсервіс**

Вебсервіс виконаний на Django має наступні частини:

- Категорії з підкатегоріями
- Кталог книг з фільтрацією по ціні, автору, видавництву, типу обкладинки, мові та інших характеристиках.
- Пошук по назві та опису.
- Сторінки з інформацією: **Оплата/Доставка, Про нас, Договір публічної оферти, Політика конфіденційності, Контакти** Цю інформацію можна редагувати з адмін панелі.
- Особистий кабінет користувача.
- Зареєстрований користувач може переглянути свою історію замовлень.
- Сторінку з детальним описом книги.
- Відгуки та зірковий рейтинг до книги.
- Кошик.
- Сторінку зробити замовлення.
- Авторизацію.
- Реєстрацію.

Запустити даний додаток можна в двох режимах: **розробці**, та **продакшн**.

### Інструкція з запуску
1. Перевірити що doker і docker-compose встановлені на ПК.
2. Перевірити що git встановлено на ПК.
3. Виконати команди:
   ```
   git clone https://github.com/victor-herasimov/homebook.git
   cd homebook
   ```
4. Запуск в режимі розробки:
4.1 Створити файл **.env** в директорії **app**
4.2 Заповнити його за зразком **.env.example** aбо скопіювати код нижче:
   ```
    SECRET_KEY=j98ybtl&l(wqudy!o2x!43=htxf2c0ivr-q7wy5h!01ahn4wy!
    DEBUG=1

    DATABASE_HOST=db
    DATABASE_PORT=5432
    POSTGRES_USER=home
    POSTGRES_PASSWORD=home
    POSTGRES_DB=homebook

    CELERY_BROKER_URL=amqp://guest:guest@rabbit_mq:5672

    DEVELOP_EMAIL_SERVER=1
    MAILDEV_WEB_HOST=maildev
    MAILDEV_WEB_PORT=1025

    EMAIL_HOST=smtp.gmail.com
    EMAIL_HOST_USER=your_email@gmail.com
    EMAIL_HOST_PASSWORD=email_server_pass
    EMAIL_PORT=587
    EMAIL_USE_TLS=1
    DEFAULT_FROM_EMAIL=your_email@gmail.com

    ALLOWED_HOSTS=localhost 127.0.0.1 192.168.0.166
   ```
    Змінна **DEVELOP_EMAIL_SERVER=1** включає поштовий сервер *maildev* для розробки та відлади emails.
4.3 Перебуваючи терміналом в директорії ***homebook*** виконати команду
   ```
   docker compose up --build
   ```
   Пілсля зборки контейнерів сервіс буде доступний за адресами `http://localhost:8000` або `http://127.0.0.1:8000`.
   База даних автоматично буде заповнена тестовими даними.
5. Запуск в режимі продакшн:
5.1 В директорії **homebook** створити директорію **sets**.
5.2 В директорії **sets** створити наступні файли з секретами докер:
    1. *celery_broker_url.txt* - url до rabbitmq
        ```
        amqp://guest:guest@rabbit_mq:5672
        ```
    2. *email_host_pass.txt* - Пароль email email_host_pass
        ```
        email password
        ```
    3. *postgres_pass.txt* - Пароль для email
        ```
        password
        ```
    5.3 В директорії **sets** створити наступні скрипти:
    1. ***set_env.sh*** для встановлення змінних.
        ```sh
        #!/bin/sh

        export SECRET_KEY="j98ybtl&l(wqudy!o2x!43=htxf2c0ivr-q7wy5h!01ahn4wy!"
        export DEBUG="0"

        export DATABASE_HOST="db"
        export DATABASE_PORT="5432"
        export POSTGRES_USER="home"
        export POSTGRES_DB="homebook"

        export DEVELOP_EMAIL_SERVER="1"
        export MAILDEV_WEB_HOST="maildev"
        export MAILDEV_WEB_PORT="1025"

        export EMAIL_HOST="your smtp host"
        export EMAIL_HOST_USER="your_account@gmail.com"
        export EMAIL_PORT="587"
        export EMAIL_USE_TLS="1"

        export DEFAULT_FROM_EMAIL="your_account@gmail.com"

        export ALLOWED_HOSTS="localhost 127.0.0.1 192.168.0.166"
        export CSRF_TRUSTED_ORIGINS="http://localhost:8001 http://127.0.0.1:8001 http://192.168.0.166:8001"
        ```
    2. ***del_env.sh*** для очищення змінних
        ```sh
        #!/bin/sh

        unset SECRET_KEY
        unset DEBUG

        unset DATABASE_HOST
        unset DATABASE_PORT
        unset POSTGRES_USER
        unset POSTGRES_DB

        unset DEVELOP_EMAIL_SERVER
        unset MAILDEV_WEB_HOST
        unset MAILDEV_WEB_PORT

        unset EMAIL_HOST
        unset EMAIL_HOST_USER
        unset EMAIL_PORT
        unset EMAIL_USE_TLS
        unset DEFAULT_FROM_EMAIL

        unset ALLOWED_HOSTS
        unset CSRF_TRUSTED_ORIGINS
        ```
    5.4 Перебуваючи терміналом в директорії **homebook** виконати команди
        - `. ./sets/set_env.sh` або `source ./sets/set_env.hs`
        - `docker compose -f docker-compose.prod.yaml up --build`  


    Пілсля зборки контейнерів сервіс буде доступний за адресами `http://localhost:8001` або `http://127.0.0.1:8001`.
    База даних автоматично буде заповнена тестовими даними.


