"""Se module se charge de configurer une base données
(PosgreSQL, SQLite ou MySQL) en fonction du choix de l'utilisateur.

class:

    PsqlConfig:

        Cette classe configure la connection d'une base de données PostgreSQL.

        Args:
            password  (str)                     : Mot de passe de l'utilisateur.
            dbname    (list = list("postgres")) : Le nom de la base de données de connection.
            conn_name (str = "connection_psql") : Nom de la connection.
            user      (list = list("postgres")) : Nom de l'utilisateur/rôle qui se connecte.
            "postgres" par défaut.
            host      (str | int = "localhost") : Le nom du serveur de connection.
            "locahost" par défaut.
            port      (int = 5432)              : Port de connection au serveur.
            schema    (list = list("postgres")) : Le schéma de connection dans la base de données.
            "postgres" par défaut.

    SqlitConfig:

    MysqlConfig:

    DbType:

        Enum représentant les types de bases de données et leurs configurations associées.

        Args:
            PSQL = PsqlConfig
            SQLIT = SqlitConfig
            MYSQL = MysqlConfig

    ConfigDb:
"""

# import sqlite3
# import mysql
from typing import Union, Any
from enum import Enum
from pydantic.dataclasses import dataclass

@dataclass
class PsqlConfig:
    """Cette classe configure la connection d'une base de données PostgreSQL.

        Args:

            password  (str)                     : Mot de passe de l'utilisateur.
            dbname    (list = list("postgres")) : Le nom de la base de données de connection.
            conn_name (str = "connection_psql") : Nom de la connection.
            user      (list = list("postgres")) : Nom de l'utilisateur/rôle qui se connecte.
            "postgres" par défaut.
            host      (str | int = "localhost") : Le nom du serveur de connection.
            "locahost" par défaut.
            port      (int = 5432)              : Port de connection au serveur.
            schema    (list = list("postgres")) : Le schéma de connection dans la base de données.
            "postgres" par défaut.
    """

    modal_config = {"extra": "forbid"} # Pas de données exaussive.

    password:  str
    dbname:   list = list("postgres")
    conn_name: str = "connection_psql"
    user:     list = list("postgres")
    host:str | int = "localhost"
    port:      int = 5432
    schema:   list = list("postgres")

@dataclass
class SqlitConfig:
    """Configuration de connection d'une base de données SQLite.
    """

    path: str = "local.db"

@dataclass
class MysqlConfig:
    """Configuration de connection d'une base de données MySQL.
    """

    user:     str = "root"
    password: str = ""
    host:     str = "localhost"

# Enum qui mappe les types de base de données à leurs classes de configuration
class DbType(Enum):
    """Enum représentant les types de bases de données et leurs configurations associées."""
    PSQL  = PsqlConfig
    SQLIT = SqlitConfig
    MYSQL = MysqlConfig

class ConfigDb:
    """Gère la configuration d'une base de données en fonction du choix par l'utilisateur
    (PostgreSQL, MySQL et SQLite).
    """

    def __init__(self, db_type: DbType, **kwargs: Any) -> None:
        """Paramètre d'instanciation de la classe `ConfigDb`.

        Args:
            db_type (DbType): le type de configuration à faire (PSQL, MYSQL ou SQLITE).
        """
        self.db_type = db_type
        self.config  = db_type.value(**kwargs)

    def get_config(self) -> Union[PsqlConfig, MysqlConfig, SqlitConfig]:

        """Retourne la configuration actuelle de la base de données."""
        return self.config

    def __repr__(self) -> str:
        """La représentation de la classe `ConfigDb`.

        Returns:
            str: Le message de représentation de la classe.
        """
        return f"<ConfigDb type={self.db_type.name}, config={self.config}>"
