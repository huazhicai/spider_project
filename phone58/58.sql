DROP TABLE IF EXISTS `enterprise_58`;

CREATE TABLE `enterprise_58` (
id int(6) unsigned not null auto_increment,
title varchar(255) null,
salary varchar(255) null,
company varchar(255) null,
company_type varchar(255) null,
company_scale varchar(255) null,
industry varchar(255) null,
contacts varchar(255) null,
phone varchar(255) null,
website varchar(255) null,
address varchar(255) null,
primary key (`id`),
unique key `url` (`website`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;