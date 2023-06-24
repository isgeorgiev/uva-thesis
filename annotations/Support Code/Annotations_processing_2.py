"""
Script for processing and cleaning the google drive annotations.
The output is a simple .csv file with the acronyms and expansions per document.
Date: 17-05-2022
"""
# dependencies
import os
import pandas as pd
import re

"""
train --> "acronym": 20, "expansion": "secrecy rate", "id": "TR-0", "tokens":[]
test --> "acronym": 34, "id": "TS-0", "tokens": ["Experiment", "2", ":"

To do's: create test and train sets 
"""

rootdir = 'D:/University/Thesis/annotations/annotations'
df = pd.DataFrame(columns=['acronym', 'expansion', 'language', 'type'])

annotations = [
    "Conus_eugrammatus_dsgeorgiev90@yahoo.com.json-15 Oct 2022, 14:16:23",
    "Conus_eugrammatus_violeta.todorovaaa@gmail.com.json-15 Oct 2022, 18:28:53",
    "JavaScript_contact@iliyasgeorgiev.com.json-2 Jun 2022, 14:40:52",
    "JavaScript_petya.stoyanovaaaa@gmail.com.json-21 May 2022, 15:47:17",
    "UML_contact@iliyasgeorgiev.com.json-16 May 2022, 10:32:40",
    "UML_dsgeorgiev90@yahoo.com.json-13 May 2022, 23:37:05",
    "Административен_акт_g.yordanov999@gmail.com.json-29 Jun 2022, 13:16:50",
    "Административен_акт_violeta.todorovaaa@gmail.com.json-6 Jul 2022, 00:23:25",
    "Акционерно_дружество_dsgeorgiev90@yahoo.com.json-9 May 2022, 21:52:52",
    "Акционерно_дружество_stella.vouteva@gmail.com.json-9 May 2022, 21:49:03",
    "Американска_психологична_асоциация_dsgeorgiev90@yahoo.com.json-11 May 2022, 22:56:57",
    "Американска_психологична_асоциация_georgitidorov4508@gmail.com.json-12 May 2022, 21:03:03",
    "Амстердамски_университет_dsgeorgiev90@yahoo.com.json-15 Oct 2022, 13:51:08",
    "Амстердамски_университет_violeta.todorovaaa@gmail.com.json-14 Oct 2022, 17:55:38",
    "БНТ_1_dsgeorgiev90@yahoo.com.json-15 Oct 2022, 14:00:27",
    "БНТ_1_violeta.todorovaaa@gmail.com.json-15 Oct 2022, 18:20:03",
    "БНТ_2_dsgeorgiev90@yahoo.com.json-15 Oct 2022, 13:58:08",
    "БНТ_2_violeta.todorovaaa@gmail.com.json-14 Oct 2022, 18:12:12",
    "Банкова_консолидационна_компания_dsgeorgiev90@yahoo.com.json-9 May 2022, 21:52:03",
    "Банкова_консолидационна_компания_stella.vouteva@gmail.com.json-9 May 2022, 21:48:21",
    "Баркод_g.yordanov999@gmail.com.json-22 Jun 2022, 01:10:40",
    "Баркод_petya.stoyanovaaaa@gmail.com.json-20 Jun 2022, 17:56:17",
    "Берлин_dsgeorgiev90@yahoo.com.json-15 Oct 2022, 14:13:54",
    "Берлин_violeta.todorovaaa@gmail.com.json-15 Oct 2022, 18:25:42",
    "Би_Би_Си_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:46:40",
    "Би_Би_Си_petya.stoyanovaaaa@gmail.com.json-20 Oct 2022, 01:08:01",
    "Би_Ти_Ви_dsgeorgiev90@yahoo.com.json-15 Oct 2022, 13:56:29",
    "Би_Ти_Ви_violeta.todorovaaa@gmail.com.json-14 Oct 2022, 18:06:43",
    "Бобслей_contact@iliyasgeorgiev.com.json-8 May 2022, 22:19:53",
    "Бобслей_violeta.todorovaaa@gmail.com.json-9 May 2022, 10:57:07",
    "Ботаника_dsgeorgiev90@yahoo.com.json-28 Jun 2022, 23:14:07",
    "Ботаника_violeta.todorovaaa@gmail.com.json-22 Jun 2022, 13:47:42",
    "Българска_народна_банка_stella.vouteva@gmail.com.json-9 May 2022, 21:31:09",
    "Българска_народна_банка_violeta.todorovaaa@gmail.com.json-9 May 2022, 17:05:33",
    "Българска_социалистическа_партия_dsgeorgiev90@yahoo.com.json-9 May 2022, 21:24:11",
    "Българска_социалистическа_партия_violeta.todorovaaa@gmail.com.json-9 May 2022, 15:45:32",
    "Васил_Левски_dsgeorgiev90@yahoo.com.json-9 May 2022, 22:57:44",
    "Васил_Левски_stella.vouteva@gmail.com.json-9 May 2022, 22:25:28",
    "Водноелектрическа_централа_g.yordanov999@gmail.com.json-28 Oct 2022, 01:03:28",
    "Водноелектрическа_централа_georgitidorov4508@gmail.com.json-20 Oct 2022, 02:18:24",
    "Волейбол_stella.vouteva@gmail.com.json-9 May 2022, 16:33:43",
    "Волейбол_violeta.todorovaaa@gmail.com.json-9 May 2022, 12:07:51",
    "Временно_руско_управление_dsgeorgiev90@yahoo.com.json-9 May 2022, 21:46:13",
    "Временно_руско_управление_stella.vouteva@gmail.com.json-9 May 2022, 21:43:12",
    "Гъвкав_магнитен_диск_g.yordanov999@gmail.com.json-21 Jun 2022, 18:13:58",
    "Гъвкав_магнитен_диск_petya.stoyanovaaaa@gmail.com.json-2 Jun 2022, 15:40:49",
    "Дисниленд_dsgeorgiev90@yahoo.com.json-11 May 2022, 23:28:49",
    "Дисниленд_georgitidorov4508@gmail.com.json-12 May 2022, 21:23:36",
    "Драйвер_g.yordanov999@gmail.com.json-3 Jun 2022, 19:15:51",
    "Драйвер_petya.stoyanovaaaa@gmail.com.json-2 Jun 2022, 15:34:11",
    "Дуги_оток_petya.stoyanovaaaa@gmail.com.json-23 Jun 2022, 16:53:37",
    "Дуги_оток_violeta.todorovaaa@gmail.com.json-22 Jun 2022, 13:44:58",
    "Държавен_вестник_g.yordanov999@gmail.com.json-29 Jun 2022, 13:15:05",
    "Държавен_вестник_violeta.todorovaaa@gmail.com.json-6 Jul 2022, 00:21:04",
    "Държавен_съвет_на_Народна_република_България_dsgeorgiev90@yahoo.com.json-9 May 2022, 21:58:01",
    "Държавен_съвет_на_Народна_република_България_stella.vouteva@gmail.com.json-9 May 2022, 21:53:11",
    "Европейска_централна_банка_dsgeorgiev90@yahoo.com.json-11 May 2022, 22:50:41",
    "Европейска_централна_банка_petya.stoyanovaaaa@gmail.com.json-12 May 2022, 00:32:01",
    "Железният_човек_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:29:36",
    "Железният_човек_petya.stoyanovaaaa@gmail.com.json-19 Oct 2022, 23:50:54",
    "Закон_за_трудовата_поземлена_собственост_g.yordanov999@gmail.com.json-28 Oct 2022, 01:04:48",
    "Закон_за_трудовата_поземлена_собственост_georgitidorov4508@gmail.com.json-20 Oct 2022, 02:21:36",
    "Златен_глобус_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:36:17",
    "Златен_глобус_petya.stoyanovaaaa@gmail.com.json-20 Oct 2022, 00:52:55",
    "Иван_Славков_dsgeorgiev90@yahoo.com.json-6 Jul 2022, 00:39:09",
    "Иван_Славков_g.yordanov999@gmail.com.json-29 Jun 2022, 13:38:24",
    "Изобразително_изкуство_dsgeorgiev90@yahoo.com.json-13 May 2022, 23:05:45",
    "Изобразително_изкуство_georgitidorov4508@gmail.com.json-12 May 2022, 21:40:52",
    "Интегрална_схема_georgitidorov4508@gmail.com.json-10 May 2022, 20:30:39",
    "Интегрална_схема_violeta.todorovaaa@gmail.com.json-10 May 2022, 20:19:56",
    "Интел_dsgeorgiev90@yahoo.com.json-11 May 2022, 21:48:15",
    "Интел_georgitidorov4508@gmail.com.json-10 May 2022, 22:24:10",
    "Ирландия_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:57:55",
    "Ирландия_petya.stoyanovaaaa@gmail.com.json-20 Oct 2022, 01:28:40",
    "Капитан_Америка_dsgeorgiev90@yahoo.com.json-15 Oct 2022, 14:20:31",
    "Капитан_Америка_petya.stoyanovaaaa@gmail.com.json-19 Oct 2022, 23:47:27",
    "Княжество_България_dsgeorgiev90@yahoo.com.json-9 May 2022, 21:40:09",
    "Княжество_България_stella.vouteva@gmail.com.json-9 May 2022, 21:40:06",
    "Конституционен_съд_на_България_g.yordanov999@gmail.com.json-29 Jun 2022, 13:20:57",
    "Конституционен_съд_на_България_violeta.todorovaaa@gmail.com.json-6 Jul 2022, 00:26:08",
    "Крис_Евънс_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:32:26",
    "Крис_Евънс_petya.stoyanovaaaa@gmail.com.json-19 Oct 2022, 23:55:41",
    "Леброн_Джеймс_dsgeorgiev90@yahoo.com.json-20 Jun 2022, 14:13:01",
    "Леброн_Джеймс_petya.stoyanovaaaa@gmail.com.json-20 Jun 2022, 14:52:56",
    "Лека_атлетика_stella.vouteva@gmail.com.json-9 May 2022, 21:14:26",
    "Лека_атлетика_violeta.todorovaaa@gmail.com.json-9 May 2022, 15:32:58",
    "Лилав_цвят_contact@iliyasgeorgiev.com.json-13 May 2022, 11:39:28",
    "Лилав_цвят_georgitidorov4508@gmail.com.json-12 May 2022, 21:30:26",
    "Лукойл_Нефтохим_Бургас_g.yordanov999@gmail.com.json-28 Oct 2022, 01:07:09",
    "Лукойл_Нефтохим_Бургас_georgitidorov4508@gmail.com.json-20 Oct 2022, 02:25:03",
    "Майкъл_Фелпс_petya.stoyanovaaaa@gmail.com.json-20 Jun 2022, 15:19:25",
    "Майкъл_Фелпс_violeta.todorovaaa@gmail.com.json-8 May 2022, 23:58:47",
    "Марк_Ръфало_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:33:03",
    "Марк_Ръфало_petya.stoyanovaaaa@gmail.com.json-19 Oct 2022, 23:57:34",
    "Международна_автомобилна_федерация_g.yordanov999@gmail.com.json-29 Jun 2022, 12:59:36",
    "Международна_автомобилна_федерация_petya.stoyanovaaaa@gmail.com.json-29 Jun 2022, 14:38:13",
    "Метро_Груп_dsgeorgiev90@yahoo.com.json-28 Jun 2022, 23:28:48",
    "Метро_Груп_violeta.todorovaaa@gmail.com.json-22 Jun 2022, 13:57:38",
    "Микроелектроника_dsgeorgiev90@yahoo.com.json-11 May 2022, 21:02:",
    "Микроелектроника_georgitidorov4508@gmail.com.json-10 May 2022, 20:34:32",
    "Микропроцесор_dsgeorgiev90@yahoo.com.json-10 May 2022, 00:21:01",
    "Микропроцесор_petya.stoyanovaaaa@gmail.com.json-20 Jun 2022, 15:37:33",
    "Мила_Кунис_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:43:41",
    "Мила_Кунис_petya.stoyanovaaaa@gmail.com.json-20 Oct 2022, 00:56:38",
    "Министерство_на_външните_работи_на_България_g.yordanov999@gmail.com.json-29 Jun 2022, 13:13:19",
    "Министерство_на_външните_работи_на_България_violeta.todorovaaa@gmail.com.json-6 Jul 2022, 00:12:34",
    "Мобилно_устройство_dsgeorgiev90@yahoo.com.json-28 Jun 2022, 23:35:07",
    "Мобилно_устройство_violeta.todorovaaa@gmail.com.json-22 Jun 2022, 14:02:26",
    "Модерно_семейство_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:45:08",
    "Модерно_семейство_petya.stoyanovaaaa@gmail.com.json-20 Oct 2022, 01:06:37",
    "Музикален_продуцент_dsgeorgiev90@yahoo.com.json-15 Oct 2022, 14:17:54",
    "Музикален_продуцент_violeta.todorovaaa@gmail.com.json-15 Oct 2022, 18:30:07",
    "НАТО_g.yordanov999@gmail.com.json-28 Oct 2022, 01:00:51",
    "НАТО_georgitidorov4508@gmail.com.json-20 Oct 2022, 02:15:36",
    "Награди_на_филмовата_академия_на_САЩ_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:42:01",
    "Награди_на_филмовата_академия_на_САЩ_petya.stoyanovaaaa@gmail.com.json-20 Oct 2022, 00:54:40",
    "Народно_събрание_stella.vouteva@gmail.com.json-9 May 2022, 21:23:03",
    "Народно_събрание_violeta.todorovaaa@gmail.com.json-9 May 2022, 16:54:03",
    "Национална_баскетболна_асоциация_dsgeorgiev90@yahoo.com.json-20 Jun 2022, 14:18:52",
    "Национална_баскетболна_асоциация_petya.stoyanovaaaa@gmail.com.json-20 Jun 2022, 14:58:25",
    "Нетфликс_dsgeorgiev90@yahoo.com.json-11 May 2022, 23:22:49",
    "Нетфликс_georgitidorov4508@gmail.com.json-12 May 2022, 21:22:03",
    "Оксфордски_университет_g.yordanov999@gmail.com.json-3 Jun 2022, 19:14:00",
    "Оксфордски_университет_petya.stoyanovaaaa@gmail.com.json-2 Jun 2022, 15:29:26",
    "Октомврийска_революция_stella.vouteva@gmail.com.json-9 May 2022, 21:34:13",
    "Октомврийска_революция_violeta.todorovaaa@gmail.com.json-9 May 2022, 20:11:10",
    "Олимпийски_игри_petya.stoyanovaaaa@gmail.com.json-20 Jun 2022, 15:07:20",
    "Олимпийски_игри_violeta.todorovaaa@gmail.com.json-8 May 2022, 23:53:04",
    "Операционна_система_dsgeorgiev90@yahoo.com.json-15 May 2022, 13:46:02",
    "Операционна_система_petya.stoyanovaaaa@gmail.com.json-21 May 2022, 15:40:10",
    "Орден_на_Британската_империя_g.yordanov999@gmail.com.json-3 Jun 2022, 19:07:42",
    "Орден_на_Британската_империя_petya.stoyanovaaaa@gmail.com.json-2 Jun 2022, 15:23:09",
    "Остромила_dsgeorgiev90@yahoo.com.json-11 May 2022, 23:20:30",
    "Остромила_georgitidorov4508@gmail.com.json-12 May 2022, 21:17:26",
    "Открито_първенство_на_Франция_petya.stoyanovaaaa@gmail.com.json-20 Jun 2022, 14:59:07",
    "Открито_първенство_на_Франция_violeta.todorovaaa@gmail.com.json-8 May 2022, 23:36:10",
    "Пейо_Яворов_dsgeorgiev90@yahoo.com.json-9 May 2022, 22:02:25",
    "Пейо_Яворов_stella.vouteva@gmail.com.json-9 May 2022, 22:00:02",
    "Планова_икономика_dsgeorgiev90@yahoo.com.json-9 May 2022, 21:34:50",
    "Планова_икономика_violeta.todorovaaa@gmail.com.json-9 May 2022, 17:13:02",
    "Пловдивски_университет_dsgeorgiev90@yahoo.com.json-15 Oct 2022, 13:45:47",
    "Пловдивски_университет_violeta.todorovaaa@gmail.com.json-14 Oct 2022, 17:41:18",
    "Практикер_dsgeorgiev90@yahoo.com.json-28 Jun 2022, 23:23:22",
    "Практикер_violeta.todorovaaa@gmail.com.json-22 Jun 2022, 13:51:22",
    "Програмна_грешка_g.yordanov999@gmail.com.json-21 Jun 2022, 18:09:32",
    "Програмна_грешка_petya.stoyanovaaaa@gmail.com.json-21 May 2022, 15:41:34",
    "Прототип_dsgeorgiev90@yahoo.com.json-13 May 2022, 23:40:29",
    "Прототип_petya.stoyanovaaaa@gmail.com.json-20 Jun 2022, 15:38:42",
    "Реклама_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:48:26",
    "Реклама_petya.stoyanovaaaa@gmail.com.json-20 Oct 2022, 01:14:23",
    "Република_Кипър_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:54:33",
    "Република_Кипър_petya.stoyanovaaaa@gmail.com.json-20 Oct 2022, 01:22:54",
    "Робърт_Дауни_Джуниър_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:31:48",
    "Робърт_Дауни_Джуниър_petya.stoyanovaaaa@gmail.com.json-19 Oct 2022, 23:54:26",
    "Сам_вкъщи_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:35:36",
    "Сам_вкъщи_petya.stoyanovaaaa@gmail.com.json-20 Oct 2022, 00:51:27",
    "Световна_организация_за_интелектуална_собственост_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:52:19",
    "Световна_организация_за_интелектуална_собственост_petya.stoyanovaaaa@gmail.com.json-20 Oct 2022, 01:18:49",
    "Силициева_долина_dsgeorgiev90@yahoo.com.json-11 May 2022, 21:19:04",
    "Силициева_долина_georgitidorov4508@gmail.com.json-10 May 2022, 21:39:49",
    "Скарлет_Йохансон_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:34:02",
    "Скарлет_Йохансон_petya.stoyanovaaaa@gmail.com.json-20 Oct 2022, 00:50:45",
    "Софтуер_с_отворен_код_dsgeorgiev90@yahoo.com.json-29 Jun 2022, 00:08:05",
    "Софтуер_с_отворен_код_g.yordanov999@gmail.com.json-29 Jun 2022, 12:36:52",
    "Старокаменна_епоха_dsgeorgiev90@yahoo.com.json-28 Jun 2022, 23:11:22",
    "Старокаменна_епоха_violeta.todorovaaa@gmail.com.json-22 Jun 2022, 13:46:00",
    "Стефка_Костадинова_dsgeorgiev90@yahoo.com.json-15 Oct 2022, 13:39:16",
    "Стефка_Костадинова_violeta.todorovaaa@gmail.com.json-14 Oct 2022, 17:32:19",
    "Стокхолмски_синдром_dsgeorgiev90@yahoo.com.json-15 Oct 2022, 14:14:58",
    "Стокхолмски_синдром_violeta.todorovaaa@gmail.com.json-15 Oct 2022, 18:27:30",
    "Съюз_на_българските_автомобилисти_dsgeorgiev90@yahoo.com.json-29 Jun 2022, 00:09:31",
    "Съюз_на_българските_автомобилисти_g.yordanov999@gmail.com.json-29 Jun 2022, 12:44:06",
    "ТАБСО_dsgeorgiev90@yahoo.com.json-15 Oct 2022, 13:49:58",
    "ТАБСО_violeta.todorovaaa@gmail.com.json-14 Oct 2022, 17:43:38",
    "Табулираща_машина_petya.stoyanovaaaa@gmail.com.json-23 Jun 2022, 16:51:08",
    "Табулираща_машина_violeta.todorovaaa@gmail.com.json-22 Jun 2022, 13:42:27",
    "Транзистор_dsgeorgiev90@yahoo.com.json-11 May 2022, 22:33:23",
    "Транзистор_petya.stoyanovaaaa@gmail.com.json-12 May 2022, 00:22:50",
    "Тримерен_печат_dsgeorgiev90@yahoo.com.json-13 May 2022, 23:23:15",
    "Тримерен_печат_georgitidorov4508@gmail.com.json-12 May 2022, 21:55:35",
    "Уеб_сървър_g.yordanov999@gmail.com.json-3 Jun 2022, 19:06:00",
    "Уеб_сървър_petya.stoyanovaaaa@gmail.com.json-2 Jun 2022, 14:50:22",
    "Уебстраница_g.yordanov999@gmail.com.json-3 Jun 2022, 19:00:52",
    "Уебстраница_petya.stoyanovaaaa@gmail.com.json-21 May 2022, 15:53:20",
    "ФК_Ювентус_g.yordanov999@gmail.com.json-29 Jun 2022, 13:30:12",
    "ФК_Ювентус_violeta.todorovaaa@gmail.com.json-6 Jul 2022, 00:31:05",
    "Фестивал_g.yordanov999@gmail.com.json-28 Oct 2022, 01:05:32",
    "Фестивал_georgitidorov4508@gmail.com.json-20 Oct 2022, 02:23:14",
    "Формула_1_g.yordanov999@gmail.com.json-29 Jun 2022, 13:11:06",
    "Формула_1_violeta.todorovaaa@gmail.com.json-6 Jul 2022, 00:10:07",
    "Хановер_dsgeorgiev90@yahoo.com.json-28 Jun 2022, 23:30:20",
    "Хановер_violeta.todorovaaa@gmail.com.json-22 Jun 2022, 13:59:02",
    "Хокей_на_лед_tachevy001@gmail.com.json-9 May 2022, 14:04:19",
    "Хокей_на_лед_violeta.todorovaaa@gmail.com.json-9 May 2022, 11:13:20",
    "Хоум_Бокс_Офис_dsgeorgiev90@yahoo.com.json-11 May 2022, 23:38:15",
    "Хоум_Бокс_Офис_georgitidorov4508@gmail.com.json-12 May 2022, 21:29:42",
    "Христо_Ботев_dsgeorgiev90@yahoo.com.json-9 May 2022, 22:19:44",
    "Христо_Ботев_stella.vouteva@gmail.com.json-9 May 2022, 22:09:36",
    "Хълк_georgitidorov4508@gmail.com.json-20 Oct 2022, 01:30:",
    "Хълк_petya.stoyanovaaaa@gmail.com.json-19 Oct 2022, 23:51:40",
    "Хърватия_g.yordanov999@gmail.com.json-28 Oct 2022, 00:57:48",
    "Хърватия_georgitidorov4508@gmail.com.json-20 Oct 2022, 02:04:35",
    "Чип_dsgeorgiev90@yahoo.com.json-11 May 2022, 20:58:33",
    "Чип_georgitidorov4508@gmail.com.json-10 May 2022, 20:32:46",
    "Шампионска_лига_на_УЕФА_dsgeorgiev90@yahoo.com.json-20 Jun 2022, 14:22:26",
    "Шампионска_лига_на_УЕФА_violeta.todorovaaa@gmail.com.json-8 May 2022, 23:31:57"
]
winners = [
    "Conus_eugrammatus 15 Oct 2022, 14:16:23",
    "Би_Би_Си 20 Oct 2022, 01:08:01",
    "Модерно_семейство 20 Oct 2022, 01:45:08",
    "Берлин 15 Oct 2022, 14:13:54",
    "Транзистор 12 May 2022, 00:22:50",
    "Конституционен_съд_на_България 29 Jun 2022, 13:20:57",
    "Пловдивски_университет 15 Oct 2022, 13:45:47"
]

