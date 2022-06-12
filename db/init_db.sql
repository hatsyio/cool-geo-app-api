CREATE TABLE paystats
(
    id             INT,
    postal_code_id INT,
    p_gender       VARCHAR(1),
    p_age          VARCHAR(10),
    p_month        DATE,
    amount        FLOAT
);

CREATE TABLE postal_codes (
    id INT,
    code VARCHAR,
    the_geom GEOMETRY
);

COPY paystats(amount,p_month,p_age,p_gender,postal_code_id,id)
FROM '/tmp/data/paystats.csv'
    (FORMAT CSV, DELIMITER ',', HEADER, ENCODING 'UTF8');

COPY postal_codes(the_geom,code,id)
FROM '/tmp/data/postal_codes.csv'
    (FORMAT CSV, DELIMITER ',', HEADER, ENCODING 'UTF8');
