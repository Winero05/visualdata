"""Se module se charge de configurer une base données
(PosgreSQL, SQLite ou MySQL) en fonction du choix de l'utilisateur.

class:

    PsqlConfig
    
        Args:
            dbname (str) : Le nom de la base de données auquelle il faut se connecter.
            password (str) : Mot de passe de l'utilisateur.
            conn_name (str) : Nom de la connection.
            user (str) : Nom de l'utilisateur de la connection à la base de données.
            "postgres" par défaut.
            host (str | int) : Le nom du serveur de connection.
            "locahost" ou 127.0.0.1 par défaut.
            port (int) : 5432 est le port par défaut.
            schema (str) : Le schéma de connection dans la base de données.
            "postgres" par défaut.

    SqlitConfig
    MysqlConfig
    ConfigDb(Union[PsqlConfig, SqlitConfig, MysqlConfig], Enum)
"""

# import sqlite3
# import mysql
from typing import Union
from enum import Enum
from pydantic.dataclasses import dataclass

@dataclass
class PsqlConfig:
    """Cette classe configuraiton de connection de la base de données PostgreSQL.
    """

    modal_config = {"extra": "forbid"} # Pas de données exaussive.

    password:  str
    dbname:    list = list("postgres").append("sh_ovdd")
    conn_name: str = "connection_psql"
    user:      str = "postgres"
    host:str | int = "localhost"
    port:str | int = 5432
    schema:    str = "public"

    # def conf_schema(self):

@dataclass
class SqlitConfig:
    """Configuration de connection d'une base de données SQLite.
    """

@dataclass
class MysqlConfig:
    """Configuration de connection d'une base de données MySQL.
    """

@dataclass
class ConfigDb(Union[PsqlConfig, SqlitConfig, MysqlConfig], Enum): # type: ignore[misc]
    """Configuration d'une base de données en fonction du choix de l'utilisateur
    (PostgreSQL, MySQL et SQLite).
    """

    PSQL  = PsqlConfig
    SQLIT = SqlitConfig
    MYSQL = MysqlConfig
