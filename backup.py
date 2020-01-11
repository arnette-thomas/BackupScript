#!/usr/bin/env python3

# Importation
from modules import backup_ftp, backup_sftp
import os
import logging

def get_config():
    conf = {}
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backup.conf')
    with open(conf_path) as file_conf:
        for line in file_conf:
            if line[0] in "#\n": continue
            args = line.split('=')
            conf[args[0]] = args[1].replace("\n", "")

    return conf

def get_dirs(conf):
    dirs_str = conf['dirs']
    dirs_str = dirs_str.replace(" ", "")
    return dirs_str.split(',')

if __name__ == '__main__':
    config = get_config()
    dirs = get_dirs(config)

    # Configuration du logger
    logging.basicConfig(filename=config['logfile'],
                            filemode='a',
                            format='%(asctime)s - %(levelname)s : %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)

    # Gestion des différents target
    saver = None
    if config['target'] == 'ftp':
        saver = backup_ftp.BackupFTP(config)
    saver.run(dirs)