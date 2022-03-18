import os
import shutil
# x = os.listdir("/home/www/code/python_server/media")
try:
    x = os.listdir("/home/www/code/django_server/django_ggrksok/media/youtube")
    for i in x:
        # shutil.rmtree(f"/home/www/code/django_server/django_ggrksok/media/{i}")
        os.remove(f"/home/www/code/django_server/django_ggrksok/media/youtube/{i}")
except FileNotFoundError:
    print("youtube already clean")
try:
    p = os.listdir("/home/www/code/django_server/django_ggrksok/media/tiktok")
    for i in p:
        os.remove(f"/home/www/code/django_server/django_ggrksok/media/tiktok/{i}")
except FileNotFoundError:
    print("tiktok already clean")
    # u = os.listdir(f"/home/www/code/django_server/django_ggrksok/instagram")
try:
    g = os.listdir(f"/home/www/code/django_server/django_ggrksok/media/tt_profile")
    for i in g:
        shutil.rmtree(f"/home/www/code/django_server/django_ggrksok/media/tt_profile/{i}")
except FileNotFoundError:
    print("tt_profiles already clean")
try:
    u = os.listdir("/home/www/code/python_server2/instagram")
    for y in u:
        shutil.rmtree(f"/home/www/code/python_server2/instagram/{y}")
        # shutil.rmtree(f"/home/www/code/django_server/django_ggrksok/instagram/{y}")
except FileNotFoundError:
    print("instagram stories already clean")
try:
    # u = os.listdir(f"/home/www/code/django_server/django_ggrksok/highlights")
    u = os.listdir("/home/www/code/python_server2/highlights")
    for y in u:
        shutil.rmtree(f"/home/www/code/python_server2/highlights/{y}")
        # shutil.rmtree(f"/home/www/code/django_server/django_ggrksok/highlights/{y}")
except FileNotFoundError:

        print("highlights already clean")
