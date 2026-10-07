-- create tables
CREATE TABLE IF NOT EXISTS users
(
    uuid uuid NOT NULL DEFAULT gen_random_uuid(),
    user_name character varying(128) COLLATE pg_catalog."default",
    pass_hash character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_uuid PRIMARY KEY (uuid),
    CONSTRAINT unique_name UNIQUE (user_name),
    CONSTRAINT uq_u_name UNIQUE (user_name)
);

CREATE TABLE IF NOT EXISTS song_rating
(
    id integer NOT NULL DEFAULT nextval('song_rating_id_seq'::regclass),
    song_mbid uuid NOT NULL,
    user_name character varying(128) COLLATE pg_catalog."default" NOT NULL,
    review text COLLATE pg_catalog."default",
    rating smallint NOT NULL,
    last_updated timestamp with time zone,
    CONSTRAINT song_rating_pkey PRIMARY KEY (song_mbid, user_name),
    CONSTRAINT user_name_fk FOREIGN KEY (user_name)
        REFERENCES users (user_name) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT rating_range CHECK (rating >= 1 AND rating <= 5)
)

CREATE TABLE IF NOT EXISTS sessions
(
    user_name character varying(128) COLLATE pg_catalog."default" NOT NULL,
    sid uuid NOT NULL DEFAULT gen_random_uuid(),
    expire_by date DEFAULT (CURRENT_DATE + 30),
    CONSTRAINT sessions_sid_key UNIQUE (sid),
    CONSTRAINT sessions_user_name_fkey FOREIGN KEY (user_name)
        REFERENCES users (user_name) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE sessions (
    user_name VARCHAR(128) NOT NULL REFERENCES users(user_name), 
    sid uuid UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    expire_by DATE DEFAULT CURRENT_DATE + 30
);

