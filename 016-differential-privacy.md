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
GROUP BY fruit;
```

Suppose that instead of getting the regular count, we want the differentially private count with the privacy parameter ε=ln(3). The final product of the query rewrite would be

```sql
SELECT result.fruit, result.number_eaten
FROM (
  SELECT per_person.fruit,
    ANON_SUM(per_person.fruit_count, LN(3)/2) as number_eaten,
    ANON_COUNT(uid, LN(3)/2) as number_eaters
    FROM(
      SELECT * , ROW_NUMBER() OVER (
        PARTITION BY uid
        ORDER BY random()
      ) as row_num
      FROM (
        SELECT fruit, uid, COUNT(fruit) as fruit_count
        FROM FruitEaten
        GROUP BY fruit, uid
      ) as per_person_raw
    ) as per_person
  WHERE per_person.row_num <= 5
  GROUP BY per_person.fruit
) as result
WHERE result.number_eaters > 50;
```