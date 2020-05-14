https://github.com/google/differential-privacy/tree/master/differential_privacy/postgres


```sql
CREATE TABLE FruitEaten (
  uid integer,
  fruit character varying(20)
);
COPY fruiteaten(uid, fruit) FROM 'fruiteaten.csv' DELIMITER ',' CSV HEADER;

```