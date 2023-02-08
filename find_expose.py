import os
import sys
import subprocess
import threading
import requests
from termcolor import colored
from time import sleep

def brute_force(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(colored(f"Found: {url}", 'green', attrs=['bold']))

def worker(word_list, base_url):
    for word in word_list:
        url = base_url + "/" + word
        brute_force(url)

def clone_repo(url, name):
    with open(os.devnull, 'w') as devnull:
       subprocess.call(["git", "clone", url, name], stdout=devnull, stderr=devnull)

def get_files(path):
    output = subprocess.check_output(["git", "ls-files"], cwd=path)
    files = output.decode().strip().split("\n")
    return files

def delete_repo(repo_name):
    os.system(f"rm -rf {repo_name}")

def main():
    # python find_expose.py [SPACE] https://example.com [SPACE] https://github.com/repo
    base_url = sys.argv[1]
    repo_url = sys.argv[2]
    repo_name = repo_url.split("/")[-1].split(".")[0]

    word_list = []
    clone_repo(repo_url, repo_name)
    files = get_files(repo_name)
    for file in files:
        if file.endswith(".php") or file.endswith(".js") or file.endswith(".html") or file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".css") or file.endswith(".ttf") or file.endswith(".gif") or file.endswith(".eot") or file.endswith(".z") or file.endswith(".htm") or file.endswith(".docx") or file.endswith(".pdf") or file.endswith(".woff2") or file.endswith(".eot") or file.endswith(".svg") or file.endswith(".doc") or file.endswith(".htm") or file.endswith(".woff") or file.endswith(".txt") or file.endswith(".ico") or file.endswith(".fdf") or file.endswith(".eps") or file.endswith(".icc") or file.endswith(".ai") or file.endswith(".md") or file.endswith(".p12") or file.endswith(".otf"):
            continue
        word_list.append(file)
    sleep(10)

    for i in range(len(word_list)):
        word_list[i] = word_list[i].rstrip()
        
    num_threads = 50 
    chunk_size = len(word_list) // num_threads
    threads = []

    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size
        chunk = word_list[start:end]
        t = threading.Thread(target=worker, args=(chunk, base_url))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    delete_repo(repo_name)

if __name__ == "__main__":
    main()
