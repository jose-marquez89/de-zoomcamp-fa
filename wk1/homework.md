## Week 1 Homework

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command

Which tag has the following text? - *Write the image ID to the file* 

- `--imageid string`
- `--iidfile string` *this one*
- `--idimage string`
- `--idfile string`


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

- 1
- 6
- 3
- 7

*Not gonna do this but the answer depends on how many packages/modules you've chosen to install in the Dockerfile*

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from January 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

*DONE!!!*


## Question 3. Count records 

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 20689
- 20530
- 17630
- 21090

*This is hard to tell based on the csv given in this homework, but I'm assuming this is just for the green taxi, going to put my sql code and result below* 

```SQL
/*
Assuming unique records are the basis of these tables,
both queries yield 1764
*/

SELECT COUNT(*) FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) = '2023-01-15'
	AND DATE(lpep_dropoff_datetime) = '2023-01-15';
	
SELECT COUNT(*) FROM green_taxi_trips
WHERE CAST(lpep_pickup_datetime AS DATE) = '2023-01-15'
	AND CAST(lpep_dropoff_datetime AS DATE) = '2023-01-15';
```

## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

- 2019-01-18
- 2019-01-28
- 2019-01-15
- 2019-01-10

```SQL
-- yields 2023-01-11

SELECT DATE(lpep_pickup_datetime) AS longest_dist_day
FROM green_taxi_trips
WHERE trip_distance >= (SELECT MAX(trip_distance) FROM green_taxi_trips);
```

## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?
 
- 2: 1282 ; 3: 266
- 2: 1532 ; 3: 126
- 2: 1282 ; 3: 254
- 2: 1282 ; 3: 274

```SQL
-- yields 129

SELECT COUNT(*)
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) = '2023-01-01'
	AND (passenger_count = 2 OR passenger_count = 3);
```


## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- South Ozone Park
- Long Island City/Queens Plaza

```SQL
-- yields "Greenpoint"
WITH adds_zones AS (
	SELECT 
		g.index AS trip_record,
		g.tip_amount,
		pz."Zone" AS pu_zone,
		dz."Zone" AS do_zone
	FROM green_taxi_trips g
	JOIN zones pz
		ON g."PULocationID" = pz."LocationID"
	JOIN zones dz
		ON g."DOLocationID" = dz."LocationID"
	ORDER BY g.tip_amount DESC
)

SELECT *
FROM adds_zones
WHERE pu_zone = 'Astoria'
LIMIT 1;
```


## Submitting the solutions

* Form for submitting: [form](https://forms.gle/EjphSkR1b3nsdojv7)
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 30 January (Monday), 22:00 CET


## Solution

See here: https://www.youtube.com/watch?v=KIh_9tZiroA