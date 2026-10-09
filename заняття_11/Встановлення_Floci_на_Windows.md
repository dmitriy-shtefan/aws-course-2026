# Встановлення Floci на Windows

## Мета

Підготувати локальне середовище для практики з AWS: запустити Floci та перевірити створення S3 bucket, завантаження і отримання файлу через AWS CLI.

Floci емулює API сервісів AWS на вашому комп'ютері. Для цієї роботи AWS-акаунт і справжні ключі доступу не потрібні. Локальні ресурси не з'являються в AWS Console. Емулятор корисний для навчання, але підтримку конкретних операцій потрібно перевіряти перед перенесенням застосунку в AWS. [Документація Floci](https://github.com/floci-io/floci/tree/main).

Основний спосіб у цій інструкції: Docker Desktop з WSL 2 і Docker Compose. Git, Java та збирання Floci з вихідного коду не потрібні. Усі наведені команди виконуйте у **Windows PowerShell**, а не в Ubuntu, Git Bash або CMD. Команди вводьте по черзі; якщо крок завершується помилкою, спочатку усуньте її.

## 1. Підготовка комп'ютера

Потрібні інтернет для завантаження компонентів, підтримувана 64-бітна Windows, щонайменше 8 ГБ RAM та увімкнена апаратна віртуалізація. Для заняття рекомендовано оновлену Windows 11. Точні вимоги до поточної версії та редакції Windows перевірте на [сторінці Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/).

1. Натисніть `Win + R`, введіть `winver` і перевірте версію Windows.
2. У параметрах Windows відкрийте `System > About` і перевірте тип системи. Для Intel/AMD обирайте інсталятор Docker для `x86_64`. Для ARM використовуйте відповідний інсталятор і перевірте доступність образу Floci для вашої архітектури.
3. Відкрийте Диспетчер завдань через `Ctrl + Shift + Esc`.
4. У розділі `Performance > CPU` знайдіть `Virtualization`. Значення має бути `Enabled`.
5. Якщо віртуалізація вимкнена, увімкніть її в BIOS/UEFI за інструкцією виробника комп'ютера. Назва параметра може бути Intel Virtualization Technology, VT-x, AMD-V або SVM.

Для встановлення системних компонентів WSL можуть знадобитися права адміністратора. На навчальному комп'ютері без таких прав зверніться до адміністратора.

## 2. Встановлення WSL 2

WSL 2 забезпечує Linux-середовище, у якому Docker Desktop запускає Linux-контейнери.

Якщо WSL уже встановлено, почніть із перевірки:

```powershell
wsl --version
wsl --status
```

Для Docker потрібна WSL версії 2.1.5 або новішої. Версія пакета WSL, наприклад `2.6.x`, і версія дистрибутива в `wsl --list --verbose` є різними показниками.

Якщо WSL немає:

1. Відкрийте меню Пуск, знайдіть PowerShell.
2. Оберіть `Run as administrator`.
3. Виконайте:

```powershell
wsl --install
```

4. Перезавантажте комп'ютер.
5. Якщо відкриється Ubuntu з пропозицією створити користувача, задайте ім'я та пароль. Це локальний Linux-користувач. Під час введення пароля символи можуть не відображатися.
6. Знову відкрийте PowerShell і виконайте:

```powershell
wsl --update
wsl --set-default-version 2
wsl --version
wsl --list --verbose
```

Якщо встановлена Ubuntu має `VERSION 1`, перетворіть саме цей дистрибутив:

```powershell
wsl --set-version Ubuntu 2
```

Якщо дистрибутив має іншу назву, використайте точну назву з `wsl --list --verbose`. Надалі для цієї роботи залишайтеся у PowerShell. [Інструкція Microsoft](https://learn.microsoft.com/en-us/windows/wsl/install).

## 3. Встановлення Docker Desktop

1. Відкрийте [офіційну сторінку встановлення Docker Desktop для Windows](https://docs.docker.com/desktop/setup/install/windows-install/).
2. Завантажте інсталятор для вашої архітектури.
3. Запустіть його й оберіть WSL 2 backend, якщо інсталятор пропонує вибір.
4. Завершіть встановлення. Якщо з'явиться вимога перезавантаження, виконайте її.
5. Запустіть **Docker Desktop** з меню Пуск і дочекайтеся запуску Docker Engine.
6. У `Settings > General` перевірте `Use the WSL 2 based engine`, якщо цей параметр доступний.
7. Використовуйте **Linux containers**. Якщо меню Docker пропонує `Switch to Linux containers`, натисніть цей пункт.

Відкрийте нове звичайне вікно PowerShell і перевірте:

```powershell
docker --version
docker compose version
docker info --format '{{.OSType}}'
docker run --rm hello-world
```

Очікувані результати:

- перші дві команди показують версії Docker і Compose;
- третя команда повертає `linux`;
- остання команда завантажує тестовий образ і виводить `Hello from Docker!`.

Якщо остання команда не працює, перейдіть до розділу з помилками. До запуску Floci Docker має успішно пройти цю перевірку.

## 4. Встановлення AWS CLI v2

Якщо AWS CLI встановлено під час заняття 3, перевірте:

```powershell
aws --version
```

У відповіді має бути `aws-cli/2`. Якщо команда відсутня, завантажте [офіційний інсталятор AWS CLI для поточного користувача](https://awscli.amazonaws.com/AWSCLIV2-User.msi), запустіть його й завершіть встановлення. Закрийте та знову відкрийте PowerShell, потім повторіть перевірку.

Додаткові пояснення: [матеріал заняття 3](../заняття_3/Встановлення_AWS_CLI_на_Windows.md) та [документація AWS](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

## 5. Створення конфігурації Floci

Створіть окрему папку й перейдіть до неї:

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\aws-labs\floci" | Out-Null
Set-Location "$HOME\aws-labs\floci"
notepad compose.yaml
```

Якщо Блокнот запропонує створити файл, погодьтеся. Вставте:

```yaml
services:
  floci:
    image: floci/floci:latest
    ports:
      - "127.0.0.1:4566:4566"
    environment:
      FLOCI_STORAGE_MODE: persistent
      FLOCI_STORAGE_PERSISTENT_PATH: /app/data
    volumes:
      - floci-data:/app/data

volumes:
  floci-data:
```

Збережіть файл як **compose.yaml**, без додаткового `.txt`. У діалозі збереження оберіть тип `All files`, якщо потрібно. У YAML важливі відступи: використовуйте пробіли, а не Tab.

Пояснення конфігурації:

- `image` визначає готовий образ Floci. `latest` змінюється з виходом релізів.
- `ports` відкриває API на порту 4566 тільки через локальну адресу комп'ютера.
- `persistent` і том `floci-data` призначені для збереження локального стану між запусками.

Перевірте файл:

```powershell
Get-ChildItem
docker compose config
```

Має бути файл `compose.yaml`; друга команда має показати конфігурацію без помилок. Параметри образу та сховища описано в [README Floci](https://github.com/floci-io/floci/tree/main#configuration).

## 6. Перший запуск

У папці з `compose.yaml` виконайте:

```powershell
docker compose pull
docker compose up -d
docker compose ps
docker compose logs --tail 50 floci
```

Перший запуск потребує завантаження образу. `-d` залишає контейнер працювати у фоновому режимі. У `docker compose ps` сервіс `floci` має бути запущений, а серед портів має бути `127.0.0.1:4566`.

Перевірте доступність порту:

```powershell
Test-NetConnection -ComputerName localhost -Port 4566
```

Очікуване значення: `TcpTestSucceeded : True`. Це перевірка мережевого доступу; роботу API перевіримо наступним кроком.

## 7. Налаштування PowerShell для локального AWS

У цьому самому вікні задайте навчальні значення:

```powershell
$env:AWS_ACCESS_KEY_ID = "test"
$env:AWS_SECRET_ACCESS_KEY = "test"
$env:AWS_DEFAULT_REGION = "us-east-1"
$env:AWS_REGION = "us-east-1"
$env:AWS_ENDPOINT_URL = "http://localhost:4566"
$env:AWS_PAGER = ""
Remove-Item Env:AWS_SESSION_TOKEN -ErrorAction SilentlyContinue
```

Ці змінні діють лише у поточному PowerShell і процесах, які ви з нього запускаєте. У новому вікні потрібно повторити цей блок. Він не переписує збережені AWS-профілі. `test` є умовним локальним значенням.

У прикладах нижче додатково вказано `--endpoint-url http://localhost:4566`: так адреса призначення видима в кожній команді. Для локальної роботи залишайте цей параметр. [Правила вибору endpoint в AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-endpoints.html).

Перша перевірка API:

```powershell
aws --endpoint-url http://localhost:4566 s3api list-buckets
```

Очікується JSON із полем `Buckets`; у новому середовищі список може бути порожнім. Якщо отримано помилку, не переходьте до створення ресурсів.

## 8. Практична перевірка через S3

### Створити bucket

```powershell
aws --endpoint-url http://localhost:4566 s3 mb s3://lesson11-floci-demo
aws --endpoint-url http://localhost:4566 s3 ls
```

Очікується повідомлення `make_bucket: lesson11-floci-demo`, а потім назва bucket у списку. Під час повторного виконання використовуйте вже створений bucket або задайте іншу назву.

### Завантажити файл

```powershell
Set-Content -Path .\hello.txt -Value "Hello from lesson 11" -Encoding UTF8
aws --endpoint-url http://localhost:4566 s3 cp .\hello.txt s3://lesson11-floci-demo/hello.txt
aws --endpoint-url http://localhost:4566 s3 ls s3://lesson11-floci-demo/
```

У списку має бути `hello.txt`.

### Отримати файл назад

```powershell
aws --endpoint-url http://localhost:4566 s3 cp s3://lesson11-floci-demo/hello.txt .\downloaded-hello.txt
Get-Content .\downloaded-hello.txt
(Get-FileHash .\hello.txt).Hash -eq (Get-FileHash .\downloaded-hello.txt).Hash
```

Очікується текст `Hello from lesson 11`, а порівняння контрольних сум має повернути `True`.

### Перевірити збереження після перезапуску

```powershell
docker compose restart floci
```

Дочекайтеся запуску сервісу, потім повторіть:

```powershell
aws --endpoint-url http://localhost:4566 s3 ls s3://lesson11-floci-demo/
```

Якщо сервіс ще запускається, перевірте логи і повторіть запит. Файл `hello.txt` має залишитися у списку.

## 9. Зупинка, наступне заняття й оновлення

Усі команди Compose виконуйте з папки конфігурації:

```powershell
Set-Location "$HOME\aws-labs\floci"
```

| Дія | Команда |
| --- | --- |
| Тимчасово зупинити | `docker compose stop` |
| Запустити після зупинки | `docker compose up -d` |
| Переглянути стан | `docker compose ps` |
| Переглянути останні логи | `docker compose logs --tail 100 floci` |
| Стежити за логами | `docker compose logs -f floci` |
| Видалити контейнери та мережу, залишивши том | `docker compose down` |

`Ctrl + C` завершує перегляд логів, коли використано `logs -f`.

На наступному занятті запустіть Docker Desktop, відкрийте PowerShell, перейдіть до папки, виконайте `docker compose up -d` та повторіть блок змінних із розділу 7.

Для оновлення образу:

```powershell
docker compose pull
docker compose up -d
```

Оновлення може змінити поведінку емулятора. Для відтворюваного середовища оберіть конкретний реліз із [переліку релізів Floci](https://github.com/floci-io/floci/releases) і замініть `latest` на його тег.

**Повне очищення навчального середовища видаляє дані тому.** Виконуйте наступну команду лише коли хочете почати заново:

```powershell
docker compose down -v
```

Після цього `docker compose up -d` створить порожнє сховище.

## 10. Якщо потрібна Lambda

Базова конфігурація вище призначена для перевірки S3. Для запуску Lambda Floci потрібен доступ до Docker socket, оскільки середовище виконання функції запускається в окремому контейнері. [Docker integration у Floci](https://github.com/floci-io/floci/tree/main#real-docker-integration).

Для практики з Lambda замініть конфігурацію на:

```yaml
services:
  floci:
    image: floci/floci:latest
    ports:
      - "127.0.0.1:4566:4566"
    environment:
      FLOCI_STORAGE_MODE: persistent
      FLOCI_STORAGE_PERSISTENT_PATH: /app/data
      FLOCI_SERVICES_DOCKER_NETWORK: lesson11-floci
      FLOCI_HOSTNAME: floci
      FLOCI_BASE_URL: http://floci:4566
    volumes:
      - floci-data:/app/data
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - floci-network

volumes:
  floci-data:

networks:
  floci-network:
    name: lesson11-floci
```

Застосуйте зміни:

```powershell
docker compose config
docker compose up -d
```

Шлях `/var/run/docker.sock` належить Linux-середовищу Docker Desktop; створювати такий файл на диску Windows не потрібно. Цей mount дає Floci можливість керувати Docker-контейнерами. Налаштування мережі адаптоване з [Compose-файлу проєкту](https://github.com/floci-io/floci/blob/main/docker-compose.yml).

З PowerShell звертайтеся до `http://localhost:4566`. Із контейнерів у мережі `lesson11-floci` використовуйте `http://floci:4566`: усередині контейнера `localhost` означає сам контейнер. Для першого запуску Lambda може знадобитися інтернет для завантаження runtime-образу. Успішна перевірка S3 сама по собі не перевіряє виконання Lambda.

## 11. Типові помилки

### PowerShell не знаходить `docker` або `aws`

Закрийте PowerShell і відкрийте нове вікно після встановлення. Перевірте:

```powershell
Get-Command docker
Get-Command aws
```

Якщо команду не знайдено, перевірте завершення відповідної інсталяції. Не встановлюйте AWS CLI через `pip` замість CLI v2.

### Docker повідомляє, що не може підключитися до daemon

Запустіть Docker Desktop і дочекайтеся готовності Engine. Повторіть `docker info`. Якщо проблема залишається, перевірте WSL через `wsl --status` і повідомлення у Docker Desktop.

### WSL не запускається або встановлення зависло

Перевірте віртуалізацію та перезавантаження після встановлення. Спробуйте `wsl --update`. Якщо завантаження Ubuntu зависло на 0%, Microsoft пропонує:

```powershell
wsl --install --web-download -d Ubuntu
```

Додаткова допомога: [усунення проблем WSL](https://learn.microsoft.com/en-us/windows/wsl/troubleshooting).

### `no configuration file provided` або помилка YAML

Виконайте `Get-Location` і `Get-ChildItem`. Переконайтеся, що поточна папка містить `compose.yaml`, а не `compose.yaml.txt`. Перевірте відступи й виконайте `docker compose config`.

### Порт 4566 уже зайнятий

Знайдіть контейнер, який використовує порт:

```powershell
docker ps --format "table {{.Names}}\t{{.Ports}}"
Get-NetTCPConnection -LocalPort 4566 -State Listen -ErrorAction SilentlyContinue
```

Якщо це запущений вами LocalStack або інший Floci, зупиніть саме його. Якщо порт потрібний іншому застосунку, змініть у YAML mapping на `127.0.0.1:4567:4566`, застосуйте `docker compose up -d` і використовуйте `http://localhost:4567` у змінній endpoint та всіх командах AWS. Внутрішній порт контейнера залиште 4566.

### `Could not connect to the endpoint URL`

Перевірте:

```powershell
docker compose ps
docker compose logs --tail 100 floci
Test-NetConnection -ComputerName localhost -Port 4566
```

Переконайтеся, що адреса починається з `http://`, контейнер працює та порт збігається з конфігурацією. Якщо контейнер завершився, причина має бути в логах.

### `Unable to locate credentials`, помилка токена або регіону

Повторіть блок розділу 7 у вікні, де запускаєте AWS CLI. Перевірте наявність `--endpoint-url http://localhost:4566`. Якщо отримано помилку токена, переконайтеся, що старий `AWS_SESSION_TOKEN` видалено з поточної сесії.

### Образ не завантажується

Перевірте інтернет і налаштування proxy у Docker Desktop. Запустіть `docker compose pull` ще раз і прочитайте конкретну помилку. Використовуйте `floci/floci`, як у наведеній конфігурації.

### Bucket зник після зупинки

Перевірте `FLOCI_STORAGE_MODE: persistent` і mount `floci-data:/app/data`. Переконайтеся, що не виконували `down -v` і не змінили папку або назву Compose-проєкту: інший проєкт може отримати інший том. Не очищуйте том під час діагностики.

### Потрібно повернутися до роботи зі справжнім AWS

Закрийте навчальне вікно PowerShell і відкрийте нове. Якщо змінні задавали лише за цією інструкцією, вони не перенесуться в нову сесію. Далі використовуйте потрібний AWS-профіль. Команди з `--endpoint-url http://localhost:4566` залишаються локальними незалежно від профілю.

## 12. Критерії готовності

- [ ] WSL і Docker Desktop працюють.
- [ ] Docker використовує Linux containers, тест `hello-world` успішний.
- [ ] `aws --version` показує CLI v2.
- [ ] `docker compose config` не повідомляє про помилки.
- [ ] Сервіс Floci працює, порт 4566 доступний.
- [ ] AWS CLI показує створений локальний bucket.
- [ ] Файл завантажено й отримано назад; контрольні суми збігаються.
- [ ] Файл доступний після перезапуску Floci.

Для підтвердження виконання можна зберегти знімки результатів `docker compose ps`, списку файлів у bucket та порівняння контрольних сум. На знімках не показуйте справжні ключі AWS.

Джерела перевірено 9 жовтня 2026 року. Команди розраховані на PowerShell; назви елементів інсталятора можуть змінюватися з новими версіями.
