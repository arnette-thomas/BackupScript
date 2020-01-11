# Importations
from modules import backup_abstract
import os
from ftplib import FTP, error_perm
import logging

class BackupFTP(backup_abstract.BackupAbstract):

    def __init__(self, conf):
        super().__init__(conf)
        self.ftp = FTP()
        self.ftp.encoding = 'utf-8'

    def _init_connection(self):
        # Connexion
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.user, self.password)
        self.logger.info('Connected to server')

    def _quit_connection(self):
        # Deconnexion
        self.ftp.quit()

    def _run_backup(self, dirs):

        # Pour chaque dossier
        for dir in dirs:

            # Création des sous-dossiers
            for subdir in dir[1:].split('/'):
                self._mkdir(subdir)
                self._cd(subdir)

            # Sauvegarde des fichiers
            try:
                self._save_directory(dir)
            except Exception as e:
                self.logger.error("Saving {} : {}".format(dir, str(e)))
            

            # Retour à la racine pour l'itération suivante
            self._cd(self.base_path)

            self.logger.info("{} directory saved to {}".format(dir, self.host))          

    def _save_directory(self, dir):
        # Pour chaque sous-fichier / sous-repertoire
        for name in os.listdir(dir):
            fullpath = os.path.join(dir, name)

            if os.path.isfile(fullpath):    # Si c'est un sous-fichier
                # On l'envoie sur le serveur en binaire
                self.ftp.storbinary('STOR {}'.format(name), open(fullpath, 'rb'))

            elif os.path.isdir(fullpath):   # Si c'est un sous-dossier

                self._mkdir(name)

                # On se déplace dans le dossier nouvellement créé
                self._cd(name)

                # On relance cette méthode pour sauvegarder les sous-fichiers / sous-dossier
                self._save_directory(fullpath)

                # On reviens dans le dossier parent
                self._cd('..')
    

    def _mkdir(self, name):
        try:
            # On crée un sous-dossier du même nom sur le serveur
            self.ftp.mkd(name)
        except error_perm as e:
            # Si le code d'erreur est 550 (le dossier existe déjà), on ignore l'erreur
            # Sinon, on raise l'exception
            if not e.args[0].startswith('550'): raise

    def _ls(self):
        files = self.ftp.mlsd()
        return [name for name, infos in files]

    def _cd(self, path):
        self.ftp.cwd(path)

    def _rmdir(self, name):

        self._cd(name)

        files = [f for f in self._ls() if f != '.' and f != '..']
        for filename in files:
            try:
                self._cd(filename)

                # Si on a réussi, il s'agit d'un dossier
                self._cd('..')
                self._rmdir(filename)
            except Exception:
                # Si on arrive ici, filename est un fichier
                self.ftp.delete(filename)

        self._cd('..')
        self.ftp.rmd(name)