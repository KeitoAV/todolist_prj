## Дипломный проект. Курс "Python-разработчик".

### Цель проекта: создать web-приложение — планировщик задач.

#### Для запуска проекта необходимо:

1. скопировать репозиторий - 'git clone https://github.com/KeitoAV/todolist_prj.git'
2. создать виртуальное окружение;
3. 'pip install -r requirements.txt' - установить зависимости;
4. создать файл .env и заполнить в нём переменные окружения, как в .env.example;
5. 'docker-compose up -d' - запустить проект.

### Этапы реализации проекта.

#### 1. Работа с БД + Django-admin.

Стек (python 3.10, Django 4.0.1, Postgres).

Подготовка проекта и настройка всех необходимых системных компонентов для дальнейшей работы:

- создание проекта 'todolist',
- настройка зависимостей 'pip install -r requirements.txt',
- настройка файла конфигурации '.env',
- создано приложение 'core',
- создана кастомная модель пользователя core/models.py - User(AbstractUser),
- настроено подключение к базе данных:
    - docker run --name todolist_project -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres;
    - python manage.py makemigrations;
    - python manage.py migrate.


- добавлена модель пользователя в Django admin:
    - python manage.py createsuperuser;
    - python manage.py runserver.

#### 2. Deploy.

frontend - image: sermalenk/skypro-front:lesson-34

Настроена автоматическая сборка и деплой приложения на сервер:

- создан Dockerfile,
- создан docker-compose.yaml,
- создан файл .github/actions/action.yaml.

#### 3. Аутентификация и авторизация. OAuth2.0.

frontend - image: sermalenk/skypro-front:lesson-35

В приложении 'core' реализованы следующие функции:

- регистрация,
- вход/выход,
- получение и обновление профиля,
- смена пароля,
- вход через социальную сеть VK.


 #### 4. REST API для веб-интерфейса целей.

frontend - image: sermalenk/skypro-front:lesson-36

- Создано приложение 'goals', в котором графический интерфейс пользователя для работы с целями представляет из себя доску, где каждая цель — это карточка на данной доске.
- Реализованы все методы API, которые представлены в swagger - http://51.250.69.194:8080/api/swagger/.
- В models.py созданы модели - GoalCategory, Goal, GoalComment.
- Добавлен файл filters.py для реализации фильтрации в списке целей (по названию, категории/категориям, приоритету/приоритетам, статусу, дате дедлайна (от/до)).
- Создана админка для категорий, целей, комментариев.

Приложение состоит из:
1. Категорий, которые можно создавать, редактировать, удалять/архивировать. Есть возможность просматривать список всех категорий и имеющиеся цели в каждой категории.

2. Целей, которые делятся на 3 колонки по статусам (к выполнению, в работе, выполнено). Цели можно создавать, редактировать, удалять/архивировать. Для цели есть возможность добавить комментарий, отредактировать его, удалить.
Добавлены функции сортировки, фильтрации и поиска. В каждой карточке цели можно увидеть: название цели, приоритет, дату дедлайна, категорию, дату создания/обновления, комментарий, статус.


#### 5. Шеринг доски.

frontend - image: sermalenk/skypro-front:lesson-37

- В приложение 'goals' добавлен функционал «шеринга» доски, чтобы пользователи могли совместно редактировать/просматривать наборы целей.
- В models.py добавлены две модели - Board,  BoardParticipant, в модели GoalCategory добавлено новое поле board.
- Реализованы все методы API, которые представлены в swagger - http://51.250.69.194:8080/api/swagger/.
- Создан файл permissions.py для управления доступами пользователей (владелец, редактор, читатель).
- Создана админка для доски.

#### 6. Телеграм-бот.

frontend - image: sermalenk/skypro-front:lesson-38

Создан бот (приложение 'bot'), который требует подтверждение аккаунта в написанном приложении и через которого можно получать и создавать цели.

- Можно выполнить запрос /bot/verify с помощью swagger.
- При некорректном verification_code метод возвращает ошибку.
- Бот присылает сообщение, в котором содержится случайная последовательность символов для верификации бота на сайте.
- При корректном verification_code метод должен вернуть HTTP-статус 200 и прислать сообщение в Telegram об успешной связке.
- Метод должен быть доступен только авторизованными пользователям.
- Случайная последовательность символов хранится в verification_code в модели TgUser.
- С помощью команды /goals можно получить список целей (для каждой цели можно увидеть - её название, категорию, статус, дедлайн), если целей нет бот вернёт сообщение "Нет задач".
- С помощью команды /create можно создать цель, созданную цель можно найти в списке в приложении (с указанием, что цель была создана в Telegram).
- Для отмены реализована команда /cancel.
- Добавлена секция bot в docker-compose.yaml файл.
- При написании сообщения в Telegram бот отвечает пользователю.
