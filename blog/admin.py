from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Post


#admin.site.register(Post)

@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    pass

'''
가상환경 만들기
C:\djangogirls> C:\ProgramData\Anaconda3\python -m venv myvenv

가상환경 사용하기
C:\djangogirls> myvenv\Scripts\activate

(myvenv) python manage.py createsuperuser


(myvenv) python manage.py makemigrations blog
(myvenv) python manage.py migrate

(myvenv) python manage.py runserver


http://127.0.0.1:8000/
'''