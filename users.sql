-- $ sqlite3 users.db < users.sql

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

INSERT INTO users(username, email, password) VALUES('planetar','cvrcek@gmail.com','PwA7HrxK6D3X5=#!');
INSERT INTO users(username, email, password) VALUES('theprestige','chrisk@icloud.com','F9x&3jG?y+n^u-XN');
INSERT INTO users(username, email, password) VALUES('spiralshape','fmerges@att.net','sp9XZAFhyb%82!hB');
INSERT INTO users(username, email, password) VALUES('batmanbegins','bhima@mac.com','ibeatthejoker');
INSERT INTO users(username, email, password) VALUES('aromatic','stern@mac.com','2AXz-h%GFm9b&?tU');

INSERT INTO followers(username, usernameToFollow) VALUES('planetar', 'theprestige');
INSERT INTO followers(username, usernameToFollow) VALUES('planetar', 'spiralshape');
INSERT INTO followers(username, usernameToFollow) VALUES('theprestige', 'batmanbegins');
INSERT INTO followers(username, usernameToFollow) VALUES('aromatic', 'spiralshape');
INSERT INTO followers(username, usernameToFollow) VALUES('aromatic', 'planetar');
INSERT INTO followers(username, usernameToFollow) VALUES('batmanbegins', 'theprestige');
INSERT INTO followers(username, usernameToFollow) VALUES('spiralshape', 'aromatic');

COMMIT;
