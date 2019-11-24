PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Type(
Name char(10) unique not null,
Shape char(10) not null,
Color char(20) not null, 
Width real default 0.0,
Height real default 0.0);

CREATE TABLE ObjectGraphic(
id integer unique not null,
Name varchar(30) not null,
X real default 0.0,
Y real default 0.0,
Type varchar(10) not null);

CREATE TABLE ObjectDescription(
id integer unique not null,
Description varchar(100) default 'None' );

CREATE TABLE Background(
Name varchar(10) not null,
X real default 0.0,
Y real default 0.0,
size_rate real default 1.0);

COMMIT;
