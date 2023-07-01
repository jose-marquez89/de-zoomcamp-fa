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
This section used Java. See the repo for this section on [GitHub](https://github.com/jose-marquez89/kafka-dez-tutorial/tree/main)

## Kafka configurations
- what is a kafka cluster?
    - just machines or nodes talking to eachother that are running kafka
    - kafka used to use zookeeper for topics, now it uses its own internals
- topic is just a sequence of events coming in
    - rides contains everything pertaining to rides
    - there's a key and a value and a timestamp
        - these three things form a message
- how does kafka provide reliablility?
    - replication: a "leader" node will write a message in the logs that is submitted by the producer
        - this message is replicated in a "follower" node
    - if the "leader" node goes down, producers and consumers will not know the difference, but the "follower" node becomes a leader and starts replicating to another available node

### Retention
- if you set a day-long retention, any message in a log older than one day will get deleted from nodes (all nodes? would make sense)

### Partitioning
- a topic will be split between the amount of nodes you partition by
- there is still replication going on between the utilized nodes
- in the partitioning case, multiple nodes will be communicating with consumers and producers
- you still have the "follower"/"leader" behavior for replication, but it is done with partitions instead of whole topics/logs being replicated across nodes
- consumers can only read from one partition at a time
    - theoretically, if you had a large processing requirement or delay, you could use multiple consumers to spread out the time and "multithread" the reading of messages
        - kafka doesn't operate this way however
        - we use multiple partitions instead
- consumer group ids help kafka understand that a group of consumers are going to be independently reading individual paritions
    - kafka scales out and provides reliability in the case of partitioning using the knowledge that there are say (partitions)+1 consumers
    - in the event that a consumer goes down, kafka will redirect partition messages to the spare consumer
        - it's a good idea to have an idle consumer

### Offsets
This is how kafka determines that a consumer has already read a particular message and it should now read a different one
- there is an internal kafka topic called `__consumer_offset`
    - stores consumer.group.id, topic, partition, offset
    - kafka stores each consumer's "commit" data for message consumption
    - this is kind of like the way CDC is stored in databases
- if a consumer dies and is restarted, kafka will be able to start the consumer back off on the right foot (message) based on data in `__consumer_offset`
- `AUTO.OFFSET.RESET`
    - you have latest and earliest
    - this helps kafka know how to react when a new consumer group has been attached to it 
    - when you set your `AUTO.OFFSET.RESET` to earliest, kafka assumes that you have a different consumer group id (than a group id which is set to read the latest message)
    - at this point, the new group id consumer will be able to read from say, message 0

### ACK.ALL
- this example is with a replication factor of 2 in mind
- a producer will publish a message to a node and this will then be replicated to a second node (replication factor 2)
- there are levels of ack.all
    - 0: fire and forget, the producer just fires the message and doesn't really care if it was delivered or not (like UDP as opposed to TCP, I think that's correct)
    - 1: publishing to leader node must be successful
    - all: leaders are written but followers are also for sure written
        - this means that even if the leader fails, the follower will have the message
        - this is one of the slowest ways to publish because if there is failure, it means you will have to re-publish the message (because no nodes received it)
        - it's a guarantee that messages will always be delivered
- your choice on this will depend on the importance of the data
- you can check out more configuration from the [kafka docs](https://kafka.apache.org/documentation/#configuration)