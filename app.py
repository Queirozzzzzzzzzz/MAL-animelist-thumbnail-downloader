from tkinter import Tk, Label, Entry, Button, messagebox

from models.api import getUserAnimeList
from models.imageDownloader import downloadImages


def get_user_anime_list():
    clientId = mal_client_id_entry.get()
    username = username_entry.get()
    limit = list_limit_entry.get()
    
    res = getUserAnimeList(clientId, username, limit)

    messagebox.showinfo(title= 'Get User Animelist', message=res)

def download_images():
    username = username_entry.get()
    min_score = min_score_entry.get()

    res = downloadImages(username, min_score)

    messagebox.showinfo(title= 'Download Images', message=res)

root = Tk()
root.title("Anime List Ranking")
root.geometry("400x300")

#  MAL Client ID input
mal_client_id_label = Label(root, text="MAL CLIENT_ID:")
mal_client_id_entry = Entry(root)
mal_client_id_label.pack()
mal_client_id_entry.pack()

# Username input
username_label = Label(root, text="USERNAME:")
username_entry = Entry(root)
username_label.pack()
username_entry.pack()

# Limit input
list_limit_label = Label(root, text="LIST LIMIT:")
list_limit_entry = Entry(root)
list_limit_entry.insert(0, '1000')
list_limit_label.pack()
list_limit_entry.pack()

# Anime list button
get_anime_list_button = Button(root, text="GET USER ANIMELIST", command=get_user_anime_list)
get_anime_list_button.pack()

# Min Score input
min_score_label = Label(root, text="MINIMUM SCORE:")
min_score_entry = Entry(root)
min_score_entry.insert(0, '10')
min_score_label.pack()
min_score_entry.pack()

# Download images button
download_images_button = Button(root, text="DOWNLOAD IMAGES", command=download_images)
download_images_button.pack()

root.mainloop()
