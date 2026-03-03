-- ===============================
-- AI Blood Bank System - Strong SQL Schema
-- ===============================

CREATE DATABASE IF NOT EXISTS ai_blood_bank;
USE ai_blood_bank;

-- ===============================
-- Hospitals Table
-- ===============================
CREATE TABLE hospitals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hname VARCHAR(150) NOT NULL,
    hcity VARCHAR(100) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hcity ON hospitals(hcity);

-- ===============================
-- Receivers Table
-- ===============================
CREATE TABLE receivers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rname VARCHAR(150) NOT NULL,
    rbg VARCHAR(5) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rbg ON receivers(rbg);

-- ===============================
-- Blood Inventory Table
-- (Better than repeating rows)
-- ===============================
CREATE TABLE blood_inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hospital_id INT NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    units_available INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE
);

CREATE INDEX idx_blood_group ON blood_inventory(blood_group);
CREATE INDEX idx_hospital_bg ON blood_inventory(hospital_id, blood_group);

-- ===============================
-- Blood Requests Table
-- ===============================
CREATE TABLE blood_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receiver_id INT NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    urgency ENUM('critical','high','medium','low') NOT NULL,
    request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    fulfilled BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (receiver_id) REFERENCES receivers(id) ON DELETE CASCADE
);

CREATE INDEX idx_request_bg ON blood_requests(blood_group);
CREATE INDEX idx_request_urgency ON blood_requests(urgency);

-- ===============================
-- SAMPLE DATA
-- ===============================

INSERT INTO hospitals (hname, hcity, latitude, longitude) VALUES
('City Hospital', 'Bangalore', 12.9716, 77.5946),
('Apollo Care', 'Bangalore', 12.9352, 77.6245),
('Red Cross Center', 'Bangalore', 12.9081, 77.6476),
('Delhi Central Hospital', 'Delhi', 28.6139, 77.2090),
('Mumbai LifeCare', 'Mumbai', 19.0760, 72.8777),
('Chennai Medical Center', 'Chennai', 13.0827, 80.2707);

INSERT INTO blood_inventory (hospital_id, blood_group, units_available) VALUES
(1, 'A+', 12),
(1, 'O+', 6),
(2, 'B+', 8),
(2, 'O+', 5),
(3, 'AB+', 4),
(3, 'A+', 3),
(4, 'AB+', 10),
(5, 'AB+', 7),
(6, 'AB+', 9);

INSERT INTO receivers (rname, rbg, latitude, longitude) VALUES
('Patient1','A+',12.9600,77.6000);