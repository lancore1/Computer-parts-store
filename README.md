# Computer-parts-store

Проект для управління магазином комп'ютерних комплектуючих.

---

## Для колаборантів з прямим доступом

### 1. Клонування репозиторію

```bash
git clone https://github.com/lancore1/Computer-parts-store.git
cd Computer-parts-store
```

### 2. Створення і активація віртуального середовища

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

## Внесення змін

1. Редагувати або додавати файли проекту.
2. Додати зміни до Git:

```bash
git add .
```

3. Зробити коміт:

```bash
git commit -m "Опис змін"
```

4. Перед пушем отримати останні зміни з репозиторію, щоб уникнути конфліктів:

```bash
git pull origin main
```

5. Відправити зміни на GitHub:

```bash
git push origin main
```

---

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
