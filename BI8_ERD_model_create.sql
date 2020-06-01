-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2020-05-28 11:53:57.825

-- tables
-- Table: Article
CREATE TABLE Article (
    accession varchar(15) NOT NULL,
    doi text NOT NULL,
    article_title text NOT NULL,
    authors text NOT NULL,
    date date NOT NULL,
    CONSTRAINT Article_pk PRIMARY KEY (accession)
);

-- Table: Disease
CREATE TABLE Disease (
    disease_id int NOT NULL,
    disease text NOT NULL,
    inheritance_pattern varchar(30) NULL,
    CONSTRAINT Disease_pk PRIMARY KEY (disease_id)
);

-- Table: Gene
CREATE TABLE Gene (
    gene_id int NOT NULL,
    gene json NOT NULL,
    CONSTRAINT Gene_pk PRIMARY KEY (gene_id)
);

-- Table: Gene_Disease
CREATE TABLE Gene_Disease (
    gene_disease_id int NOT NULL,
    Gene_gene_id int NOT NULL,
    Disease_disease_id int NOT NULL,
    Article_accession varchar(15) NOT NULL,
    CONSTRAINT Gene_Disease_pk PRIMARY KEY (gene_disease_id)
);

-- foreign keys
-- Reference: Gene_Disease_Article (table: Gene_Disease)
ALTER TABLE Gene_Disease ADD CONSTRAINT Gene_Disease_Article FOREIGN KEY Gene_Disease_Article (Article_accession)
    REFERENCES Article (accession);

-- Reference: Gene_Disease_Disease (table: Gene_Disease)
ALTER TABLE Gene_Disease ADD CONSTRAINT Gene_Disease_Disease FOREIGN KEY Gene_Disease_Disease (Disease_disease_id)
    REFERENCES Disease (disease_id);

-- Reference: Gene_Disease_Gene (table: Gene_Disease)
ALTER TABLE Gene_Disease ADD CONSTRAINT Gene_Disease_Gene FOREIGN KEY Gene_Disease_Gene (Gene_gene_id)
    REFERENCES Gene (gene_id);

-- End of file.

