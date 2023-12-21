import libtorrent as lt
from tqdm import tqdm

def download_torrent(torrent_file_paths, save_path):
    ses = lt.session()
    params = {
        'save_path': save_path,
        'storage_mode': lt.storage_mode_t(2)
    }

    for torrent_file_path in torrent_file_paths:
        with open(torrent_file_path, 'rb') as f:
            e = lt.bdecode(f.read())
            info = lt.torrent_info(e)
            handle = ses.add_torrent({'ti': info, 'save_path': save_path})

        print("Downloading", info.name())

        with tqdm(total=100, dynamic_ncols=True, unit="%", unit_scale=True, desc="Progress") as pbar:
            while not handle.is_seed():
                s = handle.status()
                progress = int(s.progress * 100)
                download_speed = s.download_rate / 1000000  # Convert to MB/s
                pbar.set_postfix({"Download Speed": f"{download_speed:.1f} MB/s"})
                pbar.update(progress - pbar.n)

        print(f"Download of {info.name()} complete!")

if __name__ == "__main__":
    num_torrents = int(input("Enter the number of torrents: "))
    torrent_file_paths = [input(f"Enter path to torrent file {i + 1}: ") for i in range(num_torrents)]
    save_path = "/content/onePace"  # Use raw string for Windows paths
    download_torrent(torrent_file_paths, save_path)
