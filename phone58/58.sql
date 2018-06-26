DROP TABLE IF EXISTS `phones`;

CREATE TABLE `phone` (
id int(6) unsigned not null auto_increment,
title varchar(255) null,
salary varchar(128) null,
company varchar(128) null,
company_type varchar(128) null,
command_scale varchar(128) null,
industry varchar(128) null,
contacts varchar(64) null,
phone varchar(64) null,
website varchar(255) null,
address varchar(255) null,
primary key (`id`),
unique key `url` (`website`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;