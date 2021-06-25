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
