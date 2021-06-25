create table api_credentials
(
    api_id     integer not null,
    api_hash   text    not null,
    account_id integer not null
        constraint api_credentials_account_id_fk
            references account
);

alter table api_credentials
    owner to postgres;

create unique index api_credentials_account_id_uindex
    on api_credentials (account_id);

create unique index api_credentials_api_id_uindex
    on api_credentials (api_id);

create unique index api_credentials_api_hash_uindex
    on api_credentials (api_hash);
