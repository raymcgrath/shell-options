CREATE OR REPLACE FUNCTION md.upsert_volatility(underlying_in varchar(20), datadate_in date,implied_vol_in numeric) RETURNS VOID AS $$
    DECLARE
    BEGIN
        INSERT INTO md.volatility (underlying, datadate, implied_vol) values (underlying_in, datadate_in, implied_vol_in)
        ON CONFLICT (underlying,datadate )
        DO UPDATE SET implied_vol = implied_vol_in;
    END;
    $$ LANGUAGE 'plpgsql';