from __future__ import unicode_literals
from fastapi import (
    FastAPI,
    Form,
    Cookie,
    Body,
    Query,
    Request,
    BackgroundTasks,
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import Optional
import json
import random
from youtube_dl import YoutubeDL
import base64
from pathlib import Path


from fastapi.responses import Response
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


import hashlib
import hmac


app = FastAPI()
app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/gg", StaticFiles(directory="gg"), name="gg")
app.mount("/instagram", StaticFiles(directory="instagram"), name="instagram")
templates = Jinja2Templates(directory="templates/")

origins = [
    "http://ggrksok.fun",
    "https://ggrksok.fun"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
users = {
    "alex": {
        "name": "alexey",
        "password": "870956f00d1448b7a92008bc8a2dd54628eae478c7a3c1197af3d082bc9ab6c1",
        "balance": 10,
    },
    "john": {
        "name": "johny",
        "password": "a59d0c1ecf2294fd443fa0a54e85a48d0067d50c3edadccece7ae9038e03b97c",
        "balance": 100_000,
    },
}

SECRET_KEY = "password"
PASSWORD_SALT = "a4848b2bb3b55d0c1f16"


def sign_data(data: str) -> str:
    return (
        hmac.new(SECRET_KEY.encode(), msg=data.encode(), digestmod=hashlib.sha256)
        .hexdigest()
        .upper()
    )


def verify_password(
    username: str,
    password: str,
) -> bool:
    password_hash = (
        hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    )
    stored_password_hash = users[username]["password"].lower()
    return password_hash == stored_password_hash


def get_username_from_signed_string(username_signed: str) -> Optional[str]:
    username_base64, sign = username_signed.split(".")
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username


@app.get("/download")
def root(username: Optional[str] = Cookie(default=None)):
    with open("templates/login.html", "r") as f:
        login_page = f.read()
    if not username:
        return Response(login_page, media_type="text/html")
    valid_username = get_username_from_signed_string(username)
    if not valid_username:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")
        return response
    try:
        user = users[valid_username]
    except KeyError:
        response = Response(login_page, media_type="text/html")

        response.delete_cookie(key="username")
        return response
    return Response(f"hello, {users[valid_username]['name']}", media_type="text/html")


def clear_file(file: str = Form(...)):
    os.remove(f"./media/{file}")


bestvideo = "best[height<=1080]"


def video_downloader(url: str):
    ydl_opts = {
        "format": bestvideo,
        "outtmpl": "media/%(id)s.%(ext)s",
        "noplaylist": True,
        "extract-audio": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_id = info_dict.get("id")
        video_ext = info_dict.get("ext")
    file_response = f"{video_id}.{video_ext}"
    return file_response


def file_size(file_list):
    pass


@app.post("/api/download")
def api_download(request: Request, data: str = Query(...)):
    file = video_downloader(data)
    response = f"https://ggrksok.fun/media/{file}"
    return Response(response)


@app.get("/")
def download(request: Request):
    return templates.TemplateResponse("ytb.html", context={"request": request})


@app.post("/link")
def app_download(
    background_tasks: BackgroundTasks,
    request: Request,
    url: str = Form(...),
    save: bool = Form(False),
):
    if not save:
        file_response = video_downloader(url)
        return FileResponse(
            f"media/{file_response}",
            media_type="application/octet-stream",
            filename=file_response,
        )
    else:
        message = "Будь готов! Всегда готов!"
        background_tasks.add_task(video_downloader, url)
        return templates.TemplateResponse(
            "ytb.html", context={"request": request, "message": message}
        )


@app.get("/checkbox")
def form_post(request: Request):
    result = os.listdir("./media")
    return templates.TemplateResponse(
        "checkbox.html", context={"request": request, "result": result}
    )


@app.post("/checkbox")
def get_file(
    request: Request, file: str = Form(default=None), clear: str = Form(default=None)
):
    if file:
        return FileResponse(
            f"media/{file}",
            media_type="application/octet-stream",
            filename=file,
        )
    if clear:
        clear_file(clear)
        result = os.listdir("./media")
        return templates.TemplateResponse(
            "checkbox.html", context={"request": request, "result": result}
        )


# def app_download(url: str):
#     ydl_opts = {
#         "format": "bestvideo[height <= 1080]+bestaudio",
#         "outtmpl": r"after_media/%(id)s%(ext)s",
#     }
#     x = os.listdir("./after_media")
#     print(x)
#     for i in x:
#         os.remove(f"./after_media/{i}")
#     with YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(url, download=True)
#         video_title = info_dict.get("title")
#         print(video_title)
#         # print(list(info_dict))
#         new_list = []
#         file_list = os.listdir("./after_media")

#         for i in file_list:
#             if i.endswith("webm"):
#                 h = "".join(filter(str.isalnum, i))
#                 a = i.replace("webm", ".mkv")
#                 print(h)
#                 os.replace(f"after_media/{i}", f"after_media/{a}")
#             elif i.endswith("mp4"):
#                 h = "".join(filter(str.isalnum, i))
#                 a = h.replace("mp4", ".mkv")
#                 os.replace(f"after_media/{i}", f"after_media/{a}")
#             else:
#                 h = "".join(filter(str.isalnum, i))
#                 a = h.replace("mkv", ".mkv")

#                 os.replace(f"after_media/{i}", f"after_media/{a}")
#                 return a


@app.post("/fake")
async def download(background_tasks: BackgroundTasks, url: str = Form(...)):
    background_tasks.add_task(app_download, url)
    return Response("OK", media_type="text/html")


@app.get("/get_file")
def directory():
    x = os.listdir("./after_media")
    print(x)
    # path = Path(f"./after_media/{x}")
    # if path.exists():
    for i in x:
        return FileResponse(f"./after_media/{i}")


@app.post("/login")
# def process_login_page(username : str = Form(...), password : str = Form(...)):
def process_login_page(data: dict = Body(...)):
    username = data["username"]
    password = data["password"]
    user = users.get(username)
    if not user or not verify_password(username, password):
        return Response(
            json.dumps({"success": False, "message": "I dont know you"}),
            media_type="application/json",
        )
    response = Response(
        json.dumps(
            {
                "success": True,
                "message": f"Hello, {user['name']}!<br />Balance: {user['balance']}",
            }
        ),
        media_type="application/json",
    )
    username_signed = (
        base64.b64encode(username.encode()).decode() + "." + sign_data(username)
    )
    response.set_cookie(key="username", value=username_signed)
    return response


@app.post("/unify_phone_from_json")
def unify_phone_from_json(data: dict = Body(...)):
    phone = "".join(filter(str.isdigit, data["phone"]))
    if len(phone) == 11:
        if phone[0] == "7" or phone[0] == "8" or phone[0] == "9":
            if phone[0] == "7":
                phone = phone.replace("7", "8", 1)
            elif phone[0] == "8":
                phone = phone
            elif phone[0] == "9":
                phone = "8" + phone
            phone = f"{phone[:1]} ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:]}"
    else:
        phone
    return Response(phone, media_type="text/html")


@app.post("/unify_phone_from_form")
def unify_phone_from_form(phone: str = Form(...)):
    phone = "".join(filter(str.isdigit, phone))
    if len(phone) == 11:
        if phone[0] == "7" or phone[0] == "8" or phone[0] == "9":
            if phone[0] == "7":
                phone = phone.replace("7", "8", 1)
            elif phone[0] == "8":
                phone = phone
            elif phone[0] == "9":
                phone = "8" + phone
            phone = f"{phone[:1]} ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:]}"
    else:
        phone
    return Response(phone, media_type="text/html")


@app.get("/unify_phone_from_query")
def unify_phone_from_query(phone: str = Query(...)):
    phone = "".join(filter(str.isdigit, phone))
    if len(phone) == 11:
        if phone[0] == "7" or phone[0] == "8" or phone[0] == "9":
            if phone[0] == "7":
                phone = phone.replace("7", "8", 1)
            elif phone[0] == "8":
                phone = phone
            elif phone[0] == "9":
                phone = "8" + phone
            phone = f"{phone[:1]} ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:]}"
    else:
        phone
    return Response(phone, media_type="text/html")


@app.get("/unify_phone_from_cookies")
def unify_phone_from_cookies(phone: Optional[str] = Cookie(...)):
    # return {"ads_id": ads_id}
    # def unify_phone_from_query(phone: str):
    if phone:
        phone = "".join(filter(str.isdigit, phone))
        if len(phone) == 11:
            if phone[0] == "7" or phone[0] == "8" or phone[0] == "9":
                if phone[0] == "7":
                    phone = phone.replace("7", "8", 1)
                elif phone[0] == "8":
                    phone = phone
                elif phone[0] == "9":
                    phone = "8" + phone
                phone = (
                    f"{phone[:1]} ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:]}"
                )
        else:
            phone
        response = Response(phone, media_type="text/html")
        response.set_cookie(key="phone", value=phone)
        return response

