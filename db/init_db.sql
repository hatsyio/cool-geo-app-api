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

CREATE TABLE users (
    username VARCHAR,
    full_name VARCHAR,
    email VARCHAR,
    hashed_password VARCHAR,
    disabled BOOL
);

COPY paystats(amount,p_month,p_age,p_gender,postal_code_id,id)
FROM '/tmp/data/paystats.csv'
    (FORMAT CSV, DELIMITER ',', HEADER, ENCODING 'UTF8');

COPY postal_codes(the_geom,code,id)
FROM '/tmp/data/postal_codes.csv'
    (FORMAT CSV, DELIMITER ',', HEADER, ENCODING 'UTF8');

--pg_dump -Fc --no-acl --no-owner -h localhost -U postgres cool-geo-app > mydb.dump
--pg_restore --verbose --clean --no-acl --no-owner -h ec2-34-242-8-97.eu-west-1.compute.amazonaws.com -U xcauhyiguzxrux -d d6ka3ub4arjj66 mydb.dump
