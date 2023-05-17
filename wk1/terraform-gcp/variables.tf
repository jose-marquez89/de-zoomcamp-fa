locals {
    data_lake_bucket = "dtc_data_lake"
}

# TODO: Add gcp project ID
variable "project" {
    description = "de-zc-i"
}

variable "region" {
    description = "GCP resource region"
    default = "europe-west6"
    type = string
}

variable "storage_class" {
    description = "Bucket storage class"
    default = "STANDARD"
}

variable "BQ_DATASET" {
    description = "BQ dataset that will get written to from other GCS resources"
    default = "trips_data_all"
    type = string
}
