# First argument: path to playlists links list file(links should be separated by newline and the file should have a trailing newline)
# Second argument: the number of processes to spawn concurrently
# Third argument: maximum resolution
import shlex
import subprocess
from multiprocessing import Process
import sys

TEXT_FILE = None
with open(sys.argv[1]) as fp:
    TEXT_FILE = fp.read()
N_THREADS = int(sys.argv[2])
RES = sys.argv[3]
LINKS = TEXT_FILE.split('\n')
LINKS.pop()


def download_playlist(link: str) -> bool:
    command = shlex.split(f'yt-dlp -i \"{link}\" --no-mtime -o \'%(playlist)s/%(title)s.%(ext)s\' -f \'bestvideo['f'height<={RES}]bestvideo[ext=mp4]+bestaudio\'')
    try:
        process = subprocess.Popen(command)
        process.wait()
    except Exception as e:
        print("Unexpected exception: ", e)
        return False
    return True


def main():
    idx = 0
    while idx < len(LINKS):
        processes = []
        for _ in range(0, N_THREADS):
            print(f"Spawning thread for playlist: {LINKS[idx]}")
            process = Process(target=download_playlist, args=(LINKS[idx], ))
            processes.append(process)
            process.start()
            idx += 1
            
        while len(processes) != 0:
            p_idx = 0
            while p_idx < len(processes):
                if not processes[p_idx].is_alive():
                    processes.pop(p_idx)
                    break
                p_idx += 1

                
if __name__ == "__main__":
    main()
    
