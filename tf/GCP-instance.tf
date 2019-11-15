# Requirements: 
# - login-details.json: GCP credentials (see https://console.cloud.google.com/apis/credentials)
# - start-up-script.sh: script for setting up the CUDA + Jupyter environment upon the provisioning of the GCP instance
variable "region" {
  default = "us-west1" // We're going to need it in several places in this config
}

provider "google" {
  credentials = "${file("login-details.json")}"
  project     = "privapi-dl"
  region      = "${var.region}" // Call it from variable "region"
}

resource "google_compute_firewall" "allow-http" {
    name = "allow-http"
    network = "default"

    allow {
        protocol = "tcp"
        ports = ["80"]
    }

    source_ranges = ["0.0.0.0/0"]
    target_tags = ["http"]
}

resource "google_compute_instance" "privapi" {
  count        = 1
  name         = "privapi-gpu"
  machine_type = "n1-standard-4"
  zone         = "${var.region}" // Call it from variable "region"

  tags = ["http"]

 boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-1604-lts"
      size = 50
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral IP - leaving this block empty will generate a new external IP and assign it to the machine
    }
  }

  guest_accelerator{
    type = "nvidia-tesla-p100" // Type of GPU attahced
    count = 1 // Num of GPU attached
  }

  scheduling{
    on_host_maintenance = "TERMINATE" // Need to terminate GPU on maintenance
  }

  metadata_startup_script = "${file("start-up-script.sh")}" // Add the startup script locally

}
