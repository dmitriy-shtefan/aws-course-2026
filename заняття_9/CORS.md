# Мініпрактика по CORS

## Мета

Навчитися визначати:

1. чи є запит cross-origin;
2. чи виконає браузер preflight-запит `OPTIONS`;
3. чи дозволить браузер JavaScript прочитати відповідь.

## Інструкція

Для кожної ситуації дайте три короткі відповіді:

1. **Same-origin чи cross-origin?**
2. **Чи потрібен preflight `OPTIONS`?**
3. **Чи отримає JavaScript доступ до відповіді? Чому?**

### Ситуація 1. Інший порт

Сторінка відкрита за адресою:

```text
http://localhost:3000
```

JavaScript виконує запит:

```http
GET http://localhost:8080/students
```

API повертає:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[{"name":"Олена"}]
```

### Ситуація 2. Дозволений origin

Сторінка відкрита за адресою:

```text
https://app.example.com
```

JavaScript надсилає:

```http
POST https://api.example.com/notes
Content-Type: application/json

{"text":"Вивчити CORS"}
```

На preflight-запит API відповідає:

```http
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: POST
Access-Control-Allow-Headers: Content-Type
```

Основний `POST` повертає:

```http
HTTP/1.1 201 Created
Access-Control-Allow-Origin: https://app.example.com
Content-Type: application/json

{"id":7,"text":"Вивчити CORS"}
```

### Ситуація 3. Метод не дозволений

Сторінка відкрита за адресою:

```text
https://app.example.com
```

JavaScript надсилає:

```http
DELETE https://api.example.com/notes/7
```

На preflight-запит API відповідає:

```http
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET,POST
```

## Завдання на виправлення

Змініть **один заголовок** у кожній невдалій ситуації так, щоб браузер дозволив JavaScript прочитати відповідь або виконати запит.
