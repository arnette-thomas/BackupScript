import logging
import os.path
import re
from datetime import date

class BackupAbstract:
    """
    Classe abstraite définissant une solution de Backup (Design Pattern : Strategy)
    """
    
    def __init__(self, conf):
        """Constructeur"""

        self.user = conf['user']
        self.password = conf['pass']
        self.host = conf['host']
        self.port = int(conf['port'])
        self.base_path = conf['path']
        self.versioning = conf['versioning']
        self.versionscount = int(conf['versionscount'])
        self.logger = logging.getLogger('main')

    def run(self, dirs):
        """
        Méthode principale pour lancer une sauvegarde
        """

        self.logger.info('Starting backup')
        try:
            self._init_connection()
            self._create_version_folder()
            self._run_backup(dirs)
            self._quit_connection()
        except Exception as e:
            self.logger.error("{} : {}".format(type(e).__name__, str(e)))
        self.logger.info('End of backup')

    def _init_connection(self):
        """
        Méthode pour initialiser la connexion (si nécessaire)
        """

        raise NotImplementedError

    def _quit_connection(self):
        """
        Méthode pour se déconnecter du serveur (si nécessaire)
        """

        raise NotImplementedError

    def _run_backup(self, dirs):
        """
        Méthode qui effectue la sauvegarde
        """
        raise NotImplementedError

    # Methode pour créer le fichier d'historisation
    # Après cette méthode, le répertoire courant est le répertoire nouvellement créé
    def _create_version_folder(self):
        """
        Methode pour créer le fichier d'historisation
        Après cette méthode, le répertoire courant est le répertoire nouvellement créé
        """

        self._cd(self.base_path)
        existing_dirs = [d for d in self._ls() if re.search(r'^V?[0-9]+$', d)]

        # Numérotation des versions activée
        if self.versioning != 'none':
            if self.versioning == 'version':
                try:
                    # Récupérations des versions sous la forme d'entiers
                    versions = [int(name.replace('V', '')) for name in existing_dirs if name[0] == 'V']

                    last_version = max(versions)
                    first_version = min(versions)
                except ValueError:
                    # Pas de fichier
                    first_version = 0
                    last_version = 0

                old_file = 'V{}'.format(first_version)
                new_file = 'V{}'.format(last_version + 1)

            elif self.versioning == 'date':
                try:
                    # Récupérations des versions sous la forme d'entiers
                    versions = [int(name) for name in existing_dirs if name[0] != 'V']

                    last_version = max(versions)
                    first_version = min(versions)
                except ValueError:
                    # Pas de fichier
                    first_version = 0
                    last_version = 0

                old_file = str(first_version)
                today = date.today()
                new_file = str(today.strftime("%Y%m%d"))
                
            else:
                raise Exception("Versioning type unknown")

            # Si le nombre de versions est trop important, on supprime la plus ancienne
            if len(versions) >= self.versionscount and old_file in existing_dirs :
                self._rmdir(old_file)
                self.logger.info('Removed {} directory'.format(old_file))
        
            self._mkdir(new_file)
            self._cd(new_file)
            self.base_path = os.path.join(self.base_path, new_file)

    def _mkdir(self, name):
        """
        Méthode pour créer un dossier dans le répertoire courant
        name : nom du nouveau dossier
        """

        raise NotImplementedError

    def _cd(self, path):
        """
        Méthode pour changer de répertoire courant
        path : chemin vers le nouveau répertoire courant
        """

        raise NotImplementedError

    def _ls(self):
        """
        Méthode qui retourne la liste des noms des fichiers et repertoires du repertoire courant
        """

        raise NotImplementedError

    def _rmdir(self, name):
        """
        Méthode pour supprimer un répertoire, de manière récursive
        """

        raise NotImplementedError