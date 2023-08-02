import os
import shutil
import argparse
import time
import logging

"""create logger file"""
logging.basicConfig(filename='sync.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

"""Parse command line arguments"""
# TODO 4
parser = argparse.ArgumentParser(description='Synchronize two folders')
parser.add_argument('source', type=str,
                    help='Source folder path')
parser.add_argument('replica', type=str,
                    help='Replica folder path')
parser.add_argument('-i', type=int, default=60,
                    help='Synchronization interval in seconds (default: 60)')
args = parser.parse_args()


"""Check if source and replica folders exist"""
if not os.path.isdir(args.source):
    print(f'Error: {args.source} is not a valid folder path')
    logging.error(f'Source folder - {args.source} - does not exist')
    exit(1)
if not os.path.isdir(args.replica):
    print(f'Error: {args.replica} is not a valid folder path')
    logging.error(f'Source folder - {args.replica} - does not exist')
    exit(1)

# TODO 1


def sync_folders(source_path, replica_path):
    modified_files = []
    # iterate over the files and folders in the source folder
    for root, dirs, files in os.walk(source_path):
        # check if the corresponding subfolder exists in the replica folder
        replica_root = os.path.join(
            replica_path, os.path.relpath(root, source_path))
        if not os.path.isdir(replica_root):
            os.makedirs(replica_root)
        # copy new or modified files from the source to the replica folder
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_root, file)
            source_stat = os.stat(source_file)
            replica_stat = os.stat(replica_file) if os.path.exists(
                replica_file) else None
            if replica_stat is None or source_stat.st_mtime > replica_stat.st_mtime:
                shutil.copy2(source_file, replica_file)
                modified_files.append(replica_file)
                log_operation(
                    'create' if replica_stat is None else 'copy', replica_file)
        # delete files or folders that are in the replica but not in the source folder
        for replica_file in os.listdir(replica_root):
            source_file = os.path.join(root, replica_file)
            replica_file = os.path.join(replica_root, replica_file)
            if not os.path.exists(source_file):
                if os.path.isdir(replica_file):
                    shutil.rmtree(replica_file)
                else:
                    os.remove(replica_file)
                modified_files.append(replica_file)
                log_operation('delete', replica_file)
    return modified_files


def log_operation(operation, path):
    """ Log the operation performed on the path """
    message = f'{operation.upper()} - {path}'
    print(message)
    logging.info(message)


# TODO 2: set up a loop to periodically synchronize the folders
while True:
    sync_folders(args.source, args.replica)
    time.sleep(args.i)
