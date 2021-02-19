drop table if exists station_list;
create table station_list(
 code int not null primary key,
 id varchar(16) unique,
 name varchar(64) not null,
 original_name varchar(64) not null,
 name_kana varchar(64) not null,
 lat numeric(10,6) not null,
 lng numeric(10,6) not null,
 prefecture int not null,
 postal_code varchar(16),
 address varchar(128),
 closed boolean not null,
 open_date date default null,
 closed_date date default null,
 impl boolean not null,
 attr varchar(16)
);

create index on station_list (code);
create index on station_list (id);

drop table if exists line_list;
create table line_list(
 code int not null primary key,
 id varchar(16) unique,
 name varchar(64) not null,
 name_kana varchar(64) not null,
 name_formal varchar(64),
 station_size int not null,
 company_code int,
 color varchar(16),
 symbol varchar(16),
 closed boolean not null,
 closed_date date default null,
 impl boolean not null
);

create index on line_list (code);
create index on line_list (id);

drop table if exists data_info;
create table data_info(
  id serial primary key,
  data_version bigint not null,
  updated_at TIMESTAMP not null
);

create index on data_info (id);