terraform {
    required_version = ">= 1.0"
    backend "local" {} # you can change this to your cloud provider if you want to preserve state online
    required_providers {
      google = {
          source = "hashicorp/google"
      }
    }
}

provider "google" {
    project = var.project
    region = var.region
    // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# data lake bucket
resource "google_storage_bucket" "data_lake_bucket" {
    name = "${local.data_lake_bucket}_${var.project}"
    location = var.region

    # optional settings
    storage_class = var.storage_class
    uniform_bucket_level_access = true 

    versioning {
        enabled = true
    }

    lifecycle_rule {
      action {
        type = "Delete"
      }

      condition {
        age = 30
      }

    }
    
    force_destroy = true
}

# data warehouse
resource "google_bigquery_dataset" "dataset" {
    dataset_id = var.BQ_DATASET
    project = var.project
    location = var.region
}