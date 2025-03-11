#!/usr/bin/env python3

import os
import subprocess
import argparse
from datetime import datetime

files_added = 0
files_removed = 0

def mega_login(email, password):
    # print("[jframe.py] Logging in to mega")
    subprocess.run(['mega-login', email, password], check=True)
    # print("[jframe.py] Login complete")

def mega_logout():
    # print("[jframe.py] Logging out of mega")
    subprocess.run(['mega-logout'], check=True, stdout=subprocess.DEVNULL)
    # print("[jframe.py] Logout complete")


def list_remote_files(remote_path):
    # print(f"[jframe.py] Getting listing of files in mega:{remote_path}")
    result = subprocess.run(['mega-ls', '-l', remote_path], capture_output=True, text=True, check=True)
    # print("[jframe.py] List received. Parsing list")
    files = {}
    lines = result.stdout.splitlines()
    for line in lines[1:]:  # Skip the first line which contains the headings
        entry_type = line[0]
        size_str = line[12:23].strip()  # Adjusted to match the size column
        size = int(size_str) if size_str.isdigit() else 0
        path = line[42:].strip()  # Adjusted to start from column 43 (index 42)
        if entry_type == 'd':
            sub_files = list_remote_files(os.path.join(remote_path, path))
            for sub_path, sub_size in sub_files.items():
                files[os.path.join(path, sub_path)] = sub_size
        else:
            files[path] = size
    # print("[jframe.py] List processed")
    return files

def list_local_files(local_path):
    local_files = {}
    for dp, dn, filenames in os.walk(local_path):
        for f in filenames:
            path = os.path.relpath(os.path.join(dp, f), local_path)
            size = os.path.getsize(os.path.join(local_path, path))
            local_files[path] = size
    return local_files

def download_file(remote_path, local_path):
    # print(f"[jframe.py] Downloading mega:{remote_path} to local:{local_path}")
    subprocess.run(['mega-get', remote_path, local_path], check=True)
    # print("[jframe.py] Download complete")

def sync_files(remote_path, local_path):
    global files_added, files_removed

    remote_files = list_remote_files(remote_path)
    local_files = list_local_files(local_path)

    # Download files from remote if not present locally or if sizes differ
    for remote_file, remote_size in remote_files.items():
        local_file_path = os.path.join(local_path, remote_file)
        if remote_file not in local_files or local_files[remote_file] != remote_size:
            download_file(os.path.join(remote_path, remote_file), local_file_path)
            files_added += 1

    # Remove local files that are not present on the remote
    for local_file in local_files:
        if local_file not in remote_files:
            os.remove(os.path.join(local_path, local_file))
            files_removed += 1

def main():
    parser = argparse.ArgumentParser(description='Synchronize a MEGA directory to a local directory.')
    parser.add_argument('email', help='MEGA account email')
    parser.add_argument('password', help='MEGA account password')
    parser.add_argument('remote_path', help='Remote directory path in MEGA account')
    parser.add_argument('local_path', help='Local directory path')

    args = parser.parse_args()

    print(f"[jframe.py] ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) Starting synchronization")
    mega_login(args.email, args.password)
    try:
        sync_files(args.remote_path, args.local_path)
    finally:
        mega_logout()
        print(f"[jframe.py] ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) Synchronization complete. {files_added} files added, {files_removed} files removed")
        return 188 if files_added > 0 or files_removed > 0 else 0

if __name__ == '__main__':
    main()
