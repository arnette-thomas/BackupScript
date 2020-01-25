# Importations
from modules import backup_abstract
import os
import subprocess
import logging

class BackupRsync(backup_abstract.BackupAbstract):

    def __init__(self, conf):
        super().__init__(conf)

    def _init_connection(self):
        pass

    def _quit_connection(self):
        pass

    # Dans le cas du Rsync, on ne crée pas d'historisation
    def _create_version_folder(self):
        pass

    def _run_backup(self, dirs):
        # Pour chaque dossier
        for dir in dirs:
            remote_base = self.base_path[1:] if self.base_path.startswith('/') else self.base_path

            rsyncaddr = "rsync://{}@{}:{}/{}".format(self.user, self.host, self.port, remote_base)
            try:
                process = subprocess.check_output("sshpass -p {} rsync -avrzR --no-group {} {}".format(self.password, dir, rsyncaddr), stderr=subprocess.STDOUT,shell=True)
            except subprocess.CalledProcessError as ex:
                for line in str(ex.output).split('\\n'):
                    print(line)
                    if "failed" in line:
                        self.logger.error(line)
                        raise

            self.logger.info('Saved {} to {} using Rsync'.format(dir, self.host))