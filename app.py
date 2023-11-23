from flask import Flask, request, render_template
from datetime import datetime
import re
from database.database import DataBase

app = Flask(__name__)
app.config.from_object('config')
db = DataBase()


def sublist_in_list(sub, lis):
    return str(sub).strip('[]') in str(lis).strip('[]')


def validate_date(date_str):
    formats = ['%d.%m.%Y', '%Y-%m-%d']

    for date_format in formats:
        try:
            datetime.strptime(date_str, date_format)
            return True

        except ValueError:
            pass

    return False


def validate_phone(phone_number):
    phone_regex = r'^\+7 \d{3} \d{3} \d{2} \d{2}$'

    if re.match(phone_regex, phone_number):
        return True
    else:
        return False


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9]+\.[a-z]+$'

    if re.match(email_regex, email):
        return True
    else:
        return False


def get_type(item):
    if validate_date(item):
        return 'date'
    elif validate_phone(item):
        return 'phone'
    elif validate_email(item):
        return 'email'
    else:
        return 'text'


def find_matching_template(data):
    result = []
    form_templates = db.get_templates()
    data_new = [i for i in form_templates if sublist_in_list(data.keys(), i.keys())]
    for i in data_new:
        k = 0
        for key, item in i:
            if key in data.keys:
                if item == data[key]:
                    k += 1
        if k == len(data):
            result.append(i['name'])
    if result:
        return result
    else:
        result = {}
        for key, item in data:
            result[key] = get_type(item)
        return result


@app.route('/get_form', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)

        return find_matching_template(data)
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run()
