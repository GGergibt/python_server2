import os
import shutil
# x = os.listdir("/home/www/code/python_server/media")
try:
    u = os.listdir("/home/www/projects/python_server2/instagram")
    for y in u:
        shutil.rmtree(f"/home/www/projects/python_server2/instagram/{y}")
        # shutil.rmtree(f"/home/www/code/django_server/django_ggrksok/instagram/{y}")
except FileNotFoundError:
    print("instagram stories already clean")
try:
    # u = os.listdir(f"/home/www/code/django_server/django_ggrksok/highlights")
    u = os.listdir("/home/www/projects/python_server2/highlights")
    for y in u:
        shutil.rmtree(f"/home/www/projects/python_server2/highlights/{y}")
        # shutil.rmtree(f"/home/www/code/django_server/django_ggrksok/highlights/{y}")
except FileNotFoundError:

        print("highlights already clean")
