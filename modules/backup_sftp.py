# Importations
from modules import backup_abstract
import os
import pysftp
import logging

class BackupSFTP(backup_abstract.BackupAbstract):

    #Constructeur
    def __init__(self, conf):
        super().__init__(conf)
        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None

    def _init_connection(self):
        self.ftp = pysftp.Connection(self.host, username=self.user, password=self.password, port=self.port, cnopts=self.cnopts)

    def _quit_connection(self):
        self.ftp.close()

    def _run_backup(self,dirs):
        for directory in dirs:
            currdir = directory[1:] if directory[0] == '/' else directory
            self.ftp.makedirs(currdir)
            self._cd(currdir)
            self.ftp.put_r(directory, '.')
            self._cd(self.base_path)
            self.logger.info("{} directory saved to {}".format(directory, self.host))

    def _mkdir(self, name):
        self.ftp.mkdir(name)

    def _cd(self, path):
        self.ftp.cwd(path)

    def _ls(self):
        return self.ftp.listdir()

    def _rmdir(self, name):
        self.ftp.execute('rm -rf {}'.format(name))