import PySimpleGUI as sg
import backend
from datetime import datetime

def post_detail(post_pk: int, root_window:sg.Window, auth_token: str) -> None:
    root_window.hide()
    try:
        post_detail = backend.get_post_detail(post_pk)
    except ConnectionError as error:
        sg.PopupOK(error, title="Oops")
        root_window.un_hide()
        return

    layout = [
        [
            sg.Text(post_detail["title"], key="-TITLE-", font="sans-serif 24"),
        ],
        [
            sg.Text(post_detail["body"], key="-BODY-"),
        ],
        [
            sg.Button("LIKE", key="-LIKE-"),
            sg.Text(post_detail["like_count"], key="-LIKES-"),
            sg.Button("COMMENTS", key="-SHOW-COMMENTS-"),
            sg.Text(post_detail["comment_count"], key="-COMMENTS-"),
        ],
        [
            sg.Text("Created:"), sg.Text(datetime.strptime(post_detail["created_at"][:19], "%Y-%m-%dT%H:%M:%S"), font="sans-serif 16"),
            sg.Text("Updated:"), sg.Text(datetime.strptime(post_detail["updated_at"][:19], "%Y-%m-%dT%H:%M:%S"), font="sans-serif 16"),
        ],
        [
            sg.Button('CLOSE', key="-CLOSE-"),
        ],
        # [
        #     sg.Text(f"Currently logged in as {root_window['-USERNAME-']}"),
        # ],
    ]

    window = sg.Window(
        f"Post by {post_detail['user_username']}", 
        layout, 
        element_justification='center', 
        element_padding=10, 
        finalize=True,
    )

    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, "-CLOSE-"]:
            break
        if event == "-LIKE-":
            try:
                like_detail = backend.post_like(post_pk, auth_token)
            except ConnectionError as error:
                sg.PopupOK(error, title="Oops")
            else:
                try:
                    post_detail = backend.get_post_detail(post_pk)
                except ConnectionError as error:
                    sg.PopupOK(error, title="Oops")
                else:
                    window["-LIKES-"].update(post_detail["like_count"])

    window.close()

    root_window.un_hide()
