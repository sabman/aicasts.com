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

As we can see, there are four SELECTS in the query. We will explain them from inner-most to outer-most. The following steps were taken to rewrite the query:

* Construct the 1st and inner-most `SELECT`, aliased as `per_person_raw`.

```sql
SELECT fruit, uid, COUNT(fruit) as fruit_count
FROM FruitEaten
GROUP BY fruit, uid;
```

For each person, count how many of each fruit that person ate.

Construct the 2nd `SELECT`, aliased as `per_person`.

```sql
SELECT *, ROW_NUMBER() OVER (
  PARTITION BY uid
  ORDER BY random()
) as row_num
FROM per_person_raw;
```

For each person, `per_person_raw` contains rows corresponding to the fruits they have eaten. We shuffle these rows and assign them a row number. This will allow us to effectively [reservoir sample](https://en.wikipedia.org/wiki/Reservoir_sampling) rows for each user by filtering by row number in the next step. This is similar to C_u thresholding in Wilson et al.


Construct the 3rd `SELECT`, aliased as result.

```sql
SELECT per_person.fruit,
       ANON_SUM(per_person.fruit_count, LN(3)/2) as number_eaten,
       ANON_COUNT(uid, LN(3)/2) as number_eaters
FROM per_person
WHERE per_person.row_num <= 5
GROUP BY per_person.fruit;
```

First, for each person, we ensure that the person only contributed to 5 fruit groups by filtering on the **randomized row number** generated in the previous step. Then, for each fruit, we sum the number of the fruit that each person ate. We also count the number of people who ate that fruit. This will allow us to ensure we only release the sums which enough people contributed to.

In order to anonymously grab the sum and count, we replace the aggregates `SUM` and `COUNT` with `ANON_SUM` and `ANON_COUNT`, respectively. Note that since we are performing two anonymous aggregations, we split our privacy parameter between them, using `ε=ln(3)` for both.

Construct the 4th and outer-most SELECT.

```sql
SELECT result.fruit, result.number_eaten
FROM result
WHERE result.number_eaters > 50;
```

For any fruit where the number of eaters was less than 50, discard the output result. This is similar to `τ-thresholding` in Wilson et al. In addition, we drop the `number_eaters` count, so that it does not display in the output. Dropping the count of unique users is not necessary for differential privacy.

### Multiple Aggregations

In our simple count example, we used a query containing a single anonymous function. For a query with N anonymous function calls, and with a desired total privacy parameter of `ε`, we need to use `ε/(N+1)` as the privacy parameter for each aggregation. This is for the N requested calls plus the additional anonymous unique-user count. For instance, consider the following dummy query:

```sql
SELECT COUNT(col1), SUM(col2)
FROM Table;
```

Suppose we want to use the privacy parameter `ε=M`. In the rewritten query, we have to make the following replacements

| Original    | Replacement           |
| ----------- | --------------------- |
| COUNT(col1) | ANON_COUNT(col1, M/3) |
| SUM(col2)   | ANON_SUM(col2, M/3)   |

This is because we have **two** (`COUNT`, `SUM`) requested anonymous functions, and an additional **anonymous unique user count** required when we perform the rewrite.
****
### Bounding User Contribution

Consider again our fruit-eating example. Suppose we want to *restrict the contribution of each person to the fruit-eaten counts* by `5`. So if a person has eaten more than `5` fruit, we want to count it as that they have eaten `5` fruit. To do this, add lower and upper bounds on the anonymous functions:

| Original                                    | Replacement                                           |
| ------------------------------------------- | ----------------------------------------------------- |
| `ANON_SUM(per_person.fruit_count, LN(3)/2)` | **`ANON_SUM**(per_person.fruit_count, 0, 5, LN(3)/2)` |

### Query With Joins

In this section we will add a `join` to our query. In addition to the `FruitEaten` table, consider the following table, which we will call `Shirts`.

| Column | Type        | Description                          |
| ------ | ----------- | ------------------------------------ |
| uid    | integer     | Uniquely identifies a person.        |
| color  | varchar(20) | The name of the person's shirt color |

Create the table and import the data provided by `shirts.csv`. Make sure to change the file path below to point to where you cloned the directory.

```sql
CREATE TABLE Shirts (
  uid integer,
  color character varying(20)
);
COPY shirts(uid, color) FROM 'shirts.csv' DELIMITER ',' CSV HEADER;
```

Let's say we want to find out, for each shirt color, how many fruit all the people wearing that shirt color ate, altogether.

```sql
SELECT color, COUNT(fruit)
FROM FruitEaten f INNER JOIN Shirts s ON (f.uid = s.uid)
GROUP BY color;
```


We rewrite the query into its differentially private version:

```sql
SELECT result.color, result.number_eaten
FROM (
  SELECT per_person.color,
    ANON_SUM(per_person.fruit_count, LN(3)/2) as number_eaten,
    ANON_COUNT(uid, LN(3)/2) as number_eaters
    FROM(
      SELECT * , ROW_NUMBER() OVER (
        PARTITION BY uid
        ORDER BY random()
      ) as row_num
      FROM (
        SELECT color, f.uid as uid, COUNT(fruit) as fruit_count
        FROM FruitEaten f INNER JOIN Shirts s ON (f.uid = s.uid)
        GROUP BY color, f.uid
      ) as per_person_raw
    ) as per_person
  WHERE per_person.row_num <= 5
  GROUP BY per_person.color
) as result
WHERE result.number_eaters > 50;
```

The restriction with this method of rewriting is that joins must not create any rows of **shared ownership**. In the example above, this is satisfied.
