-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2020-05-27 17:18:04.403

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

-- Table: Databron
CREATE TABLE Databron (
    `database` varchar(15) NOT NULL,
    Gene_gene_id int NOT NULL,
    Disease_disease_id int NOT NULL,
    Article_accession varchar(15) NOT NULL,
    CONSTRAINT Databron_pk PRIMARY KEY (`database`)
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

-- foreign keys
-- Reference: Databron_Article (table: Databron)
ALTER TABLE Databron ADD CONSTRAINT Databron_Article FOREIGN KEY Databron_Article (Article_accession)
    REFERENCES Article (accession);

-- Reference: Databron_Disease (table: Databron)
ALTER TABLE Databron ADD CONSTRAINT Databron_Disease FOREIGN KEY Databron_Disease (Disease_disease_id)
    REFERENCES Disease (disease_id);

-- Reference: Databron_Gene (table: Databron)
ALTER TABLE Databron ADD CONSTRAINT Databron_Gene FOREIGN KEY Databron_Gene (Gene_gene_id)
    REFERENCES Gene (gene_id);

-- End of file.

