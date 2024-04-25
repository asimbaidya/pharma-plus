# pharma-plus

## Tentative Features List for Medicine Delivery Dystem

- [x] 0.1 Flask Project structured flowing(enforcing) MVC pattern

```text
├── models // => M
│   ├── other.py
│   ├── product.py
│   └── user.py
├── templates // [View] => V
│   ├── about.html
│   ├── components
│   │   ├── flash.html
│   │   ├── layout.html
│   │   ├── nav.html
│   │   └── user-admin.html
│   ├── home.html
│   ├── login.html
│   ├── product-add.html
│   ├── product-browser.html
│   ├── product.html
│   ├── register.html
│   ├── search.html
│   └── user.html
├── controllers // [+router] => C
│   ├── pharma_plus.py
│   ├── products.py
│   ├── search.py
│   └── users.py
```

## Setup(once)

```sh
# 1. Clone repository
git clone https://github.com/asimbaidya/pharma-plus.git
```

```sh
# 2. Create virtual environment using pipenv and login to it
pipenv shell
```

```sh
# 3.  Install the dependencies
pipenv install
```

```sh
# 4. Create tables and populate with dummy data(add more dummy data)
python3 dummy-data-generator/main.py

```

```sh
# 5. Install node dependencies
npm install
```

## running(two terminal instances/tab/etc)

```sh
# 6. Run tailwind watcher
npm run tailwind
```

```sh
# 7. Run the server

python3  run.py
```
