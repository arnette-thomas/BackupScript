# Importations
from modules import backup_abstract
import os
from ftplib import FTP, error_perm
import logging

class BackupSFTP(backup_abstract.BackupAbstract):

    #Constructeur
    def __init__(self, conf):
        super().__init__(conf)