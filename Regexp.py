from pprint import pprint
import csv
import re

with open("venv/Regexp/phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# lastname,firstname,surname,organization,position,phone,email

lastname_list = []
firstname_list = []
surname_list = []
organization_list = []
position_list = []
phone_list = []
email_list = []

m = 0
#Индекс для проверки, что этот признак (Ф,И,О) вообще есть у пользователя

for i in contacts_list:
    x = 0
    for t in i:
        if x == 0:
            pattern_1 = re.compile(r"([а-яёА-ЯЁ]*)?\s?([а-яёА-ЯЁ]*)?\s?([а-яёА-ЯЁ]*)?")
            lastname = pattern_1.sub(r"\1", i[x])
            firstname_1 = pattern_1.sub(r"\2", i[x])
            surname_1 = pattern_1.sub(r"\3", i[x])
            if len(lastname) > 0:
                lastname_list.append(lastname)
            if len(firstname_1) > 0:
                firstname_list.append(firstname_1)
            if len(surname_1) > 0:
                surname_list.append(surname_1)

        if x == 1:
            pattern_2 = re.compile(r"([а-яёА-ЯЁ]*)?\s?([а-яёА-ЯЁ]*)?")
            firstname_2 = pattern_2.sub(r"\1", i[x])
            surname_2 = pattern_2.sub(r"\2", i[x])
            if len(firstname_2) > 0:
                firstname_list.append(firstname_2)
            if len(surname_2) > 0:
                surname_list.append(surname_2)
        if x == 2:
            pattern_3 = re.compile(r"([а-яёА-ЯЁ]*)?\s?")
            surname_3 = pattern_3.sub(r"\1", i[x])
            if len(surname_3) > 0:
                surname_list.append(surname_3)
        if x == 3:
            organization_list.append(t)
        if x == 4:
            position_list.append(t)
        if x == 5:
            pattern_5 = re.compile(r"(\+7|8)?\s*\(*(\d{3})\)*[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s*)\(?([а-яА-Я\.]*)(\s*)(\d*)\)?")
            phone = pattern_5.sub(r"+7(\2)\3-\4-\5 \7\9", i[x])
            phone_list.append(phone)
        if x == 6:
            email_list.append(t)
        # переходим к следующему элементу в списке
        x += 1
    #проверка пустых значений
    if len(firstname_list) < len(lastname_list):
        firstname_list.append("")
    if len(surname_list) < len(lastname_list):
        surname_list.append("")
    m += 1

new_contacts_list = list(zip(lastname_list, firstname_list, surname_list, organization_list, phone_list, email_list))

#ищем дубли
counter = {}
for elem in lastname_list:
    counter[elem] = counter.get(elem, 0) + 1

duplicates = {element: count for element, count in counter.items() if count > 1}

e = ""

#складываем дубли вместе
dict = {}
position = []
for k in duplicates.keys():
    test = []
    for i in new_contacts_list:
        if k in i[0]:
            for z in i:
                if z not in test:
                    test.append(z)
            position.append(new_contacts_list.index(i))
    new_contacts_list.append(tuple(test))

# удаляем дубли
q = sorted(position, reverse=True)
for d in q:
    new_contacts_list.pop(d)

all_new_contacts = []

for i in new_contacts_list:
    if i == new_contacts_list[5]:
        f = list(i)
        f.pop(5)
        print(f)
        all_new_contacts.append(f)
    else:
        all_new_contacts.append(i)



pprint(all_new_contacts)

with open("venv/Regexp/phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(all_new_contacts)