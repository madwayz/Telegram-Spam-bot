create table account
(
    id                serial                not null
        constraint account_pk
            primary key,
    phone_number      text                  not null,
    username          text    default 'не установлено'::text,
    full_name         text    default 'не установлено'::text,
    type              integer,
    is_current        boolean default false not null,
    distribution_text text    default 'отсутствует'::text,
    session_path      text                  not null,
    chat_list_id      serial                not null,
    in_progress       boolean default false
);

alter table account
    owner to postgres;

create unique index account_id_uindex
    on account (id);

create unique index account_phone_number_uindex
    on account (phone_number);

create unique index account_chat_list_id_uindex
    on account (chat_list_id);
