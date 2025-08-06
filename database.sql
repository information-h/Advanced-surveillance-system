CREATE DATABASE surveillance;
USE surveillance;

CREATE TABLE criminals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    image_path VARCHAR(255)
);

CREATE TABLE missing_persons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    image_path VARCHAR(255)
);

CREATE TABLE vip_access (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    image_path VARCHAR(255)
);

-- Example Data
INSERT INTO criminals (name, image_path) VALUES ('John Doe', 'images/criminals/john.jpg');
INSERT INTO missing_persons (name, image_path) VALUES ('Jane Smith', 'images/missing/jane.jpg');
INSERT INTO vip_access (name, image_path) VALUES ('VIP Person', 'images/vip/vip1.jpg');
