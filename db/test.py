from db import user
import random

uid = random.randint(0, 100)
name = "Sm00thiee"
email = str(random.randint(0, 200)) + "@gmail.com"
pwd = "123123123"

user.login(uid, name, email, pwd)

#user.get_info(email)

