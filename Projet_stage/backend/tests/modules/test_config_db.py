"""Ce test est fait pour le module "Projet_stage/backend/modules/db_config.py"
"""

# Chemin du test Projet_stage/backend/tests/modules/test_db_config.py

from typing import Generator
import pytest
from cfg.config_db import (
    PsqlConfig,
    SqlitConfig,
    MysqlConfig,
    ConfigDb,
    DbType
    )

from pydantic import ValidationError

@pytest.fixture(autouse=True)
def patch_psql_load(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Prevent actual DB calls and provide cached allowed values for validations"""
    monkeypatch.setattr(
        PsqlConfig,
        "_load_database_info",
        classmethod(lambda cls: ([], [], [])),
        raising=False
        )
    PsqlConfig.cached_db = ["postgres", "db_ovdd", "mydb", "db1", "db2", "mydbname"]
    PsqlConfig.cached_users = ["postgres", "admin", "myuser"]
    PsqlConfig.cached_schema = ["postgres", "public", "sh_ovdd"]
    yield


class TestPsqlConfig:
    """Tester la classer PsqlConfig.
    """
    def test_instance_with_required_password(self) -> None:
        """Tester les variables d'instance de la classe PsqlConfig.
        """
        cfg = PsqlConfig(password="test123", dbname="db_ovdd", user="postgres", db_schema="sh_ovdd")
        assert cfg.password == "test123"
        assert cfg.dbname == ["db_ovdd"]
        assert cfg.user == ["postgres"]
        assert cfg.host == "localhost"
        assert cfg.port == 5432
        assert cfg.db_schema == ["sh_ovdd"]
        assert cfg.conn_name == "connection_psql"

    def test_dbname_string_converted_to_list(self) -> None:
        cfg = PsqlConfig(password="test123", dbname="postgres", user=["myuser"])
        assert cfg.dbname == ["postgres"]

    def test_user_string_converted_to_list(self) -> None:
        cfg = PsqlConfig(password="test123", dbname=["mydbname"], user="postgres")
        assert cfg.user == ["postgres"]

    def test_schema_string_converted_to_list(self) -> None:
        cfg = PsqlConfig(password="test123", dbname=["mydbname"], user=["myuser"], db_schema="public")
        assert cfg.db_schema == ["public"]

    def test_dbname_as_list(self) -> None:
        cfg = PsqlConfig(password="test123", dbname=["db1", "db2"], user="myuser")
        assert cfg.dbname == ["db1", "db2"]

    # Vérifier que le champ de mot de passe est données.
    def test_empty_password_raises_error(self) -> None:
        """Vérifier que le champ de mot de passe n'est pas vide.

        Raises:
            ValidationError: Error de validation si le passe n'est pas données.
        """
        with pytest.raises(ValidationError, match="Le mot de passe ne peut pas être vide"):
            PsqlConfig(password="", dbname=["postgres"], user=["postgres"])
            raise ValidationError("Le mot de passe ne peut pas être vide.")

    def test_whitespace_only_password_raises_error(self) -> None:
        with pytest.raises(ValidationError, match="Le mot de passe ne peut pas être vide"):
            PsqlConfig(password="   ", dbname=["postgres"], user=["postgres"])
            raise ValidationError("Le mot de passe ne peut pas être vide.")

    def test_port_validation_min(self) -> None:
        """Test la validation du port minimum."""
        with pytest.raises(ValueError):
            PsqlConfig(password="test123", port=0)

    def test_port_validation_max(self) -> None:
        """Test la validation du port maximum."""
        with pytest.raises(ValueError):
            PsqlConfig(password="test123", port=65536)

    def test_valid_port_range(self) -> None:
        """Test les ports valides."""
        config1 = PsqlConfig(password="test123", port=1)
        config2 = PsqlConfig(password="test123", port=65535)
        assert config1.port == 1
        assert config2.port == 65535

    def test_custom_host(self) -> None:
        """Test la configuration d'un host personnalisé."""
        config = PsqlConfig(password="test123", host="192.168.1.1")
        assert config.host == "192.168.1.1"

    def test_invalid_dbname_type_raises_error(self) -> None:
        """Test qu'un type invalide pour dbname lève une erreur."""
        with pytest.raises(TypeError):
            PsqlConfig(password="test123", dbname=123)

    def test_to_dsn(self) -> None:
        """Test la génération de la chaîne DSN PostgreSQL."""
        config = PsqlConfig(
            password="mypass",
            dbname="mydb",
            user="admin",
            host="db.example.com",
            port=5433,
            db_schema="public"
        )
        dsn = config.to_dsn()
        assert dsn == "postgresql://admin:mypass@db.example.com:5433/mydb?options=-csearch_path=public"

    def test_to_dsn_with_defaults(self) -> None:
        """Test la génération DSN avec les valeurs par défaut."""
        config = PsqlConfig(password="pass123")
        dsn = config.to_dsn()
        assert dsn == "postgresql://postgres:pass123@localhost:5432/postgres?options=-csearch_path=postgres"

    def test_custom_conn_name(self) -> None:
        """Test la configuration du nom de connexion."""
        config = PsqlConfig(password="test123", conn_name="my_connection")
        assert config.conn_name == "my_connection"

    def test_essaie_de_connection(self) -> None:
        """Test de la méthode essaie_de_connection.
        """
        chargeur = PsqlConfig(password="Adouayom13@#")
        chargeur.essaie_de_connection()

class TestSqlitConfig:
    """Cette classe test la classe SqlitConfig."""

    def test_instance_with_defaults(self) -> None:
        """Test l'instanciation avec les valeurs par défaut."""
        config = SqlitConfig()
        assert config.path == "local.db"

    def test_custom_path(self) -> None:
        """Test la configuration d'un chemin personnalisé."""
        config = SqlitConfig(path="/tmp/my_database.db")
        assert config.path == "/tmp/my_database.db"


class TestMysqlConfig:
    """Cette classe test la classe MysqlConfig."""

    def test_instance_with_defaults(self) -> None:
        """Test l'instanciation avec les valeurs par défaut."""
        config = MysqlConfig()
        assert config.user == "root"
        assert config.password == ""
        assert config.host == "localhost"

    def test_custom_credentials(self) -> None:
        """Test la configuration avec des identifiants personnalisés."""
        config = MysqlConfig(user="admin", password="secret", host="db.server.com")
        assert config.user == "admin"
        assert config.password == "secret"
        assert config.host == "db.server.com"


class TestDbType:
    """Cette classe test l'enum DbType."""

    def test_db_type_psql(self) -> None:
        """Test que DbType.PSQL correspond à PsqlConfig."""
        assert DbType.PSQL.value == PsqlConfig

    def test_db_type_sqlit(self) -> None:
        """Test que DbType.SQLIT correspond à SqlitConfig."""
        assert DbType.SQLIT.value == SqlitConfig

    def test_db_type_mysql(self) -> None:
        """Test que DbType.MYSQL correspond à MysqlConfig."""
        assert DbType.MYSQL.value == MysqlConfig


class TestConfigDb:
    """Cette classe test la classe ConfigDb."""

    def test_config_db_psql(self) -> None:
        """Test l'instanciation de ConfigDb avec PostgreSQL."""
        config_db = ConfigDb(DbType.PSQL, password="test123")
        assert isinstance(config_db.config, PsqlConfig)
        assert config_db.db_type == DbType.PSQL

    def test_config_db_sqlit(self) -> None:
        """Test l'instanciation de ConfigDb avec SQLite."""
        config_db = ConfigDb(DbType.SQLIT, path="test.db")
        assert isinstance(config_db.config, SqlitConfig)
        assert config_db.db_type == DbType.SQLIT

    def test_config_db_mysql(self) -> None:
        """Test l'instanciation de ConfigDb avec MySQL."""
        config_db = ConfigDb(DbType.MYSQL, user="admin", password="pass")
        assert isinstance(config_db.config, MysqlConfig)
        assert config_db.db_type == DbType.MYSQL

    def test_get_config_psql(self) -> None:
        """Test la récupération de la configuration PostgreSQL."""
        config_db = ConfigDb(DbType.PSQL, password="test123")
        config = config_db.get_config()
        assert isinstance(config, PsqlConfig)
        assert config.password == "test123"

    def test_get_config_sqlit(self) -> None:
        """Test la récupération de la configuration SQLite."""
        config_db = ConfigDb(DbType.SQLIT, path="custom.db")
        config = config_db.get_config()
        assert isinstance(config, SqlitConfig)
        assert config.path == "custom.db"

    def test_repr_psql(self) -> None:
        """Test la représentation en chaîne pour PostgreSQL."""
        config_db = ConfigDb(DbType.PSQL, password="test123")
        repr_str = repr(config_db)
        assert "ConfigDb" in repr_str
        assert "PSQL" in repr_str

    def test_repr_sqlit(self) -> None:
        """Test la représentation en chaîne pour SQLite."""
        config_db = ConfigDb(DbType.SQLIT)
        repr_str = repr(config_db)
        assert "ConfigDb" in repr_str
        assert "SQLIT" in repr_str

    def test_repr_mysql(self) -> None:
        """Test la représentation en chaîne pour MySQL."""
        config_db = ConfigDb(DbType.MYSQL)
        repr_str = repr(config_db)
        assert "ConfigDb" in repr_str
        assert "MYSQL" in repr_str




    def test_port_validation_min(self) -> None:
        with pytest.raises(ValidationError):
            PsqlConfig(password="test123", dbname=["postgres"], user=["postgres"], port=0)

    def test_port_validation_max(self) -> None:
        with pytest.raises(ValidationError):
            PsqlConfig(password="test123", dbname=["postgres"], user=["postgres"], port=65536)

    def test_valid_port_range(self) -> None:
        c1 = PsqlConfig(password="test123", dbname=["postgres"], user=["postgres"], port=1)
        c2 = PsqlConfig(password="test123", dbname=["postgres"], user=["postgres"], port=65535)
        assert c1.port == 1
        assert c2.port == 65535

    def test_custom_host(self) -> None:
        c = PsqlConfig(password="test123", dbname=["postgres"], user=["postgres"], host="192.168.1.1")
        assert c.host == "192.168.1.1"

    def test_invalid_dbname_type_raises_error(self) -> None:
        with pytest.raises(ValidationError):
            PsqlConfig(password="test123", dbname=123, user=["postgres"])

    def test_to_dsn(self) -> None:
        cfg = PsqlConfig(
            password="mypass",
            dbname="mydb",
            user="admin",
            host="db.example.com",
            port=5433,
            db_schema="public"
        )
        expected = {
            "dbname": "mydb",
            "user": "admin",
            "password": "mypass",
            "host": "db.example.com",
            "port": 5433,
            "options": "-csearch_path=public",
        }
        assert cfg.to_dsn() == expected

    def test_to_dsn_with_defaults_provided_db_user(self) -> None:
        # Provide dbname and user (required by model) and verify defaults for host/port/db_schema
        cfg = PsqlConfig(password="pass123", dbname="postgres", user="postgres")
        expected = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "pass123",
            "host": "localhost",
            "port": 5432,
            "options": "-csearch_path=postgres",
        }
        assert cfg.to_dsn() == expected

    def test_custom_conn_name(self) -> None:
        cfg = PsqlConfig(password="test123", dbname=["postgres"], user=["postgres"], conn_name="my_connection")
        assert cfg.conn_name == "my_connection"


