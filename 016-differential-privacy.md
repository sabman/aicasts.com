https://github.com/google/differential-privacy/tree/master/differential_privacy/postgres


```sql
CREATE TABLE FruitEaten (
  uid integer,
  fruit character varying(20)
);
COPY fruiteaten(uid, fruit) FROM 'fruiteaten.csv' DELIMITER ',' CSV HEADER;
```

In this table, each row represents one fruit eaten. So if person 1 eats two apples, then there will be two rows in the table with column values (1, apple). Consider a simple query counting how many of each fruit have been eaten.

```sql
SELECT fruit, COUNT(fruit)
FROM FruitEaten
```