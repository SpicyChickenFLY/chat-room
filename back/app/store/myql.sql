DROP TABLE IF EXISTS `user_list`;
CREATE TABLE `user_list` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `nickname` varchar(20) NOT NULL,
    `token` varchar(200) NOT NULL,
    `status` smallint(4) DEFAULT '0',
    `avatar` varchar(50) DEFAULT NULL,
    `create_time` datetime DEFAULT NOW(),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `room_list`;
CREATE TABLE `room_list` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(20) NOT NULL,
    `avatar` varchar(50) DEFAULT NULL,
    `single` smallint(4) DEFAULT '0',
    `create_time` datetime DEFAULT NOW(),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert into room_list values(0, "lobby", "default_avatar.png", 0, now());

DROP TABLE IF EXISTS `user_room_map`;
CREATE TABLE `user_room_map` (
    `user_id` int(11) NOT NULL,
    `room_id` int(11) NOT NULL,
    `authority` int(11) DEFAULT '0',
    `mute` int(11) DEFAULT '0',
    `create_time` datetime DEFAULT NOW(),
    PRIMARY KEY(`user_id`, `room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

