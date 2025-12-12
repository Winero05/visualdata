"""Ce module permet de faire les actions au sein
d'une base de données déjà configurée (PostgreSQL, MySQL ou SQLITE).
"""


import os
from dataclasses import (
    dataclass,
    # field
    )
from typing import (
    Annotated,
    # Optional,
    ClassVar,
    Any
    )
import psycopg
from psycopg import sql
from pydantic import (
    Field,
    # BaseModel,
    # ConfigDict
    )

@dataclass
class PSQL:
    """Cette classe permet de faire des actions dans une base données PSQL.
    Les actions faite dans cette classe respecte le CRUD (Create Read Update et Delete).
    """

    dbname: Annotated[
        str,
        Field(
            default="",
            title="dbname",
            examples=["db_medecin"],
            description="Le nom de la base de l'objet à créer dans la base de données.")]
    user: Annotated[
        str,
        Field(
            default="",
            title="user",
            examples=["nom_utilisateur"],
            description="Le nom de la base de l'utilisater à créer dans la base de données.")]
    table: Annotated[
        str,
        Field(
            default="",
            title="table",
            examples=["nom_de_la_table"],
            description="Le nom de la table à créer dans la base de données.")]
    schema: Annotated[
        list[str],
        Field(
            default="",
            title="schema",
            examples=["sh_medecin"],
            description="Le nom de la base de l'objet à créer dans la base de données.")]
    password: Annotated[
        str,
        Field(
            default="",
            title="password",
            examples=["mot_de_passe"],
            description="Le mot de passe utilisateur d'utilisateur.")]
    dsn: Annotated[
        dict[str, Any],
        Field(
            title="dsn",
            examples=[
                {
                    "dbname": 'nom_db',
                    "user": 'nom_utilisateur',
                    "password": 'user_password',
                    "host": 'localhost',
                    "port": '5432',
                    "schema": [
                        'customer_schema_1', 'customer_schema_2', '...', 'customer_schema_n']}],
            description="Ce champs reçois le DSN de connection qu'avait utilisé l'utilisateur"
            " pour configurer la base de données pour la première fois.")]

    cached_db: ClassVar[list[str]] = []
    cached_users: ClassVar[list[str]] = []
    cached_schema: ClassVar[list[str]] = []
    cached_tables: ClassVar[list[str]] = []
    # Indicateur pour vérifier si le cache est déjà chargé
    loaded: ClassVar[bool] = False

    @classmethod
    def creat_obj_in_db(cls, dsn: dict[str, Any], query: sql.Composed) -> None:
        """Cette méthode exécute une requête pour créer un objet dans une base de données.

        Returns:
            None: Rien n'est retournée une fois l'objet crée.
        """

        # dbname = os.environ.get("PG_DBNAME", "postgres")
        # user = os.environ.get("PG_USER", "postgres")
        # password = os.environ.get("PG_PASSWORD", "")
        # host = os.environ.get("PG_HOST", "localhost")
        dbname = dsn["dbname"]
        user = dsn["user"]
        password = dsn["password"]
        host = dsn["host"]

        connection_dsn = f"dbname={dbname} user={user} password={password} host={host}"

        with psycopg.connect(connection_dsn) as conn:
            conn.execute(query=query).fetchall()

    @classmethod
    def load_database_info(
        cls,
        dsn: dict[str, Any]) -> tuple[list[str], list[str], list[str], list[str]]:
        """
        Charge depuis PostgreSQL la liste des **dbname**, **users**, **schema** et **tables** existants.
        Retourne un tuple : (all_db, all_users, all_schema)
        """

        # Empêcher rechargement multiple
        if hasattr(cls, "loaded") and cls.loaded:
            return (cls.cached_db, cls.cached_users, cls.cached_tables, cls.cached_schema)

        # dbname = os.environ.get("PG_DBNAME", "postgres")
        # user = os.environ.get("PG_USER", "postgres")
        # password = os.environ.get("PG_PASSWORD", "")
        # host = os.environ.get("PG_HOST", "localhost")

        dbname = dsn["dbname"]
        user = dsn["user"]
        password = dsn["password"]
        host = dsn["host"]

        connection_dsn = f"dbname={dbname} user={user} password={password} host={host}"

        with psycopg.connect(connection_dsn) as conn:

            # Bases existantes
            result = conn.execute("SELECT datname FROM pg_database;").fetchall()
            all_db = [row[0] for row in result if row[0] not in ("template0", "template1")]

            # Utilisateurs existants
            result = conn.execute("SELECT usename FROM pg_user;").fetchall()
            all_users = [row[0] for row in result]

            # Schémas existants
            result = conn.execute("SELECT nspname FROM pg_namespace;").fetchall()
            all_schema = [
                row[0] for row in result if row[0] not in ("information_schema", "pg_toast", "pg_catalog")]

            # Tables existants
            result = conn.execute("SELECT name FROM pg_database;").fetchall()
            all_tables = [row[0] for row in result if row[0] not in ("pg_default", "pg_global")]

        cls.cached_db = all_db
        cls.cached_users = all_users
        cls.cached_schema = all_schema
        cls.cached_tables = all_tables
        cls.loaded = True

        return (all_db, all_users, all_tables, all_schema)

    # ---------------- CREATE ACTIONS ----------------

    def create_db(self) -> None:
        """Cette méthode crée une base de données.

        Returns:
            None: Rien n'est retourné à l'utilisateur après réation.
        """


        query = sql.SQL("""CREATE DATABASE IF NOT EXISTS {};""").format(sql.Identifier(self.dbname))
        # PSQL.creat_obj_in_db(query=query)
        return None

    def create_user(self) -> sql.Composed:
        """Cette méthode retoure une requête de permettant la création un utilisateur dans une BD.

        Returns:
            sql.Composed: Rêquete à utiliser pour la création d'une base données.
        """
        return sql.SQL("""CREATE ROLE IF NOT EXISTS {};""").format(sql.Identifier(self.dbname, self.user))

    def create_table(self) -> sql.Composed:
        """Cette méthode retoure une requête de permettant la création une table dans une BD.

        Returns:
            sql.Composed: Rêquete à utiliser pour la création d'une base données.
        """
        return sql.SQL("CREATE TABLE IF NOT EXIST {};").format(sql.Identifier(self.dbname, self.schema, self.table))

    def create_schema(self) -> sql.Composed:
        """Cette méthode retoure une requête permettant la création un schéma dans une BD.

        Returns:
            sql.SQL: Rêquete à utiliser pour la création d'une base données.
        """
        return sql.SQL("CREATE SCHEMA IF NOT EXISTS{};").format(sql.Identifier(self.dbname, self.schema))

    # ---------------- READ ACTIONS ----------------

    def read_db(self) -> list[str]:
        """Cette méthode retourne une liste contenant les DB présent dans le serveur utilisé.

        Returns:
            list[str]: Liste de chaîne de caractère désignant le nom des BD.
        """
        return PSQL.load_database_info()[0]

    def read_user(self) -> list[str]:
        """Cette méthode retourne une requête permettant d'afficher tous les utilisateurs présent dans une BD.

        Returns:
            list[str]: Liste de chaîne de caractère désignant le nom des utilistateurs de la BD.
        """
        return PSQL.load_database_info()[1]

    def read_table(self) -> list[str]:
        """Cette méthode retourne une requête permettant d'afficher toutes les table présent dans une BD.

        Returns:
            list[str]: Liste de chaîne de caractère désignant le nom des tables présent dans la BD.
        """
        return PSQL.load_database_info()[2]

    def read_schema(self) -> list[str]:
        """Cette méthode retourne une requête permettant d'afficher tous les schéma présent dans une BD.

        Returns:
            : _description_
        """
        return PSQL.load_database_info()[3]

    # ---------------- UPDATE ACTIONS ----------------
    
    def update_db(self) -> Any:
        """Cette méthode retourne une requête permettant de modifier le nom d'une BD présent dans le serveur utilisé.

        Returns:
            Any: _description_
        """

    def update_user(self) -> Any:
        """Cette méthode retourne une requête permettant de modifier le nom d'un utilisateur présent dans une BD.

        Returns:
            Any: _description_
        """

    def update_table(self) -> Any:
        """Cette méthode retourne une requête permettant de modifier le nom d'une table présent dans une BD.

        Returns:
            Any: _description_
        """

    def update_schema(self) -> Any:
        """Cette méthode retourne une requête permettant de modifier le nom d'un schéma présent dans une BD.

        Returns:
            Any: _description_
        """

    def update_password(self) -> Any:
        """Cette méthode retourne une requête permettant de modifier le mot de passe d'un utilisateur présent dans une BD.

        Returns:
            Any: _description_
        """
    
    # ---------------- DELETE ACTIONS ----------------
    
    def delete_db(self) -> Any:
        """Cette méthode retourne une requête permettant de supprimer une BD présent dans le serveur utilisé.

        Returns:
            Any: _description_
        """

    def delete_user(self) -> Any:
        """Cette méthode retourne une requête permettant de supprimer un utilisateur présent dans une BD.

        Returns:
            Any: _description_
        """

    def delete_table(self) -> Any:
        """Cette méthode retourne une requête permettant de supprimer une table présent dans une BD.

        Returns:
            Any: _description_
        """

    def delete_schema(self) -> Any:
        """Cette méthode retourne une requête permettant de supprimer un schéma présent dans une BD.

        Returns:
            Any: _description_
        """

    def delete_password(self) -> Any:
        """Cette méthode retourne une requête permettant de supprimer un mot de passe présent dans une BD.

        Returns:
            Any: _description_
        """

@dataclass
class ActionsInDb:
    """Cette classe permet de faire des actions
    au sein d'une base de données.
    """

    def action_in_psql(self) -> None:
        """Cette méthode permet de faire des actions
        dans une base de données PostgreSQL.
        """

    def action_in_sqlite(self) -> None:
        """Cette méthode permet de faire des actions
        dans une base de données sqlite.
        """

    def action_in_mysql(self) -> None:
        """Cette méthode permet de faire des actions
        dans une base de données mysql.
        """
