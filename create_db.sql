CREATE TABLE IF NOT EXISTS tb_user(
    user_id       SERIAL PRIMARY KEY,
    name          VARCHAR(128) UNIQUE NOT NULL,
);

