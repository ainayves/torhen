import os , sys
import time
import libtorrent as lt
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def stream_upload(magnet_link: str):
    # # # Create a service object using the credentials file
    # # credentials = service_account.Credentials.from_service_account_file('client_secrets.json')
    # # drive_service = build('drive', 'v3', credentials=credentials)

    # # Set up libtorrent session
    # ses = lt.session()
    # ses.listen_on(6881, 6891)
    # params = {"save_path": "."}  # Local path to temporarily store the torrent data
    # downloads = []
    # downloads.append(lt.add_magnet_uri(ses, magnet_link, params))
  
    # stat = 0
    # while downloads:
    #     next_shift = 0
    #     for index, download in enumerate(downloads[:]):
    #         handle = download
    #         status = handle.status()

    #         # Check if the torrent has completed downloading
    #         if status.is_seeding:
    #             # Move the downloaded file to Google Drive
    #             file_name = status.name
    #             local_path = os.path.join(params["save_path"], file_name)

    #             # Upload the file to Google Drive
    #             file_metadata = {'name': file_name}
    #             media = MediaFileUpload(local_path, mimetype='application/octet-stream')
    #             # file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    #             # print(f'File "{file_name}" uploaded to Google Drive with ID: {file["id"]}')

    #             # Remove the torrent from libtorrent session and delete the temporary file
    #             # ses.remove_torrent(handle)
    #             # os.remove(local_path)
    #             print(stat)
    #             stat+=1

    #         else :
    #             print(status.__dict__)
            
    #         time.sleep(1)  # Sleep for a second before checking the next torrent
    ses = lt.session()
    ses.listen_on(6881, 6891)

    params = {'save_path': '.'}
    # h = ses.add_torrent({'ti': info, 'save_path': '.'})
    h = lt.add_magnet_uri(ses, magnet_link, params)
    s = h.status()
    print('starting', s.name)

    while (not s.is_seeding):
        s = h.status()

        print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
            s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
            s.num_peers, s.state), end=' ')

        alerts = ses.pop_alerts()
        for a in alerts:
            if a.category() & lt.alert.category_t.error_notification:
                print(a)

        sys.stdout.flush()

        time.sleep(1)

    print(h.status().name, 'complete')