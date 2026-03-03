-- Database: ai_blood_bank
CREATE DATABASE IF NOT EXISTS ai_blood_bank;
USE ai_blood_bank;

-- Table: hospitals
CREATE TABLE IF NOT EXISTS hospitals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hname VARCHAR(100) NOT NULL,
    hcity VARCHAR(100) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL
);

-- Table: receivers
CREATE TABLE IF NOT EXISTS receivers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rname VARCHAR(100) NOT NULL,
    rbg VARCHAR(10) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL
);

-- Table: bloodinfo (inventory units)
CREATE TABLE IF NOT EXISTS bloodinfo (
    bid INT AUTO_INCREMENT PRIMARY KEY,
    hid INT NOT NULL,
    bg VARCHAR(10) NOT NULL,
    FOREIGN KEY (hid) REFERENCES hospitals(id)
);

-- Table: bloodrequest (for forecasting + ML labels later)
CREATE TABLE IF NOT EXISTS bloodrequest (
    reqid INT AUTO_INCREMENT PRIMARY KEY,
    rid INT NOT NULL,
    bg VARCHAR(10) NOT NULL,
    urgency VARCHAR(20) NOT NULL,
    request_date DATE NOT NULL,
    fulfilled INT DEFAULT 0,
    FOREIGN KEY (rid) REFERENCES receivers(id)
);

-- --------------------
-- Sample Data
-- --------------------
INSERT INTO hospitals (hname, hcity, latitude, longitude) VALUES
('City Hospital', 'Bangalore', 12.9716, 77.5946),
('Apollo Care', 'Bangalore', 12.9352, 77.6245),
('Red Cross Center', 'Bangalore', 12.9081, 77.6476),
('Delhi Central Hospital', 'Delhi', 28.6139, 77.2090),
('Mumbai LifeCare', 'Mumbai', 19.0760, 72.8777),
('Chennai Medical Center', 'Chennai', 13.0827, 80.2707);

INSERT INTO bloodinfo (hid, bg) VALUES
(1,'A+'),(1,'A+'),(1,'O+'),
(2,'B+'),(2,'O+'),
(3,'AB+'),(3,'A+'),
(4,'AB+'),
(5,'AB+'),
(6,'AB+');

INSERT INTO receivers (rname, rbg, latitude, longitude) VALUES
('Patient1','A+',12.9600,77.6000);