CREATE TABLE IF NOT EXISTS ta_exchanges (
    code_exchange TEXT NOT NULL,
    name_exchange TEXT NOT NULL,
    operating_mic TEXT,
    country TEXT NOT NULL,
    currency TEXT NOT NULL,
    country_iso_2 TEXT,
    country_iso_3 TEXT,
    PRIMARY KEY (code_exchange)
); 

CREATE TABLE IF NOT EXISTS ta_ticker_metadata (
    symbol TEXT NOT NULL PRIMARY KEY,
    name_ticker TEXT,
    country TEXT NOT NULL,
    currency TEXT NOT NULL,
    sec_type TEXT,
    isin TEXT
); 

CREATE TABLE IF NOT EXISTS ta_ohlcv (
    dt TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    code_exchange TEXT NOT NULL,
    open DOUBLE PRECISION, 
    high DOUBLE PRECISION,
    close DOUBLE PRECISION,
    adjusted_close DOUBLE PRECISION,
    volume BIGINT,
    PRIMARY KEY (symbol, dt),
    CONSTRAINT fk_code_exchange FOREIGN KEY (code_exchange) REFERENCES ta_exchanges (code_exchange),
    CONSTRAINT fk_symbol FOREIGN KEY (symbol) REFERENCES ta_ticker_metadata (symbol)
); 

CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

CREATE INDEX idx_symbol ON ta_ohlcv (symbol); 
CREATE INDEX idx_time ON ta_ohlcv (dt DESC); 

SELECT create_hypertable('ta_ohlcv', 'dt'); 

