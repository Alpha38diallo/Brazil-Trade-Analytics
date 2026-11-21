CREATE TABLE trade_data (
    period INT,
    reporter_country VARCHAR(100),
    partner_country VARCHAR(100),
    commodity_code VARCHAR(20),
    flow_code VARCHAR(10),
    trade_value_usd FLOAT,
    net_weight FLOAT
);