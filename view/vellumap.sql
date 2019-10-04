PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Type(
Name char(10) unique not null,
Shape char(10) not null,
Color char(20) not null, 
Width real default 0.0,
Height real default 0.0);
INSERT INTO Type VALUES('typetest','ell','green',100.0,100.0);

CREATE TABLE ObjectGraphic(
id integer primary key autoincrement,
Name varchar(30) not null,
X real default 0.0,
Y real default 0.0,
Type varchar(10) not null,
size real default 1.0);

CREATE TABLE ObjectDescription(
id integer not null,
Description varchar(100) default 'None' );
COMMIT;
