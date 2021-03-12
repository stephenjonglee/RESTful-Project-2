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

INSERT INTO timelines(author, text, time) VALUES('planetar', 'Science is fun!', '20210305 04:17:03');
INSERT INTO timelines(author, text, time) VALUES('planetar', 'Is pluto a planet?', '20210212 01:12:01');
INSERT INTO timelines(author, text, time) VALUES('theprestige', 'I am the best. The very best. That no one ever was.', '20210124 04:54:34');
INSERT INTO timelines(author, text, time) VALUES('theprestige', 'I am a grandmaster in chess. Does anyone want to play with me?', '20210228 01:25:53');
INSERT INTO timelines(author, text, time) VALUES('spiralshape', 'Geometry is better than science. The circle is infinite and spirals are cool.', '20210309 11:14:10');
INSERT INTO timelines(author, text, time) VALUES('spiralshape', 'Stare into my spirals and be hypnotized.', '20210227 03:20:16');
INSERT INTO timelines(author, text, time) VALUES('spiralshape', 'I love ice cream swirls.', '20210105 06:15:25');
INSERT INTO timelines(author, text, time) VALUES('batmanbegins', 'I am the Dark Knight.', '20210126 01:02:38');
INSERT INTO timelines(author, text, time) VALUES('batmanbegins', 'I know karate', '20210309 07:03:35');
INSERT INTO timelines(author, text, time) VALUES('batmanbegins', 'Be afraid. Be very afraid.', '20210226 10:44:39');
INSERT INTO timelines(author, text, time) VALUES('batmanbegins', 'Bad boys, bad boys. What you gonna do? What you gonna do when I come for you?', '20210206 08:24:54');
INSERT INTO timelines(author, text, time) VALUES('aromatic', 'Feeling stressed? Try some aroma therapy.', '20210107 10:34:04');
INSERT INTO timelines(author, text, time) VALUES('aromatic', 'Selling oil diffusers at a cheap price!', '20210218 01:36:34');
