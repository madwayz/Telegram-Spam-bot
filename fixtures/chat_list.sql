create table chat_list
(
    id      integer not null,
    chat_id integer not null
);

alter table chat_list
    owner to postgres;
