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

TODO: do stuff with terraform client + GCP