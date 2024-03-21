# Introduction

Welcome to the Monitoring Docker repository! This repository provides a Docker stack for deploying Grafana, Prometheus, and Node Exporter for monitoring Docker containers.

# Contents
- [Introduction](#introduction)
- [Deployment Steps](#deployment-steps)
- [Adding More Servers to Prometheus](#adding-more-servers-to-prometheus)
- [Folder Structure](#folder-structure)

# Monitoring Docker with Grafana, Prometheus, and Node Exporter

This repository provides a Docker stack for deploying Grafana, Prometheus, and Node Exporter for monitoring Docker containers.

## Deployment Steps

1. Clone the repository:
   ```
   git clone https://github.com/digitalstudium/grafana-docker-stack.git
   ```

2. Deploy the stack using the provided Docker Compose file:
   ```
   docker stack deploy -c grafana-docker-stack/docker-compose.yml monitoring
   ```

3. Add Prometheus datasource to Grafana:
   - Access Grafana dashboard.
   - Navigate to Configuration > Data Sources.
   - Add Prometheus datasource with address `http://prometheus:9090`.

4. Modify Prometheus config:
   - Add the following lines to the bottom of `/var/lib/docker/volumes/monitoring_prom-configs/_data/prometheus.yml` file:
     ```
     scrape_configs:
       - job_name: 'node-exporter'
         static_configs:
           - targets: ['node-exporter:9100']
     ```

5. Reload Prometheus config:
   ```
   docker ps | grep prometheus | awk '{print $1}' | xargs docker kill -s SIGHUP
   ```

6. Import Grafana dashboard:
   - Import [this dashboard](https://grafana.com/grafana/dashboards/1860) to Grafana.

## Adding More Servers to Prometheus

If you want to add more servers to Prometheus for monitoring, follow these steps:

1. Install Node Exporter to each server:
   ```
   git clone https://github.com/digitalstudium/grafana-docker-stack.git
   docker stack deploy -c grafana-docker-stack/node-exporter.yml node-exporter
   ```

2. Modify Prometheus config:
   - Add the additional servers to `/var/lib/docker/volumes/monitoring_prom-configs/_data/prometheus.yml` file:
     ```
     - targets: ['node-exporter:9100', 'server1:9100', 'server2:9100', '...']
     ```

3. Reload Prometheus config:
   ```
   docker ps | grep prometheus | awk '{print $1}' | xargs docker kill -s SIGHUP
   ```


That's it! Your monitoring setup is now ready, and you can add more servers to Prometheus as needed.

## Folder Structure

- **dashboards**: Contains Grafana dashboard configurations.
- **keys_roman**: Placeholder for any specific keys or credentials.
- **monitoring**: Docker Compose file and Prometheus configuration for monitoring setup.
- **playbooks**: Ansible playbooks for automated server configuration.
- **scripts**: Scripts for automation or additional functionality.


