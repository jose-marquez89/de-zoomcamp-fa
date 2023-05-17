# Terraform + GCP

## GCP - Where stuff is
- new project
    - project selection > add new project button
- new service account
    - IAM and Admin > Service Accounts > create service account button

### What stuff is
- service accounts can be set up for a particular service with different levels of permissions
    - managing keys: you can create a set of keys for a service account
    - you get these in a JSON format that you need to save somewhere because you only get access to it once
- datalake - GCS (google cloud storage)
    - gives you a way to store raw data in a more organized way
    - partitioned by more sensible directories
- GBQ (google big query)
    - more like a big data warehouse
- roles
    - we granted permissions for the bucket itself and objects in the bucket
    - in real production we would have custom roles (as opposed to the GCP preset roles)
    - we used "Storage Admin", "Storage Object Admin" and "BigQuery Admin"
- comm APIs
    - the local environment doesn't communicate directly with resources
    - it uses API endpoints to interact with the target resource
    - when enabling APIs make sure that you are on the intended project
        - it appears that you can have different APIs enabled on different projects


#### Setting Google application credentials for gcloud
```
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"

# Refresh token/session, and verify authentication
gcloud auth application-default login
```

The above step allows your CLI to interact with the cloud environment. This is OAuth but it's not the only way, there are other ways that don't involve a browser.

### Some bash stuff
- the command `ls -ltr` gives you permissions, users and timestamps for files in a directory
    - you can specify a certain subset of files like this `ls -ltr ~/Downloads/global-maxim-*`

TODO: build gcp resource with new terraform files (check files for accuracy first)