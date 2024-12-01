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
insert into room_list values(1, "lobby", "default_avatar.png", 0, now());

DROP TABLE IF EXISTS `user_room_map`;
CREATE TABLE `user_room_map` (
    `user_id` int(11) NOT NULL,
    `room_id` int(11) NOT NULL,
    `authority` int(11) DEFAULT '0',
    `mute` int(11) DEFAULT '0',
    `last_confirm_chat_id` int(11) DEFAULT NULL,
    `create_time` datetime DEFAULT NOW(),
    FOREIGN KEY(`user_id`) REFERENCES user_list(`id`),
    FOREIGN KEY(`room_id`) REFERENCES room_list(`id`),
    FOREIGN KEY(`last_confirm_chat_id`) REFERENCES chat_list(`id`),
    PRIMARY KEY(`user_id`, `room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `chat_list`;
CREATE TABLE `chat_list` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `room_id` int(11) NOT NULL,
    `content` varchar(500) NOT NULL,
    `create_time` datetime DEFAULT NOW(),
    FOREIGN KEY(`user_id`) REFERENCES user_list(`id`),
    FOREIGN KEY(`room_id`) REFERENCES room_list(`id`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SELECT 
    urm.room_id,
    r.name AS room_name,
    COUNT(c.id) AS unread_messages,
    lc.latest_chat_id,
    lc.latest_chat_content
FROM user_room_map AS urm
JOIN room_list AS r ON urm.room_id = r.id
LEFT JOIN chat_list AS c
    ON urm.room_id = c.room_id 
        AND c.id > urm.last_confirm_chat_id
LEFT JOIN
    (
        SELECT 
            c.room_id,
            c.id AS latest_chat_id,
            c.content AS latest_chat_content
        FROM chat_list AS c
        JOIN (
            SELECT room_id, MAX(id) AS latest_chat_id FROM chat_list GROUP BY room_id
        ) AS max_chat
        ON c.room_id = max_chat.room_id 
            AND c.id = max_chat.latest_chat_id
    ) AS lc ON urm.room_id = lc.room_id
WHERE urm.user_id = 3
GROUP BY urm.room_id, r.name, lc.latest_chat_id, lc.latest_chat_content;


SELECT 
    urm.room_id,
    r.name AS room_name
FROM user_room_map AS urm
JOIN room_list AS r ON urm.room_id = r.id
WHERE urm.user_id = 1
