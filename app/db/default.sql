CREATE TABLE IF NOT EXISTS tickets (
    uuid TEXT,
    nom TEXT,
    prenom TEXT,
    anniversaire TEXT,
    used INTEGER DEFAULT 0,
    PRIMARY KEY(uuid)
);