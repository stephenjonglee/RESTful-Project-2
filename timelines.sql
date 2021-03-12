-- $ sqlite3 timelines.db < timelines.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS users;
CREATE TABLE users(
    username VARCHAR primary key,
    email VARCHAR,
    password VARCHAR,
    UNIQUE(email)
);

DROP TABLE IF EXISTS followers;
CREATE TABLE followers(
    username VARCHAR,
    usernameToFollow VARCHAR,
    FOREIGN KEY(username) REFERENCES users(username),
    FOREIGN KEY(usernameToFollow) REFERENCES users(username),
    UNIQUE(username, usernameToFollow)
);

DROP TABLE IF EXISTS timelines;
CREATE TABLE timelines(
    author VARCHAR,
    text VARCHAR,
    time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(author) REFERENCES users(username),
    UNIQUE(author, text)
);
