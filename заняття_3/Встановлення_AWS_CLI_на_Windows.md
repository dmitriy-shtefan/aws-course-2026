# Встановлення AWS CLI на Windows

AWS CLI дає змогу працювати з AWS через команди в терміналі. Для встановлення потрібна підтримувана 64-бітна
версія Windows. AWS-акаунт і ключі доступу на цьому етапі не потрібні.

## 1. Встановити AWS CLI

Відкрити **PowerShell** і виконати офіційну команду AWS:

```powershell
irm https://awscli.amazonaws.com/v2/install.ps1 | iex
```

Інсталятор встановлює AWS CLI для поточного користувача; права адміністратора не потрібні.

Якщо зручніше встановлювати через вікно інсталятора, завантажити й запустити
[AWSCLIV2-User.msi](https://awscli.amazonaws.com/AWSCLIV2-User.msi) замість команди вище.

## 2. Перевірити встановлення

Закрити й знову відкрити PowerShell. Виконати:

```powershell
aws --version
```

У відповіді має бути `aws-cli/2...`. Якщо PowerShell не знаходить команду `aws`, ще раз відкрити нове вікно
PowerShell і скористатися
[інструкцією AWS з усунення помилки](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-troubleshooting.html).

Джерело:
[інструкція AWS CLI для Windows](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
