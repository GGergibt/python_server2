import requests
from sending_files import sending_file


def youtube_downloader(chat_id, key_name, text_url):
    print(key_name, text_url, sep="\n")
    api_url = f"http://localhost:8000/link?{key_name}={text_url}"
    response = requests.get(api_url, verify=False, stream=True)
    if response.status_code == 200:
        res = response.text

        sending_file(res, chat_id)
    else:
        print("sorry, we get problems on the server side")


def get_accounts_and_download_count(chat_id, profiles_column):
    api_url = f"http://localhost:8000/users/{chat_id}/{profiles_column}"
    response = requests.get(api_url, verify=False, stream=True)
    return response.json()


def stored_profiles_for_user_in_db(chat_id, account, profiles_column):
    api_url = f"http://localhost:8000/users/add/"
    post_body = {
        "chat_id": chat_id,
        "account": account,
        "profiles_column": profiles_column,
    }

    query_api = requests.post(api_url, json=post_body)


# i = stored_profiles_for_user_in_db(1176413729, "mishe_mozh", "insta_accounts")