class TestSqlitConfig:
    def test_instance_with_defaults(self) -> None:
        cfg = SqlitConfig()
        assert cfg.path == "local.db"

    def test_custom_path(self) -> None:
        cfg = SqlitConfig(path="/tmp/my_database.db")
        assert cfg.path == "/tmp/my_database.db"


class TestMysqlConfig:
    def test_instance_with_defaults(self) -> None:
        cfg = MysqlConfig()
        assert cfg.user == "root"
        assert cfg.password == ""
        assert cfg.host == "localhost"

    def test_custom_credentials(self) -> None:
        cfg = MysqlConfig(user="admin", password="secret", host="db.server.com")
        assert cfg.user == "admin"
        assert cfg.password == "secret"
        assert cfg.host == "db.server.com"


class TestDbType:
    def test_db_type_psql(self) -> None:
        assert DbType.PSQL.value == PsqlConfig

    def test_db_type_sqlit(self) -> None:
        assert DbType.SQLIT.value == SqlitConfig

    def test_db_type_mysql(self) -> None:
        assert DbType.MYSQL.value == MysqlConfig


class TestConfigDb:
    def test_config_db_psql(self) -> None:
        cfg_db = ConfigDb(DbType.PSQL, password="test123", dbname=["postgres"], user=["postgres"])
        assert isinstance(cfg_db.config, PsqlConfig)
        assert cfg_db.db_type == DbType.PSQL

    def test_config_db_sqlit(self) -> None:
        cfg_db = ConfigDb(DbType.SQLIT, path="test.db")
        assert isinstance(cfg_db.config, SqlitConfig)
        assert cfg_db.db_type == DbType.SQLIT

    def test_config_db_mysql(self) -> None:
        cfg_db = ConfigDb(DbType.MYSQL, user="admin", password="pass")
        assert isinstance(cfg_db.config, MysqlConfig)
        assert cfg_db.db_type == DbType.MYSQL

    def test_get_config_psql(self) -> None:
        cfg_db = ConfigDb(DbType.PSQL, password="test123", dbname=["postgres"], user=["postgres"])
        cfg = cfg_db.get_config()
        assert isinstance(cfg, PsqlConfig)
        assert cfg.password == "test123"

    def test_get_config_sqlit(self) -> None:
        cfg_db = ConfigDb(DbType.SQLIT, path="custom.db")
        cfg = cfg_db.get_config()
        assert isinstance(cfg, SqlitConfig)
        assert cfg.path == "custom.db"

    def test_repr_psql(self) -> None:
        cfg_db = ConfigDb(DbType.PSQL, password="test123", dbname=["postgres"], user=["postgres"])
        r = repr(cfg_db)
        assert "ConfigDb" in r
        assert "PSQL" in r

    def test_repr_sqlit(self) -> None:
        cfg_db = ConfigDb(DbType.SQLIT)
        r = repr(cfg_db)
        assert "ConfigDb" in r
        assert "SQLIT" in r

    def test_repr_mysql(self) -> None:
        cfg_db = ConfigDb(DbType.MYSQL)
        r = repr(cfg_db)
        assert "ConfigDb" in r
        assert "MYSQL" in r

