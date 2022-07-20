from django.core.mail import send_mail
from config.config import EMAIL_HOST_USER as f_email

def generate_name_password(obj):
    letters = 'qwertyupasdfghkzxcvbnm123456789'
    id = str(obj.objects.all().last().id).rjust(6, '0')
    username = f"user{id}"
    password = ''.join(set(letters))[:8]
    return {'username': username, 'password': password}


def send_password_to_email(data: dict, name, email):
    text = f"Ваш логин: {data['username']}\n\n"
    text += f"Ваш пароль: {data['password']}\n\n"
    text += "Ни с кем не делитесь!"
    send_mail(
        "Ваш логин и пароль",
        f"Уважаемый(ая) {name}\n\n{text}",
        f_email,
        [email],
    )
    