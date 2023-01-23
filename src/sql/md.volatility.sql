create table md.volatility
(
    id          serial,
    underlying  varchar(20) not null,
    datadate    date        not null,
    implied_vol numeric,
    constraint volatility_pk primary key (underlying, datadate)
);

alter table md.volatility owner to postgres;

