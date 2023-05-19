# Data Lake vs. Data Warehouse
- what's a data lake?
    - central repository that holds data from many sources
    - all kinds of structures for data
        - semi, un, fully
    - the main idea is quick ingestion
    - used for machine learning and analytics
    - generally needs to be secure
- comparison
    - data lake
        - users: data scientists/analysts
        - lots of big data
        - stream processing, ML, real-time analytics
    - data warehouse
        - users: business analysts
        - data is typicaly structured
        - batch processing, BI reporting  

## How it started 
- companies realized the value of the data that they just had sitting around
- the main idea is to get the data from it's raw form to being useful as quickly as possible
    - we don't wait to determine relationships and things like referential integrity here as we do in a DW
- because data tends to be more useful in the later stages of a project, companies sought to put data into a stored form as soon as possible
    - this came down to storing the data as cheaply as possible

## ETL vs ELT
- the export and load steps are flipped around
- ELT is something we tend to favor when working with quite large amounts of data
- as opposed to ETL processes, ELT is *schema on read*
    - we write the data first and the determine schema upon reading

## Gotchas
- can be well intentioned
    - turns into a data swamp
    - different data/file types can make things difficult to use
- there's no versioning
- no metadata
- can't really join (unless there's some kind of other infrastructure that runs on top of the data lake)
    - note to self: thinking maybe delta lake or hudi tables?
    - what are these, do these make a difference in cases like this?
    - what's the technical overhead and does it make more sense to work with a DW
        - probably depends on size of data

## Cloud providers
- GCP: cloud storage
- AWS: S3
- Azure: Azure Blob