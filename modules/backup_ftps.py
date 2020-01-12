from ftplib import FTP_TLS
from modules import backup_ftp

class BackupFTPS(backup_ftp.BackupFTP):
    
    def __init__(self, conf):
        super().__init__(conf)
        self.ftp = FTP_TLS(timeout=10)
        self.ftp.encoding = 'utf-8'

    def _init_connection(self):
        super()._init_connection()
        self.ftp.prot_p()