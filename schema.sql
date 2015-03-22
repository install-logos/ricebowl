PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE packages (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  program TEXT NOT NULL,
  url TEXT NOT NULL,
  images TEXT NOT NULL,
  description TEXT NOT NULL
);
INSERT INTO "packages" VALUES(1,'linux repo 1','i3','http://bwasti.com:9001/test.zip','["http://bwasti.com:9001/test.jpg"]','This is a sample of the description field.');
INSERT INTO "packages" VALUES(2,'linux repo 2','i3','http://bwasti.com:9001/test.zip','["http://bwasti.com:9001/test2.jpg"]','Does this description thing work?.');
INSERT INTO "packages" VALUES(3,'linux repo 3','i3','http://bwasti.com:9001/test.zip','["http://bwasti.com:9001/test3.png"]','test.');
INSERT INTO "packages" VALUES(4,'logos','i3','http://penisland.net','["http://bwasti.com:9001/test3.png"]','your server is working. Congrats...');
COMMIT;
