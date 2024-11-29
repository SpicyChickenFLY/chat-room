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
        SELECT room_id, id, chat_content
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
