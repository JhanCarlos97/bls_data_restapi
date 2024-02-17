-- Create necessary tables
CREATE SCHEMA IF NOT EXISTS public;

SET SEARCH_PATH = public;

DROP TABLE IF EXISTS all_ces;
DROP TABLE IF EXISTS ce_government;
DROP TABLE IF EXISTS ce_supersector;

-- Table to save all the CES data

create table
  public.all_ces (
    series_id text not null,
    year integer not null,
    period  text not null,
    value	numeric not null,
    footnote_codes text null
  ) tablespace pg_default;

CREATE INDEX index_on_series_id_all_ces ON public.all_ces USING btree (series_id);

-- Table to save the government data

create table
  public.ce_government (
    series_id text not null,
    year integer not null,
    period  text not null,
    value	numeric not null,
    footnote_codes text null
  ) tablespace pg_default;

CREATE INDEX index_on_series_id_ce_government ON public.ce_government USING btree (series_id);

-- Table to save the supersector info

create table
  public.ce_supersector (
    supersector_code text not null,
    supersector_name text not null
  ) tablespace pg_default;

CREATE SCHEMA IF NOT EXISTS api_call;

SET SEARCH_PATH = api_call;

-- View to allow a women-in-goverment-v1 endpoint (historical data from all the ces)

create view
  api_call.women_in_goverment_v1 as (
    select
    CONCAT(TRIM(TO_CHAR(TO_DATE(substr(period, 2), 'MM'), 'Month')),' ', year) as date,
    value as "valueInThousands"
    from public.all_ces
    where series_id = 'CES9000000010'
    and period != 'M13'
    order by year asc, period asc
  );

-- View to allow a women-in-goverment-v2 endpoint (historical data directly from government file)

create view
  api_call.women_in_goverment_v2 as (
    select
    CONCAT(TRIM(TO_CHAR(TO_DATE(substr(period, 2), 'MM'), 'Month')),' ', year) as date,
    value as "valueInThousands"
    from public.ce_government
    where series_id = 'CES9000000010'
    and period != 'M13'
    order by year asc, period asc
  );

-- View to allow a ratio-production-supervisory endpoint (historical ratio of supervisory/production or non supervisory employees by supersector)

create view
  api_call.ratio_production_supervisory as (
    with all_employees_data as (
      select
      substr(series_id, 4, 2) as category,
      CONCAT(TRIM(TO_CHAR(TO_DATE(substr(period, 2), 'MM'), 'Month')),' ', year) as date,
      sum(value) as all_employees
      from public.all_ces
      where RIGHT(series_id,2) = '01'
      and period != 'M13'
      group by category, date
      order by category, date
    ),
    production_employees_data as (
      select
      substr(series_id, 4, 2) as category,
      CONCAT(TRIM(TO_CHAR(TO_DATE(substr(period, 2), 'MM'), 'Month')),' ', year) as date,
      sum(value) as production_employees
      from public.all_ces
      where RIGHT(series_id,2) = '06'
      and period != 'M13'
      group by category, date
      order by category, date
    ),
    ratio_calculation_and_name as (
      select 
      ss.supersector_name as "sectorName",
      a.date,
      round(b.production_employees / (a.all_employees - b.production_employees)) as rate
      from all_employees_data a
      left join production_employees_data b
      on a.category = b.category and a.date = b.date
      left join public.ce_supersector ss on a.category = ss.supersector_code
    )
    select
    *
    from
    ratio_calculation_and_name
    where rate is not null
    order by "sectorName", date
  );

-- Grant permissions to role

create role web_anon nologin;

grant usage on schema api_call to web_anon;
grant select on api_call.women_in_goverment_v1 to web_anon;
grant select on api_call.women_in_goverment_v2 to web_anon;
grant select on api_call.ratio_production_supervisory to web_anon;

create role authenticator noinherit login password 'mysecretpassword';
grant web_anon to authenticator;