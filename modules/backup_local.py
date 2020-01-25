# Importations
from modules import backup_abstract
import os
import shutil
import logging

class BackupLocal(backup_abstract.BackupAbstract):

    def __init__(self, conf):
        super().__init__(conf)

    def _init_connection(self):
        pass

    def _quit_connection(self):
        pass

    def _run_backup(self, dirs):
        # Pour chaque dossier
        for dir in dirs:
            # Pour le répertoire de destination, on supprime le / du début s'il existe
            savedir = dir[1:] if dir.startswith('/') else dir

            shutil.copytree(dir, os.path.join(os.getcwd(), savedir))
            self.logger.info('Saved {} to local directory {}'.format(dir, os.path.join(os.getcwd(), savedir)))

    def _mkdir(self, name):
        os.mkdir(name)

    def _ls(self):
        return os.listdir()

    def _cd(self, path):
        os.chdir(path)

    def _rmdir(self, name):
        shutil.rmtree(name)