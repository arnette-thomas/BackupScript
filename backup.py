#!/usr/bin/env python3

# Importation
import modules.backup_ftp as bftp
import os

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

    # Gestion des différents target
    if config['target'] == 'ftp':
        ftp_saver = bftp.BackupFTP(config)
        ftp_saver.full_backup(dirs)