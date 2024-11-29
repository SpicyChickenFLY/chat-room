概念的转变：
socketio中的join_room步骤，不应该由用户在登陆后手动的去选择，
而是应该在用户登陆并连接后，由服务端

user(id, name)
room(id, name)
user_room_map(user_id, room_id, last_confirm_chat_id)
chat(id, user_id, room_id, chat_content)
如何用一句SQL查看指定ID的用户的每个房间的未读聊天消息数据与最新一条消息的内容

```sql
SELECT
    urm.room_id,
    COUNT(c.id) AS unread_messages,
    latest_chat.id AS latest_chat_id,
    latest_chat.chat_content AS latest_chat_content
FROM user_room_map AS urm
    LEFT JOIN chat AS c
        ON urm.room_id = c.room_id
            AND c.id > urm.last_confirm_chat_id
    LEFT JOIN
        (
            SELECT
                room_id,
                id,
                chat_content
            FROM chat
            WHERE
                (room_id, id) IN (
                    SELECT room_id, MAX(id) AS max_id
                    FROM chat
                    GROUP BY room_id
                )
        ) AS latest_chat
        ON urm.room_id = latest_chat.room_id
WHERE urm.user_id = :user_id
GROUP BY urm.room_id, latest_chat.id, latest_chat.chat_content;
```

```sql
SELECT
    user_room_map.room_id AS user_room_map_room_id,
    room_list.name AS room_name,
    count(chat_list.id) AS unread_messages,
    anon_1.latest_chat_id AS anon_1_latest_chat_id,
    anon_1.latest_chat_content AS anon_1_latest_chat_content
FROM user_room_map
    LEFT OUTER JOIN chat_list
        ON user_room_map.room_id = chat_list.room_id
            AND chat_list.id > user_room_map.last_confirm_chat_id
    LEFT OUTER JOIN
        (
            SELECT
                chat_list.room_id AS room_id,
                chat_list.id AS latest_chat_id,
                chat_list.content AS latest_chat_content
            FROM chat_list
                INNER JOIN (
                    SELECT chat_list.room_id AS room_id, max(chat_list.id) AS max_id
                    FROM chat_list
                    GROUP BY chat_list.room_id
                ) AS anon_2
                ON chat_list.room_id = anon_2.room_id
                    AND chat_list.id = anon_2.max_id
        ) AS anon_1
        ON user_room_map.room_id = anon_1.room_id,
    room_list
WHERE user_room_map.user_id = 1
GROUP BY user_room_map.room_id, anon_1.latest_chat_id, anon_1.latest_chat_content
```
