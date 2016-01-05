# proof of concept django project

herein find a testing playground focused around django. in these
directories i wanted to play around with sample implementations for:

- db trigger using signals
- trying out django rest framework
- glancing blows at angular for templating and rest consummation


## installation & running:
> first created runtime enviroment using python 2.7 virtualenvwrapper:
```
$ mkvirtualenv -r requirements.pip -p python2.7 poc_env
```

> setup django db
```
$ cd poc
$ python manage.py migrate
```

> add in a few sample users, for example:
```
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell
echo "from django.contrib.auth.models import User; User.objects.create_user('tom', 'tom@example.com', 'pass')" | python manage.py shell
echo "from django.contrib.auth.models import User; User.objects.create_user('spot', 'spot@example.com', 'pass')" | python manage.py shell
echo "from django.contrib.auth.models import User; User.objects.create_user('sally', 'sally@example.com', 'pass')" | python manage.py shell
```

> start the server
```
$ python manage.py runserver
```

> browse to the index, and log in
```
http://localhost:8000/
```