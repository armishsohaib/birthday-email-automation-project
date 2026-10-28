
import os
import datetime
import pandas
import random
import smtplib
import ssl

MY_EMAIL = os.environ["MY_EMAIL"]
MY_PASSWORD = os.environ["MY_PASSWORD"]

context = ssl.create_default_context()

today_date = datetime.datetime.now()
today_day = today_date.day
today_month = today_date.month

today_tuple = (today_month, today_day)

data = pandas.read_csv("birthdays.csv")

birthday_dict = {
    (data_row["month"], data_row["day"]): data_row
    for (index, data_row) in data.iterrows()
}

if today_tuple in birthday_dict:
    birthday_person = birthday_dict[today_tuple]

    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"

    with open(file_path) as f:
        contents = f.read()
        contents = contents.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        context=context,
        timeout=30
    ) as connection:
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject: Happy Birthday!\n\n{contents}"
        )
