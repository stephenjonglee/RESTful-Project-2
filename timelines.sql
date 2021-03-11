-- $ sqlite3 timelines.db < timelines.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS timelines;
CREATE TABLE timelines(
    author VARCHAR,
    text VARCHAR,
    time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(author) REFERENCES user(username)
);
