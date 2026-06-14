-- crear_tablas.hql
-- DDL de las 5 tablas obligatorias TPC-DS.
-- Ejecutar: hive -f hive/crear_tablas.hql

CREATE DATABASE IF NOT EXISTS retail;
USE retail;

-- ============================================================
-- customer
-- ============================================================
CREATE EXTERNAL TABLE IF NOT EXISTS customer (
    c_customer_sk             BIGINT,
    c_customer_id             STRING,
    c_current_cdemo_sk        BIGINT,
    c_current_hdemo_sk        BIGINT,
    c_current_addr_sk         BIGINT,
    c_first_shipto_date_sk    BIGINT,
    c_first_sales_date_sk     BIGINT,
    c_salutation              STRING,
    c_first_name              STRING,
    c_last_name               STRING,
    c_preferred_cust_flag     STRING,
    c_birth_day               INT,
    c_birth_month             INT,
    c_birth_year              INT,
    c_birth_country           STRING,
    c_login                   STRING,
    c_email_address           STRING,
    c_last_review_date_sk     BIGINT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE
LOCATION '/user/hadoop/tpcds/customer/';

-- ============================================================
-- item
-- ============================================================
CREATE EXTERNAL TABLE IF NOT EXISTS item (
    i_item_sk                 BIGINT,
    i_item_id                 STRING,
    i_rec_start_date          STRING,
    i_rec_end_date            STRING,
    i_item_desc               STRING,
    i_current_price           DOUBLE,
    i_wholesale_cost          DOUBLE,
    i_brand_id                INT,
    i_brand                   STRING,
    i_class_id                INT,
    i_class                   STRING,
    i_category_id             INT,
    i_category                STRING,
    i_manufact_id             INT,
    i_manufact                STRING,
    i_size                    STRING,
    i_formulation             STRING,
    i_color                   STRING,
    i_units                   STRING,
    i_container               STRING,
    i_manager_id              INT,
    i_product_name            STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE
LOCATION '/user/hadoop/tpcds/item/';

-- ============================================================
-- store
-- ============================================================
CREATE EXTERNAL TABLE IF NOT EXISTS store (
    s_store_sk                BIGINT,
    s_store_id                STRING,
    s_rec_start_date          STRING,
    s_rec_end_date            STRING,
    s_closed_date_sk          BIGINT,
    s_store_name              STRING,
    s_number_employees        INT,
    s_floor_space             INT,
    s_hours                   STRING,
    s_manager                 STRING,
    s_market_id               INT,
    s_geography_class         STRING,
    s_market_desc             STRING,
    s_market_manager          STRING,
    s_division_id             INT,
    s_division_name           STRING,
    s_company_id              INT,
    s_company_name            STRING,
    s_street_number           STRING,
    s_street_name             STRING,
    s_street_type             STRING,
    s_suite_number            STRING,
    s_city                    STRING,
    s_county                  STRING,
    s_state                   STRING,
    s_zip                     STRING,
    s_country                 STRING,
    s_gmt_offset              DOUBLE,
    s_tax_precentage          DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE
LOCATION '/user/hadoop/tpcds/store/';

-- ============================================================
-- date_dim
-- ============================================================
CREATE EXTERNAL TABLE IF NOT EXISTS date_dim (
    d_date_sk                 BIGINT,
    d_date_id                 STRING,
    d_date                    STRING,
    d_month_seq               INT,
    d_week_seq                INT,
    d_quarter_seq             INT,
    d_year                    INT,
    d_dow                     INT,
    d_moy                     INT,
    d_dom                     INT,
    d_qoy                     INT,
    d_fy_year                 INT,
    d_fy_quarter_seq          INT,
    d_fy_week_seq             INT,
    d_day_name                STRING,
    d_quarter_name            STRING,
    d_holiday                 STRING,
    d_weekend                 STRING,
    d_following_holiday       STRING,
    d_first_dom               INT,
    d_last_dom                INT,
    d_same_day_ly             INT,
    d_same_day_lq             INT,
    d_current_day             STRING,
    d_current_week            STRING,
    d_current_month           STRING,
    d_current_quarter         STRING,
    d_current_year            STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE
LOCATION '/user/hadoop/tpcds/date_dim/';

-- ============================================================
-- store_sales
-- ============================================================
CREATE EXTERNAL TABLE IF NOT EXISTS store_sales (
    ss_sold_date_sk           BIGINT,
    ss_sold_time_sk           BIGINT,
    ss_item_sk                BIGINT,
    ss_customer_sk            BIGINT,
    ss_cdemo_sk               BIGINT,
    ss_hdemo_sk               BIGINT,
    ss_addr_sk                BIGINT,
    ss_store_sk               BIGINT,
    ss_promo_sk               BIGINT,
    ss_ticket_number          BIGINT,
    ss_quantity               INT,
    ss_wholesale_cost         DOUBLE,
    ss_list_price             DOUBLE,
    ss_sales_price            DOUBLE,
    ss_ext_discount_amt       DOUBLE,
    ss_ext_sales_price        DOUBLE,
    ss_ext_wholesale_cost     DOUBLE,
    ss_ext_list_price         DOUBLE,
    ss_ext_tax                DOUBLE,
    ss_coupon_amt             DOUBLE,
    ss_net_paid               DOUBLE,
    ss_net_paid_inc_tax       DOUBLE,
    ss_net_profit             DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE
LOCATION '/user/hadoop/tpcds/store_sales/';

SHOW TABLES;
