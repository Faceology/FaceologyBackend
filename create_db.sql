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
    event_id          INTEGER NOT NULL REFERENCES tb_event(event_id) NOT NULL,
    bio               VARCHAR,
    headline          VARCHAR,
    profile_link      VARCHAR NOT NULL,
    email             VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS tb_employer_job(
  employer_job_id   SERIAL PRIMARY KEY,
  user_id           INTEGER NOT NULL REFERENCES tb_user(user_id) NOT NULL,
  event_id          INTEGER NOT NULL REFERENCES tb_event(event_id) NOT NULL,
  location          VARCHAR(255) NOT NULL,
  company_name      VARCHAR(255) NOT NULL,
  title             VARCHAR(255) NOT NULL,
  date_start        VARCHAR(255) NOT NULL,
  date_end          VARCHAR(255),
  is_current        BOOLEAN NOT NULL
);
