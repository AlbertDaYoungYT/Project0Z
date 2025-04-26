DROP DATABASE IF EXISTS project_z0;
CREATE DATABASE project_z0;

CREATE TABLE IF NOT EXISTS project_z0.sector_biomes (
    sector_biome VARCHAR(255) PRIMARY KEY,
    biome_title VARCHAR(255),
    biome_description VARCHAR(255),
    biome_type VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS project_z0.sectors (
    sector_id INT AUTO_INCREMENT PRIMARY KEY,
    sector_name VARCHAR(255),
    sector_lat DECIMAL(16,8),
    sector_lon DECIMAL(16,8),
    sector_biome VARCHAR(255),
    max_health DECIMAL(32,10) DEFAULT 10000,
    health DECIMAL(32,10) DEFAULT 10000,
    regeneration_amount DECIMAL(32,10) DEFAULT 10,
    foes_level INT DEFAULT 0,
    missions_liberated INT DEFAULT 0,
    missions_lost INT DEFAULT 0,
    soldiers_fallen INT DEFAULT 0,
    foes_eradicated INT DEFAULT 0,
    accidentals INT DEFAULT 0,
    FOREIGN KEY (sector_biome) REFERENCES project_z0.sector_biomes(sector_biome)
);

CREATE TABLE IF NOT EXISTS project_z0.ships (
    ship_id VARCHAR(255) PRIMARY KEY,
    ship_name VARCHAR(255) NOT NULL,
    ship_location INT NOT NULL,
    FOREIGN KEY (ship_location) REFERENCES project_z0.sectors(sector_id)
);

CREATE TABLE IF NOT EXISTS project_z0.accounts (
    account_number INT AUTO_INCREMENT PRIMARY KEY,
    account_id VARCHAR(255) UNIQUE NOT NULL,  -- Added UNIQUE constraint
    ship_id VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    passwd VARCHAR(255) NOT NULL,
    banned_amount INT DEFAULT 0,
    latest_ban TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ship_id) REFERENCES project_z0.ships(ship_id)
);

CREATE TABLE IF NOT EXISTS project_z0.banks (
    bank_number INT AUTO_INCREMENT PRIMARY KEY,
    account_id VARCHAR(255) NOT NULL,
    bank_balance DECIMAL(16,4),
    bank_currency VARCHAR(8),
    bank_silver DECIMAL(16,4),
    bank_gold DECIMAL(16,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES project_z0.accounts(account_id)
);
