# Лабораторная работа #1

![GitHub Classroom Workflow](../../workflows/GitHub%20Classroom%20Workflow/badge.svg?branch=master)

## Continuous Integration & Continuous Delivery

### Формулировка

В рамках первой лабораторной работы требуется написать простейшее веб-приложение, предоставляющее пользователю набор операций над сущностью `Person`. Для этого приложения необходимо автоматизировать процесс сборки, тестирования и доставки Docker-образа с использованием GitHub Actions.

В данной реализации вместо Heroku для доставки Docker-образа используется **GitHub Container Registry (GHCR)**.

Приложение реализует API:

* `GET /persons/{personId}` – информация о человеке;
* `GET /persons` – информация по всем людям;
* `POST /persons` – создание новой записи о человеке;
* `PATCH /persons/{personId}` – обновление существующей записи о человеке;
* `DELETE /persons/{personId}` – удаление записи о человеке.

[Описание API](person-service.yaml) в формате OpenAPI.

### Требования

* Исходный проект хранится на GitHub. Для сборки и автоматизации CI/CD используется только [GitHub Actions](https://docs.github.com/en/actions).

* Запросы / ответы должны быть в формате JSON.

* Если запись по id не найдена, необходимо возвращать HTTP статус `404 Not Found`.

* При создании новой записи о человеке методом `POST /persons` необходимо возвращать HTTP статус `201 Created` с пустым телом и Header:
  `Location: /api/v1/persons/{personId}`,
  где `personId` – id созданной записи.

* Приложение должно содержать 4-5 unit-тестов на реализованные операции.

* Приложение должно быть завернуто в Docker.

* Сборка Docker-образа и его доставка должны выполняться средствами GitHub Actions.

* Docker-образ после успешного прохождения тестов публикуется в GitHub Container Registry (GHCR).

* В [build.yml](.github/workflows/classroom.yml) должны быть реализованы шаги:

  * установка зависимостей;
  * запуск базы данных;
  * запуск unit-тестов;
  * сборка Docker-образа;
  * публикация Docker-образа в GHCR.

* Приложение должно использовать БД для хранения записей.

### Реализация CI/CD

Процесс GitHub Actions выполняется автоматически после `push` в ветку `master`.

Основные этапы:

1. Checkout исходного кода.
2. Установка Python и зависимостей.
3. Запуск PostgreSQL.
4. Запуск unit-тестов.
5. Сборка Docker-образа.
6. Авторизация в GitHub Container Registry.
7. Публикация Docker-образа в GHCR.

Таким образом:

**Continuous Integration (CI)** включает автоматическую сборку проекта и выполнение unit-тестов.

**Continuous Delivery (CD)** включает автоматическую сборку Docker-образа и его публикацию в GitHub Container Registry после успешного прохождения тестов.

### Пояснения

* Для локальной разработки используется PostgreSQL в Docker. Для запуска необходимо выполнить:

```bash
docker compose up -d
```

Поднимается контейнер с PostgreSQL 13, создаётся БД `persons` и пользователь `program:test`.

* Для запуска приложения локально используется Docker Compose.

* Локальные интеграционные тесты можно выполнить через Newman. Для этого необходимо запустить приложение и импортировать в Postman:

  * коллекцию `[inst] Lab1.postman_collection.json`;
  * environment `[inst][local] Lab1.postman_environment.json`.

* Docker-образ публикуется в GitHub Container Registry в формате:

```text
ghcr.io/<github-user>/<repository>:latest
```

* GitHub Actions использует встроенный `GITHUB_TOKEN` для публикации Docker-образа в GHCR.

* Для поиска необходимых инструментов автоматизации можно использовать [GitHub Marketplace](https://github.com/marketplace).

### Прием задания

1. Исходный проект размещается в GitHub.
2. После выполнения `push` в ветку `master` автоматически запускается GitHub Actions.
3. Workflow выполняет сборку проекта и unit-тесты.
4. После успешного прохождения тестов автоматически собирается Docker-образ.
5. Docker-образ публикуется в GitHub Container Registry.
6. Успешное завершение workflow подтверждает корректную работу CI/CD pipeline.

### Результат

В результате выполнения лабораторной работы реализованы:

* REST API для работы с сущностью `Person`;
* PostgreSQL для хранения данных;
* 5 unit-тестов;
* Docker-контейнеризация приложения;
* автоматическая сборка и тестирование через GitHub Actions;
* автоматическая публикация Docker-образа в GitHub Container Registry.
