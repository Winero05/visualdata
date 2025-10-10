----------------------------------------------------------------------------
------------------------- "I_OPE"."TB_TYPE_CLIENT" -------------------------
----------------------------------------------------------------------------
--- Sélection des données présentes dans la table "I_OPE"."TB_TYPE_CLIENT"
SELECT * FROM "I_OPE"."TB_TYPE_CLIENT";

--- Suppression des données présentes dans la table "I_OPE"."TB_TYPE_CLIENT"
TRUNCATE "I_OPE"."TB_TYPE_CLIENT" CASCADE;

---- Copie des données présentes dans le fichier TB_TYPE_CLIENT.csv
COPY  "I_OPE"."TB_TYPE_CLIENT"("CD_TYPE_CLIENT", "LB_TYPE_CLIENT")
FROM 'C:\Script SQL - Formation PostgreSQL\Section 6\TB_TYPE_CLIENT.csv'
DELIMITER '|'
CSV HEADER;

----------------------------------------------------------------------------
-------------------------- "I_OPE"."TB_CATEGORIE" --------------------------
----------------------------------------------------------------------------
--- Sélection des données présentes dans la table "I_OPE"."TB_CATEGORIE"
SELECT * FROM "I_OPE"."TB_CATEGORIE";

--- Suppression des données présentes dans la table "I_OPE"."TB_CATEGORIE"
TRUNCATE "I_OPE"."TB_CATEGORIE" CASCADE;

---- Copie des données présentes dans le fichier TB_CATEGORIE.csv
COPY  "I_OPE"."TB_CATEGORIE"("CD_CATEGORIE", "LB_CATEGORIE")
FROM 'C:\Script SQL - Formation PostgreSQL\Section 6\TB_CATEGORIE.csv'
DELIMITER '|'
CSV HEADER;


----------------------------------------------------------------------------
----------------------- "I_OPE"."TB_SOUS_CATEGORIE" ------------------------
----------------------------------------------------------------------------
--- Sélection des données présentes dans la table "I_OPE"."TB_SOUS_CATEGORIE"
SELECT * FROM "I_OPE"."TB_SOUS_CATEGORIE";

--- Suppression des données présentes dans la table "I_OPE"."TB_SOUS_CATEGORIE"
TRUNCATE "I_OPE"."TB_SOUS_CATEGORIE" CASCADE;

---- Copie des données présentes dans le fichier TB_SOUS_CATEGORIE.csv
COPY  "I_OPE"."TB_SOUS_CATEGORIE"("CD_SOUS_CATEGORIE", "LB_SOUS_CATEGORIE", "CD_CATEGORIE")
FROM 'C:\Script SQL - Formation PostgreSQL\Section 6\TB_SOUS_CATEGORIE.csv'
DELIMITER '|'
CSV HEADER;


----------------------------------------------------------------------------
----------------------- "I_OPE"."TB_CLIENT" ------------------------
----------------------------------------------------------------------------
--- Supprimer la contrainte not null de la colonne CD_POSTAL_CLIENT
ALTER TABLE "I_OPE"."TB_CLIENT" ALTER COLUMN "CD_POSTAL_CLIENT" DROP NOT NULL;

--- Sélection des données présentes dans la table "I_OPE"."TB_CLIENT"
SELECT * FROM "I_OPE"."TB_CLIENT";

--- Suppression des données présentes dans la table "I_OPE"."TB_CLIENT"
TRUNCATE "I_OPE"."TB_CLIENT" CASCADE;

---- Copie des données présentes dans le fichier TB_CLIENT.csv
COPY  "I_OPE"."TB_CLIENT"("ID_CLIENT", "NOM_CLIENT", "PREN_CLIENT", "CD_POSTAL_CLIENT", "VILLE_CLIENT", "PAYS_CLIENT", "REGION_CLIENT", "CD_TYPE_CLIENT")
FROM 'C:\Script SQL - Formation PostgreSQL\Section 6\TB_CLIENT.csv'
DELIMITER '|'
CSV HEADER;


----------------------------------------------------------------------------
----------------------- "I_OPE"."TB_PRODUIT" ------------------------
----------------------------------------------------------------------------
--- Augmenter la taille de la colonne NOM_PRODUIT.
ALTER TABLE "I_OPE"."TB_PRODUIT" ALTER COLUMN "NOM_PRODUIT" TYPE VARCHAR(255) ;

--- Sélection des données présentes dans la table "I_OPE"."TB_PRODUIT"
SELECT * FROM "I_OPE"."TB_PRODUIT" ;

--- Suppression des données présentes dans la table "I_OPE"."TB_PRODUIT"
TRUNCATE "I_OPE"."TB_PRODUIT" CASCADE;

---- Copie des données présentes dans le fichier TB_PRODUIT.csv
COPY  "I_OPE"."TB_PRODUIT"("CD_PRODUIT", "NOM_PRODUIT", "PRIX_ACHAT_PRODUIT", "PRIX_VENTE_PRODUIT", "CD_SOUS_CATEGORIE")
FROM 'C:\Script SQL - Formation PostgreSQL\Section 6\TB_PRODUIT.csv'
DELIMITER '|'
CSV HEADER;



----------------------------------------------------------------------------
----------------------- "I_OPE"."TB_VENTE" ------------------------
----------------------------------------------------------------------------
--- Sélection des données présentes dans la table "I_OPE"."TB_VENTE"
SELECT * FROM "I_OPE"."TB_VENTE";

--- Suppression des données présentes dans la table "I_OPE"."TB_VENTE"
TRUNCATE "I_OPE"."TB_VENTE" CASCADE;

---- Copie des données présentes dans le fichier TB_VENTE.csv
COPY  "I_OPE"."TB_VENTE"("ID_VENTE", "DT_VENTE", "ID_CLIENT")
FROM 'C:\Script SQL - Formation PostgreSQL\Section 6\TB_VENTE.csv'
DELIMITER '|'
CSV HEADER;



----------------------------------------------------------------------------
------------------------ "I_OPE"."TB_DETAIL_VENTE" -------------------------
----------------------------------------------------------------------------
--- Sélection des données présentes dans la table "I_OPE"."TB_DETAIL_VENTE"
SELECT * FROM "I_OPE"."TB_DETAIL_VENTE";

--- Suppression des données présentes dans la table "I_OPE"."TB_DETAIL_VENTE"
TRUNCATE "I_OPE"."TB_DETAIL_VENTE" CASCADE;

---- Copie des données présentes dans le fichier TB_VENTE.csv
COPY  "I_OPE"."TB_DETAIL_VENTE"("ID_VENTE", "CD_PRODUIT", "QTE_VENTE","PRIX_VENTE","PRIX_ACHAT")
FROM 'C:\Script SQL - Formation PostgreSQL\Section 6\TB_DETAIL_VENTE.csv'
DELIMITER '|'
CSV HEADER;
