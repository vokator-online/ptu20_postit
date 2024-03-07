import http.client
import json

HOST = "localhost"
PORT = 8000
CONNECTION_CLASS = http.client.HTTPConnection

conn = CONNECTION_CLASS(HOST, PORT)
# conn.debuglevel = 1

headers = {
    "Accept": "*/*",
    "User-Agent": "PostIt GUI",
    "Content-Type": "application/json" 
}

def login(username: str, password: str, conn:CONNECTION_CLASS=conn, headers:dict[str, str]=headers) -> str:
    payload = json.dumps({
        "username": username,
        "password": password
    })
    conn.request("POST", "/api-token-auth/", payload, headers)
    response = conn.getresponse()
    response_json = response.read()
    print(response_json)
    if response.status == 200:
        auth_data = json.loads(response_json)
        return auth_data['token']
    else:
        raise ConnectionError(f"Connection Error {response.status}.")

def auth_headers(headers: dict[str, str], auth_token: str) -> dict[str, str]:
    if len(auth_token) > 0:
        headers["Authorization"] = f"Token {auth_token}"
    else:
        if "Authorization" in headers:
            del headers["Authorization"]
    return headers

def post_like(pk: int, auth_token: str, conn:CONNECTION_CLASS=conn, headers:dict[str, str]=headers) -> dict[str, str]:
    conn.request("POST", f"/{pk}/like/", headers=auth_headers(headers, auth_token))
    response = conn.getresponse()
    response_json = response.read()
    if response.status >= 200 and response.status < 400:
        like_detail = json.loads(response_json)
        return like_detail
    else:
        raise ConnectionError(f"Connection Error {response.status}.")    

def get_post_detail(pk: int, conn:CONNECTION_CLASS=conn, headers:dict[str, str]=headers):
    conn.request("GET", f"/{pk}/", headers=headers)
    response = conn.getresponse()
    response_json = response.read()
    if response.status == 200:
        post_detail = json.loads(response_json)
        return post_detail
    else:
        raise ConnectionError(f"Connection Error {response.status}.")

def get_post_list(conn:CONNECTION_CLASS=conn, headers:dict[str, str]=headers) -> list[tuple[str]]:
    conn.request("GET", "/", headers=headers)
    response = conn.getresponse()
    response_json = response.read()
    if response.status == 200:
        data = json.loads(response_json)
        post_list = []
        for post_dict in data['results']:
            post_list.append((
                post_dict['id'], 
                post_dict['title'], 
                post_dict['user_username'], 
                f"{post_dict['updated_at'][:10]} {post_dict['updated_at'][11:16]}", 
                post_dict['like_count'], 
                post_dict['comment_count'],
            ))
        return post_list
    else:
        raise ConnectionError(f"Connection Error {response.status}.")
