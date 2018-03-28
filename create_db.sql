CREATE TABLE IF NOT EXISTS tb_event(
    event_id       SERIAL PRIMARY KEY,
    name           VARCHAR(128) UNIQUE NOT NULL,
    event_key      VARCHAR(128) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_user(
    user_id    SERIAL PRIMARY KEY,
    name       VARCHAR(128) UNIQUE NOT NULL,
    photo      VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_employer_info(
    employer_info_id  SERIAL PRIMARY KEY,
    user_id           INTEGER NOT NULL REFERENCES tb_user(user_id) NOT NULL,
    event_id          INTEGER NOT NULL REFERENCES tb_event(event_id) NOT NULL
);

