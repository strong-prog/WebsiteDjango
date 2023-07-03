# тестовое задание (интернет-магазин)

## Реализовано
1. Базова часть
   -
   - Django Модель Item с полями (name, description, price) 
   - API с двумя методами:
     - GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса
     - GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее  с помощью JS библиотеки Stripe происходить редирект на Checkout форму
2. Дополнительно
   -
   - Просмотр Django Моделей в Django Admin панели
   - Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
   - Модели Discount и Tax, в которых высчитывается скидка и налог для User_id и связывается с соответствующими атрибутами при создании платежа в Stripe и корректно отображаются в Stripe Checkout форме.
   - Запуск приложения на удаленном сервере, доступном для тестирования
   - Автоматический deploy на сервер через ci/cd

## Инструкция по быстрому запуску на Linux/Ubuntu

```
mkdir ~/testproject
cd ~/testproject
git clone https://gitlab.com/strong.tretyakov/test-project2
cd test-project2/payment
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

## Демо
http://sportnote.ru/

