# Stream Processing
Key Questions
- what is stream processing
- what is kafka
- message properties of stream processing
- configurations and parameters of stream processing
    - partitioning
    - replication
    - retention
    - time spanning
- kafka producers and kafka consumers
- how data is partitioned inside stream processing
- the role of schema in stream processing

## What is stream processing?
- what is data exchange
    - a sort of data exchange is a postal service
    - you write your message on a letter and the postal service takes it somewhere else
    - a concrete example could be something like the data exchanged between two computers over an API

### Producers and Consumers
- take a bulleting board as an example
- a producer is someone who posts a flyer
- a consumer is someone who comes by and gets information from the flyer posted by the consumer
- topics
    - let's say that consumers are interested in a couple of subjects
        - kafka
        - spark
    - a producer will release a data exchange with respect to kafka
    - consumers subscribed to kafka will receive this data exchange (more or less)
    - the key difference here (compared with batch) is that subscribers are receiving this data in more real time 
- defining real time
    - there are a few seconds of delay
    - batch can be every minute or every hour, but in stream processing this happens much faster

## What is Kafka?
- it's important to understand what a topic is
    - a continuous stream of events
        - an event could be something like a recorded temperature coming from an IoT thermometer with a timestamp
        - this event might be sent out every 30 seconds
        - across time, these events are single data points at certain timestamps
    - how do logs play into topics?
        - logs are how we store events in a topic
        - when anyone talks about logs in kafka, they are talking about how data in a topic is stored
    - how are events structured inside of kafka?
        - each event contains a message
            - a message contains a key, value and a timestamp
            - keys get used for partitioning
            - the value contains the data exchange
- what's so special about kafka?
    - kafka is robust and reliable
    - even if a node goes down, you'll still receive your data
    - this is achieved via replication across different fields
        - i'm sure this will be explained in more detail later but it is internal and thus not supremely important
    - kafka has a lot of flexibility
        - big or small values
        - a variety of connection options
    - quite scalable
        - if things grow from 10 events/ps to 1000 e/ps it will handle this just fine

### Data exchange in kafka
- when a producer releases data in a topic, consumers will be able to read it, but the data will not be lost (consumed)
    - there is a retention period for data in a topic
    - this is done with robustness, scalability and flexibility in mind

### Kafka and Architecture relationship
- we are moving away (generally) from monolithic architecture
    - one large codebase that includes everthing
- now you tend to have microservices that are intended for specialized parts of the architecture
    - this works fine while APIs and microservices are not very big/complex
    - with growing data you need a consistent message bus
- how it works within an architecture
    - a microservice will write to a topic in terms of events
    - subscribed microservices can generally read published events from said topic
- kafka also allows us to implement CDC (change data capture)
    - a database can be the producer and write metadata changes to a topic
    - microservices can then read from the CDC topic
    - this is done via Kafka connect

## Confluent Cloud
What we did in this section:
- created a kafka cluster
- created a topic
    - 2 partitions
    - 1 day retention time with infinite storage (?)
- started datagen dummy connector with JSON orders
    - this will be turned off after a few hundred messages to avoid running out of credits


## Producers and Consumers
TODO: add link to new Java project
This section used Java. See the repo for this section on [GitHub](#)