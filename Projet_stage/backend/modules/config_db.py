"""Se module se charge de configurer une base données
(PosgreSQL, SQLite ou MySQL) en fonction du choix de l'utilisateur.

class:

    PsqlConfig:

        Cette classe configure la connection d'une base de données PostgreSQL.

        Args:
            password  (str) : Mot de passe de l'utilisateur.
            dbname    (list[str]) : Liste des noms de base de données (par défaut ["postgres"]).
            conn_name (str) : Nom de la connection, (par défaut "connection_psql").
            user      (list[str]) : Nom de l'utilisateur/rôle qui se connecte (par défaut ["postgres"]).
            host      (str | int) : Hôte du serveur (par défaut "locahost").
            port      (int): Port de connection (1-65535), (par défaut 5432).
            db_schema    (list[str]) : Nom du schéma (par défaut ["postgres"]).

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
import os
from dataclasses import dataclass
from typing import Any, Dict, Union, ClassVar, Annotated
from enum import Enum
from pydantic import (
    BaseModel,
    Field,
    model_validator,
    ConfigDict,
    WithJsonSchema
    )
import psycopg

class PsqlConfig(BaseModel):
    """Cette classe configure la connexion à une base de données PostgreSQL."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        strict=True
        )

    password: Annotated[
        str,
        Field(
            ...,
            min_length=1,
            description="Le mot de passe de la base de données."
        ),
        WithJsonSchema(json_schema={'type':'string'}, mode='serialization')
    ]  # Pas de chaîne vide.

    dbname: Annotated[
        list[str],
        Field(
            default_factory=lambda: ["postgres"],
            description="Le nom de la base de données auquel il faut se connées.",
            examples=["postgres"]
        )
    ]  # Accepte une chaîne/liste.

    user: Annotated[
        list[str],
        Field(
            default_factory=lambda: ["postgres"],
            description="Le nom de l'utilisateur avec lequel il faut se connecter.",
            examples=["postgres"],
        )
    ]  # Accepte une chaîne/liste.

    conn_name: Annotated[
        str,
        Field(
            default="connection_psql",
            description="Le nom qu'il faut donner à cette connection à la BD.",
            examples=["connection_psql"],
        )
    ] # Définir un nom pour la connection courante.

    host: Annotated[
        str,
        Field(
            default="localhost",
            description="Le serveur auquel il faut se connecter.",
            examples=["localhost", "127.0.0.1"],
        )
    ] # Définir le nom/adresse du serveur.

    port: Annotated[
        int,
        Field(
            default=5432,
            ge=1,
            le=65535,
            examples=["5432"],
            description="Port PostgreSQL entre 1 et 65535 (par défaut 5432).",
        )
    ] # Définir le port de connection.

    db_schema: Annotated[
        list[str],
        Field(
            default_factory=lambda: ["postgres"],
            description="Le nom du chema auquel il faut se connecter dans la BD.",
            examples=["postgres"],
        )
    ]  # Accepte une chaîne/liste.

    # Lire toute les informations par défaut dans la base de données
    # pour faire un contrôle de valeur saisi par l'utilisateur.
    cached_db: ClassVar[list[str]] = Field(init=False, default_factory=list)
    cached_users: ClassVar[list[str]] = Field(init=False, default_factory=list)
    cached_schema: ClassVar[list[str]] = Field(init=False, default_factory=list)

    # Indicateur pour vérifier si le cache est déjà chargé
    loaded: ClassVar[bool] = Field(init=False, default=False)

    @classmethod
    def load_database_info(cls) -> tuple[list[str], list[str], list[str]]:
        """
        Charge depuis PostgreSQL la liste des **dbname**, **users** et **schemas** existants.
        Retourne un tuple : (all_db, all_users, all_schema)
        """

        # Empêcher rechargement multiple
        if hasattr(cls, "loaded") and cls.loaded:
            return (cls.cached_db, cls.cached_users, cls.cached_schema)

        dbname = os.environ.get("PG_DBNAME", "postgres")
        user = os.environ.get("PG_USER", "postgres")
        password = os.environ.get("PG_PASSWORD", "Adouayom13@#")
        host = os.environ.get("PG_HOST", "localhost")

        dsn = f"dbname={dbname} user={user} password={password} host={host}"

        with psycopg.connect(dsn) as conn:

            # Bases existantes
            result = conn.execute("SELECT datname FROM pg_database;").fetchall()
            all_db = [row[0] for row in result if row[0] not in ("template0", "template1")]

            # Utilisateurs existants
            result = conn.execute("SELECT usename FROM pg_user;").fetchall()
            all_users = [row[0] for row in result]

            # Schémas existants
            result = conn.execute("SELECT nspname FROM pg_namespace;").fetchall()
            all_schema = [
                row[0] for row in result if row[0] not in (
                    "information_schema", "pg_toast", "pg_catalog"
                    )
                ]

        cls.cached_db = all_db
        cls.cached_users = all_users
        cls.cached_schema = all_schema
        cls.loaded = True

        return (all_db, all_users, all_schema)

    @classmethod
    def validate_list_fields(
        cls,
        name: str,
        values: Dict[str, Any],
        allowed_values: list[str]
        ) -> Dict[str, Any]:
        """Cette méthode de classe vérifie que les champs d'instance
        sont bien typé(respecte les types défini par défaut).

        Args:
            name (str): Le nom du champ à vérifier.
            values (Dict[str, Any]): L'ensemble des champs d'instance sous forme d'un dictionnaire.
            allowed_values (list[str]): L'ensemble des informations disponible dans la base.

        Raises:
            ValueError: Une erreur est obtenue si une valeur obtenue n'existe pas dans la BD.
            TypeError: Une erreur est obtenue si le type attendu n'est pas respecté par un champs.
            ValueError: Une erreur est obtenue si une valeur d'une liste n'existe dans la BD.
            TypeError: Une erreur est obtenue si aucun champs ne respecte les types attendu.

        Returns:
            Dict[str, Any]: Un dictionnaire de variable et de valeur d'instance est retourné.
        """

        val = values.get(name)

        # Cas: chaîne simple
        if isinstance(val, str):
            val.strip()
            if val not in allowed_values:
                raise ValueError(
                    f"Valeur invalide, '{name}': '{val}' n'existe pas dans PostgreSQL."
                )
            values[name] = [val]

        # Cas: liste
        elif isinstance(val, list):
            if not all(isinstance(v, str) for v in val):
                raise TypeError(f"Tous les éléments de '{name}' doivent être des chaînes.")

            if not set(val).issubset(allowed_values):
                raise ValueError(
                    f"Au moins une valeur dans '{name}' n'existe pas dans PostgreSQL."
                )

        else:
            raise TypeError(
                f"Le champ '{name}' doit être une chaîne ou une liste de chaînes."
            )
        return values

    # Validation avant création d'instance
    @model_validator(mode='before')
    @classmethod
    def model_validate_inputs(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valide **dbname**, **user** et **db_schema**.
        - string → convertie en liste
        - list[string] → validée
        - autres types → interdits

        Returns:
            Dict[str, Any]: Un dictionnaire contenant les valeurs validées des champs d'instance.
        """

        # Initialisation des variables de classe.
        all_db, all_users, all_schema = cls.load_database_info()

# -----------------------------------------------------------------------------
        # Veuillez décommenter les ligne suivant (celui du "if/elif")
        # afin de pouvoir faire les tests avec le module de test
        # correspondant: "Projet_stage/backend/tests/modules/test_config_db.py".

        # for index_du_test, test_a_faire in enumerate([
        #     "test_dbname_string_converted_to_list",
        #     "test_user_string_converted_to_list",
        #     "test_schema_string_converted_to_list"
        #     ]): # Veuillez modifier le numéro du champ à tester entre 0 - 2.

        #     if index_du_test == 0 and isinstance(values["dbname"], str):
        #         values = cls.validate_list_fields(
        #             name="dbname",
        #             allowed_values=cls.cached_db,
        #             values=values
        #             )
        #         print(f"\nLe test '{test_a_faire}' est fait avec succès.\n")
        #         break
        #     elif index_du_test == 1 and isinstance(values["user"], str):
        #         values = cls.validate_list_fields(
        #             name="user",
        #             allowed_values=cls.cached_users,
        #             values=values
        #             )
        #         print(f"\nLe test '{test_a_faire}' est fait avec succès.\n")
        #         break
        #     elif index_du_test == 2 and isinstance(values["db_schema"], str):
        #         values = cls.validate_list_fields(
        #             name="db_schema",
        #             allowed_values=cls.cached_schema,
        #             values=values
        #             )
        #         print(f"\nLe test '{test_a_faire}' est fait avec succès.\n")
        #         break
        #     elif index_du_test > 2:
        #         print("Veuillez entrer un numéro comprise entre 0 à 2.")
        # return values

# -----------------------------------------------------------------------------


        for field_name, allowed_values in [
            ("dbname", all_db),
            ("user", all_users),
            ("db_schema", all_schema) # Veillez désactiver ce champs si vous vouler faire des tests.
            ]:

            values = cls.validate_list_fields(
                name=field_name,
                allowed_values=allowed_values,
                values=values
                )

        return values

    def to_dsn(self) -> Dict[str, Any]:
        """Construit et renvoie un dictionnaire DSN PostgreSQL."""
        # Récupère le premier élément de la liste.
        db = self.dbname[0]
        user = self.user[0]

        if not db or not user:
            raise ValueError("La base de données ou l'utilisateur ne sont pas définis.")

        # Construction du dictionnaire DSN
        dsn = {
            'dbname': db,
            'user': user,
            'password': self.password,
            'host': self.host,
            'port': self.port,
        }

        # Si un schéma est spécifié, on l'ajoute à l'option 'options'
        if self.db_schema:
            # Si plusieurs schémas sont spécifiés, on les joint avec une virgule
            dsn['options'] = f"-csearch_path={
                ','.join(self.db_schema)
                }" if isinstance(self.db_schema, list) else f"-csearch_path={self.db_schema}"

        return dsn

@dataclass
class SqlitConfig:
    """Configuration de connection d'une base de données SQLite.
    """

    path: str = "local.db"

@dataclass
class MysqlConfig(BaseModel):
    """Configuration de connection d'une base de données MySQL.
    """

    port: int
    dbname: str = "root"
    user: str = "root"
    host: str = "localhost"
    password: str = ""


# Enum qui mappe les types de base de données à leurs classes de configuration
class DbType(Enum):
    """Enum représentant les types de bases de données et leurs configurations associées."""
    PSQL  = PsqlConfig
    SQLIT = SqlitConfig
    MYSQL = MysqlConfig

class ConfigDb:
    """Gère la configuration d'une base de données en fonction du choix par l'utilisateur
    (PostgreSQL, MySQL ou SQLite).
    """

    def __init__(self, db_type: DbType, **kwargs: Any) -> None:
        """Paramètre d'initialisation de chaque instanciation de la classe `ConfigDb`.

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
