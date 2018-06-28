DROP TABLE IF EXISTS `ganji`;

CREATE TABLE `ganji` (
id int(6) unsigned not null auto_increment,
title varchar(255) null,
salary varchar(255) null,
company varchar(255) null,
contacts varchar(255) null,
phone varchar(255) null,
address varchar(255) null,
primary key (`id`),
unique key `phone` (`phone`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;