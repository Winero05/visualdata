"""Ce module permet de mettre les données dans une base de données
(PostgreSQL, MySQL ou SQLite) en fonction du choix de l'utilisateur.

class:
    SaveInDataBase:
    Cette classe permet de faire la sauvegarde des données dans une base de données
    (PostgreSQL, MySQL ou SQLite) en fonction du choix de l'utilisateur.
    PostgreSQL est le choix par défaut.

    methodes:
            creat_table_psql(self):
                Cette méthode se charge de créer une table en PostgreSQL.

                Returns:
                    list[sql.SQL]: Une liste des différentes requête à prendre en compte pour
                    la création d'une table en PostgreSQL est renvoyé.
"""

import psycopg
from psycopg import sql
from pydantic.dataclasses import dataclass
from backend.modules.config_db import DbType, ConfigDb

@dataclass
class SaveInDataBase:
    """Cette classe permet de faire la sauvegarde des données dans une base de données
    (PostgreSQL, MySQL ou SQLite) en fonction du choix de l'utilisateur.
    PostgreSQL est le choix par défaut.
    """

    def creat_table_psql(self, sh_name: str, file_name: str) -> list[sql.SQL | sql.Composed]:
        """Cette méthode se charge de créer une table en PostgreSQL.

        Returns:
            list[sql.SQL]: Une liste des différentes requête à prendre en compte pour
            la création d'une table en PostgreSQL est renvoyé.
        """

        # Pour des raisons de sécurité:
        # Retirer tout les droits au rôle "PUBLIC" (rôle par défaut en PostgreSQL)
        # sur le schéma "public" (schéma par défaut en PostgreSQL).
        revoque_public_access_on_public_sh = sql.SQL("REVOKE ALL ON SCHEMA public FROM PUBLIC;")

        # Créer un nouveau schéma si elle n'existe pas.
        create_sh = sql.SQL(f"CREATE SCHEMA IF NOT EXISTS {sh_name};")

        # Fixer l'usage du schéma pour la création des tables.
        use_sh = sql.SQL(f"SET SCHEMA '{sh_name}';")

        # Pour des raisons de sécurité:
        # Retirer tout les droits au rôle "PUBLIC" (rôle par défaut en PostgreSQL)
        # sur le schéma donné par l'utilisateur "sh_name".
        revoque_public_access_on_sh_ovdd = sql.SQL(f"REVOKE ALL ON SCHEMA {sh_name} FROM PUBLIC;")

        # Création d'une table du nom du fichier chargé si l'utilisateur ne précise aucun nom
        create_table = sql.SQL("CREATE TABLE IF NOT EXISTS {}.{}").format(
            sql.Identifier(sh_name, file_name)
        )

        return [
            revoque_public_access_on_public_sh,
            create_sh, use_sh,
            revoque_public_access_on_sh_ovdd,
            create_table
        ]

    def save_in_psql(self) -> None:
        """Enrégistrer les données dans une base de données.

        Returns:
            None: _description_
        """
        # Récupération des requêtes de création d'une table en psql.
        queries = self.creat_table_psql()

        # Exécution de chaque requête récupéré.
        with psycopg.connect() as conn:
            for query in queries:
                conn.execute(query=query)

        return None
