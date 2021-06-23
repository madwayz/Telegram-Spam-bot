create table account
(
    id                serial                not null
        constraint account_pk
            primary key,
    phone_number      text                  not null,
    username          text,
    full_name         text,
    type              integer,
    is_current        boolean default false not null,
    distribution_text text    default 'отсутствует'::text,
    session_path      text                  not null,
    chat_list_id      serial                not null
);

alter table account
    owner to postgres;

create unique index account_id_uindex
    on account (id);

create unique index account_phone_number_uindex
    on account (phone_number);

create unique index account_username_uindex
    on account (username);

create unique index account_chat_list_id_uindex
    on account (chat_list_id);

create table api_credentials
(
    api_id     integer not null,
    api_hash   integer not null,
    account_id integer not null
        constraint api_credentials_account_id_fk
            references account
);

alter table api_credentials
    owner to postgres;

create unique index api_credentials_account_id_uindex
    on api_credentials (account_id);

create unique index api_credentials_api_hash_uindex
    on api_credentials (api_hash);

create unique index api_credentials_api_id_uindex
    on api_credentials (api_id);

create table chat
(
    id               serial not null
        constraint chat_pk
            primary key,
    name             text   not null,
    message_interval integer,
    message_quantity integer
);

alter table chat
    owner to postgres;

create unique index chat_id_uindex
    on chat (id);

create unique index chat_name_uindex
    on chat (name);

create table chat_list
(
    id      integer not null,
    chat_id integer not null
);

alter table chat_list
    owner to postgres;

