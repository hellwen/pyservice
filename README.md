售后服务系统

## 缘起


##Install

###Prerequisite

  pip install -r requirements.txt

###Custom the Configuration
	
	pypress/config.cfg

###Sync database

	python manage.py createall

###Run

	python manage.py runserver

##Example

###Create User

Admin:

	python manage.py createadmin

###Generate Admin active code

	python manage.py createcode -r admin


