CREATE TABLE IF NOT EXISTS giveaways_view(
    guild_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL UNIQUE,
    view_id INTEGER NOT NULL PRIMARY KEY
)
