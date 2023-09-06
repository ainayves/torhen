import libtorrent as lt

ses = lt.session()
ses.listen_on(6881, 6891)
downloads = []

params = {"save_path": "/content/drive/My Drive/Torrent"}

while True:
    magnet_link = input("Enter Magnet Link Or Type Exit: ")
    if magnet_link.lower() == "exit":
        break
    downloads.append(
        lt.add_magnet_uri(ses, magnet_link, params)
    )