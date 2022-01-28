import os
import shutil
x = os.listdir("/home/www/code/django_server/django_ggrksok/media/youtube")
p = os.listdir("/home/www/code/django_server/django_ggrksok/media/tiktok")
# x = os.listdir("/home/www/code/python_server/media")
for i in x:
    # shutil.rmtree(f"/home/www/code/django_server/django_ggrksok/media/{i}")
    os.remove(f"/home/www/code/django_server/django_ggrksok/media/youtube/{i}")
for i in p:
    os.remove(f"/home/www/code/django_server/django_ggrksok/media/tiktok/{i}")
# u = os.listdir(f"/home/www/code/django_server/django_ggrksok/instagram")
g = os.listdir(f"/home/www/code/django_server/django_ggrksok/media/tt_profile")
for i in g:
    shutil.rmtree(f"/home/www/code/django_server/django_ggrksok/media/tt_profile/{i}")
u = os.listdir(f"/home/www/code/python_server/instagram")
for y in u:
    shutil.rmtree(f"/home/www/code/python_server/instagram/{y}")
    # shutil.rmtree(f"/home/www/code/django_server/django_ggrksok/instagram/{y}")
u = os.listdir(f"/home/www/code/python_server/highlights")
# u = os.listdir(f"/home/www/code/django_server/django_ggrksok/highlights")
for y in u:
    shutil.rmtree(f"/home/www/code/python_server/highlights/{y}")
    # shutil.rmtree(f"/home/www/code/django_server/django_ggrksok/highlights/{y}")
