import http.client
import json

HOST = "localhost"
PORT = 8000
CONNECTION_CLASS = http.client.HTTPConnection

conn = CONNECTION_CLASS(HOST, PORT)

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
    response_data = response.read()
    response_json = json.loads(response_data)
    if response.status == 200:
        return response_json['token']
    else:
        raise ConnectionError(f"Connection Error {response.status}.")

def get_post_list(conn:CONNECTION_CLASS=conn, headers:dict[str, str]=headers) -> list[tuple[str]]:
    conn.request("GET", "/", headers=headers)
    response = conn.getresponse()
    response_data = response.read()
    response_json = json.loads(response_data)
    if response.status == 200:
        print(response_json)
        post_list = []
        for post_dict in response_json['results']:
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
