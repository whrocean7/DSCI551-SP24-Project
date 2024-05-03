-- create database
create database ratemybeer1;
create database ratemybeer2;
create database ratemybeer1_rep;
create database ratemybeer2_rep;

-- create beer table
CREATE TABLE beer (
    beer_id INT PRIMARY KEY,
    beer_name VARCHAR(255) NOT NULL,
    beer_type VARCHAR(100),
    beer_price DECIMAL(10, 2) NOT NULL,
    create_time TIMESTAMP,
    update_time TIMESTAMP
);

-- create Review table
CREATE TABLE Review (
    review_id VARCHAR(36) PRIMARY KEY,
    beer_id INT,
    review_text TEXT,
    rating INT,
    create_time TIMESTAMP,
    update_time TIMESTAMP,
    FOREIGN KEY (beer_id) REFERENCES beer(beer_id) on DELETE CASCADE
);

-- add test data
-- add beer for ratemybeer1 and ratemybeer2
INSERT INTO beer (beer_id, beer_name, beer_type, beer_price, create_time, update_time) VALUES
(1, 'Stella Artois', 'Lager', 5.99, NOW(), NOW()),
(2, 'Guinness Draught', 'Stout', 6.49, NOW(), NOW()),
(3, 'Blue Moon Belgian White', 'Wheat Beer', 4.99, NOW(), NOW()),
(4, 'Sierra Nevada Pale Ale', 'Pale Ale', 7.29, NOW(), NOW()),
(5, 'Heineken', 'Lager', 5.79, NOW(), NOW());

-- add review for ratemybeer1
INSERT INTO Review (review_id, beer_id, review_text, rating, create_time, update_time) VALUES
('024cdc7b-8226-4961-aee4-154a38eee3f0', 5, 'it''s nice', 5, NOW(), NOW()),
('056c15dc-a025-452e-a466-d8243c90a879', 1, 'greater than expected', 5, NOW(), NOW()),
('0a79686e-2b4e-4986-84ec-69b1e2198853', 1, 'I think something is wrong', 0, NOW(), NOW()),
('1a934d58-cd79-49c5-afbf-7fe75418ab04', 5, 'it''s fine', 4, NOW(), NOW()),
('1f47d958-adbc-47f5-a4ca-7188af736ab5', 1, 'amazing', 5, NOW(), NOW());

-- add review for ratemybeer2
INSERT INTO Review (review_id, beer_id, review_text, rating, create_time, update_time) VALUES
('02f781d7-1d90-4f66-a748-ca3cf1ba312d', 1, 'tastes bad', 0, NOW(), NOW()),
('055ce054-50e5-4992-b9e9-a012782f2d35', 1, 'goooood~', 5, NOW(), NOW()),
('0f5bead8-1969-4b67-87ff-c8305e4ee04f', 1, 'can not be better', 5, NOW(), NOW()),
('15a78fc2-1869-41c8-9897-1cfe00562937', 2, 'okay', 3, NOW(), NOW()),
('1bb6e9c6-12d7-456b-a40e-ca8f6af568ad', 1, 'perfect', 5, NOW(), NOW());

-- create replica
create database ratemybeer2_rep;
CREATE TABLE ratemybeer2_rep.beer LIKE ratemybeer2.beer;
INSERT INTO ratemybeer2_rep.beer SELECT * FROM ratemybeer2.beer;
CREATE TABLE ratemybeer2_rep.review LIKE ratemybeer2.review;
INSERT INTO ratemybeer2_rep.review SELECT * FROM ratemybeer2.review;

-- Copy table structure and data into the new database
drop database ratemybeer2_rep;

-- restore replica2
create database ratemybeer2_rep;
CREATE TABLE ratemybeer2_rep.beer LIKE ratemybeer2.beer;
INSERT INTO ratemybeer2_rep.beer SELECT * FROM ratemybeer2.beer;
CREATE TABLE ratemybeer2_rep.review LIKE ratemybeer2.review;
INSERT INTO ratemybeer2_rep.review SELECT * FROM ratemybeer2.review;

-- restore replica1
create database ratemybeer1_rep;
CREATE TABLE ratemybeer1_rep.beer LIKE ratemybeer1.beer;
INSERT INTO ratemybeer1_rep.beer SELECT * FROM ratemybeer1.beer;
CREATE TABLE ratemybeer1_rep.review LIKE ratemybeer1.review;
INSERT INTO ratemybeer1_rep.review SELECT * FROM ratemybeer1.review;