def processAnnotationTexts():
    # Creating the file directories
    f = open("annotations-2.txt", "w", encoding="utf-8")
    for annotation in annotations:
        
        exception_mails = ['jesher_a@hotmail.com', 'contact@iliyasgeorgiev.com']
        if any(i in annotation for i in exception_mails):
            continue
        else:
            date = annotation.split('-')[-1]
            article_name = annotation.split('-')[0]
            article_name = article_name.split('_')[:-1]
            article_name = '_'.join(article_name)
            print(article_name + ' ' + date)
            f.write(article_name + ' ' + date + "\n")
    f.close()

def processWinners():
    f = open("winners.txt", "w", encoding="utf-8")
    for winner in winners:
        article_name = winner.split(' ')[0]
        date = winner.split(' ')[1:]
        date = ' '.join(date)
        for annotation in annotations:
            date_annotation = annotation.split('-')[-1]
            article_name_annotation = annotation.split('-')[0]
            article_name_annotation = article_name.split('_')[:-1]
            article_name_annotation = ''.join(article_name)
            email = annotation.replace(date_annotation,"").replace(article_name_annotation,"").replace("-","").replace(".json","")
            if(article_name == article_name_annotation and date_annotation == date):
                f.write("Annotation:" + annotation + " Email:" + email + "\n")
    f.close()

if __name__ == "__main__":
    # processAnnotationTexts()
    processWinners()