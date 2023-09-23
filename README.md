# Bug Busters
# Ссылка на проект https://drive.google.com/drive/folders/1eBNeN2cturPsuuKxUnjogRjBzkacvU-a
ИНФО
---------
# Мы представляем программное обеспечение для поиска и идентификации деталей и узлов "DetailHunter", при помощи которой пользователь сможет распознать покрашенную деталь и получить дополнительную информацию о ней, благодаря использованию машинного обучения и компьютерного зрения в решении этой задачи.
--------


ЗАПУСК
--------
Сервер с моделью:
1) Скачиваем и открываем папку ml_serv
2) Устанавливаем библиотеки из requirements.txt (pip install -r requirements.txt)
3) Скачиваем папку mdl из Google Drive (https://drive.google.com/drive/folders/1ldgy6HGPNlm93mqLo4_68_CBdkaVIRtN)
4) Создаем папку app в ml_serv и помещаем в нее папку mdl (ml_serv/app/mdl)
5) Запускаем файл main.py

Мобильное приложение: 
1) Необходио клонировать проект с репозитория https://github.com/maksimov-m/test_detect
2) Открыть проект в Microsoft Visual Studio (test_detect.sln)
3) Выбрать для запуска либо свой телефон, либо Android Emulator
4) Запустить проект

Телеграм бот:
1) Скачиваем папку telegram_bot
2) Запускаем бота при помощи Docker:
   - docker build --tag 'tg_serv'
   - docker run --detach 'tg_serv'
4) Открыть телеграм бота https://t.me/praktitest2009bot 
--------


РАБОТА
--------------
Мобильное приложение: 
1) Наведите камеру на деталь и нажмите на кнопку
2) После нажатия Вам будет показано фото, с выделенными деталями, а снизу будут расписаны их характеристики.

Телеграм бот:
1) Пропишите команду /start
2) Отправьте фотографию детали
3) После отправки, бот пришлет Вам описание полученной детали
--------------


ДЕМО
--------------
Записи примера работы с сервисом
[https://drive.google.com/drive/folders/1WSsDSsEsTFP42RS12bbCDLrwvDPBphmX?usp=sharing](https://drive.google.com/drive/folders/1eBNeN2cturPsuuKxUnjogRjBzkacvU-a)
--------------




ПОМОЩЬ
------------
За помощью по установке и использованию проекта можно обратиться в телеграмме:
1) Галицков Богдан @boginc
2) Максимов Максим @maks_maks1
3) Ахунов Олег @olicrab
4) Хазиев Равиль @HAHRAH
--------------

