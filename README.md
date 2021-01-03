# flickerp
#### Employee Management  system, it includes employee leaves , holidays , calendar , time sheet , pay role etc.  


### Setup Instructions
 To be able to use ans run on Linux bases system,

```
git clone git@github.com:yogeshdmca/flickerp.git
```

Create Venv using python 3,

```
cd flickerp
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
virtualenv .venv 
source .venv/bin/activate
```
If you have Python3.3 and newer version, venv is already there. Here how it worked for me without installing virtualenv.
```
sudo apt-get install python3-venv
python3 -m venv .venv
source .venv/bin/activate
```


Install all python modules and app
```
pip install -r requirement
```

Now Need to change settings files. go to geitpl_erp/settings folder and open base.py and replace 
```
SECRET_KEY = "make and add your SECRET_KEY "

TIME_ZONE = 'Your timezon'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.google.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "info@flickerp.com"
# EMAIL_HOST_PASSWORD = "EMAIL HOST PASSWORD"

```

Now Need to change settings files. go to geitpl_erp/settings folder and open DEV.py and replace 
```
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'DBNAME',
        'USER':     'USERNAME',
        'PASSWORD': 'PASSWORD',
        'HOST':     'DB HOST',
        'PORT':     'DB PORT',
    }
}
```


Migrate database and load data
```
./manage.py migrate
./manage.py loaddata user < geitpl_erp/apps/user/fixture/demoData.json
```


Start dev server
```
./manage.py runserver
open browser and visit  to 127.0.0.1:8000

Admin login :

admin@flickerp.com

pass: admin123

Manager : tl@flickerp.com
pass: admin@#$123 or admin@#$12345

```

