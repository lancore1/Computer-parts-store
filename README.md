# Computer-parts-store

Проект для управління магазином комп'ютерних комплектуючих.

---

## Для колаборантів з прямим доступом

### 1. Клонування репозиторію

```bash
git clone https://github.com/lancore1/Computer-parts-store.git
cd Computer-parts-store
```

### 2. Створення і активація віртуального середовища (обов'язково)

```bash
python -m venv .venv
```

* **Windows:**

```bash
.venv\Scripts\activate
```

* **Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Встановлення бібліотек

```bash
pip install -r requirements.txt
```

---

## Внесення змін через власну гілку

1. Створити нову гілку для своєї роботи (наприклад, `feature-branch`):

```bash
git checkout -b feature-branch
```

2. Редагувати або додавати файли проекту.

3. Додати зміни до Git:

```bash
git add .
```

4. Зробити коміт:

```bash
git commit -m "Опис внесених змін"
```

5. Відправити свою гілку на GitHub:

```bash
git push origin feature-branch
```

6. На GitHub створити **Pull Request** з гілки `feature-branch` у `master` репозиторію.

   * В PR можна додати опис змін і попросити рев’ю, якщо потрібно.

7. Після мерджу PR у `master` можна видалити локальну і віддалену гілку:

```bash
git branch -d feature-branch
git push origin --delete feature-branch
```

8. Перед створенням нової гілки завжди оновлювати `master`:

```bash
git checkout master
git pull origin master
```

## Запуск проекту 

```bash
python main.py
```

---

## Примітки

* Папку `.venv` не додаємо до GitHub, вона ігнорується через `.gitignore`.
* Щоб оновити `requirements.txt` після додавання нових бібліотек:

```bash
pip freeze > requirements.txt
```

* Завжди робіть `git pull` перед новими комітами, щоб уникнути конфліктів.

---

## Контакт

* Автори: --
