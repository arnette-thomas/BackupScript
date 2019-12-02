# Importations
import os
from ftplib import FTP, error_perm

class BackupFTP:

    # Constructeur qui initialise les champs en fonction du fichier de conf
    def __init__(self, conf):
        self.user = conf['user']
        self.password = conf['pass']
        self.host = conf['host']
        self.port = int(conf['port'])
        self.base_path = conf['path']
        self.ftp = FTP()
        self.ftp.encoding = 'utf-8'

    # Procédure complète de sauvegarde
    def full_backup(self, dirs):

        # Connexion
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.user, self.password)
        print('CONNECTED')

        # Sélection du bon dossier
        self.ftp.cwd(self.base_path)

        # Sauvegarde des fichiers
        self._save(dirs)

        # Déconnection
        self.ftp.quit()

    # Sauvegarde des données sur le serveur distant
    def _save(self, dirs):

        # Pour chaque dossier
        for dir in dirs:

            # Création des sous-dossiers
            for subdir in dir[1:].split('/'):
                self._make_dir(subdir)
                self.ftp.cwd(subdir)

            # Sauvegarde des fichiers
            self._save_directory(dir)

            # Retour à la racine pour l'itération suivante
            self.ftp.cwd(self.base_path)

            

    def _save_directory(self, dir):
        # Pour chaque sous-fichier / sous-repertoire
        for name in os.listdir(dir):
            fullpath = os.path.join(dir, name)

            if os.path.isfile(fullpath):    # Si c'est un sous-fichier
                print('STORING {} to {}'.format(fullpath, self.host))
                # On l'envoie sur le serveur en binaire
                self.ftp.storbinary('STOR {}'.format(name), open(fullpath, 'rb'))

            elif os.path.isdir(fullpath):   # Si c'est un sous-dossier

                self._make_dir(name)

                # On se déplace dans le dossier nouvellement créé
                self.ftp.cwd(name)

                # On relance cette méthode pour sauvegarder les sous-fichiers / sous-dossier
                self._save_directory(fullpath)

                # On reviens dans le dossier parent
                self.ftp.cwd('..')
    

    def _make_dir(self, name):
        try:
            # On crée un sous-dossier du même nom sur le serveur
            self.ftp.mkd(name)
        except error_perm as e:
            # Si le code d'erreur est 550 (le dossier existe déjà), on ignore l'erreur
            # Sinon, on raise l'exception
            if not e.args[0].startswith('550'): raise