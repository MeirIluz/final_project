# Algorithm

### Service Overview

- Version: 0.1.0
- Author: Ayala Kluft
- Date: 07/08/2025

### Description

Processes frames from shared memory to detect human presence and pose; updates frames with pose overlay and triggers an alert on any detected movement.

### Prerequisites

- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/) (for cloning the repository)

### OS Restrictions

Runs on any OS with Docker support.

### Installation

```bash
git clone https://yf-software-dev@bitbucket.org/yf-software-dev/digital_vehicle_algorithm.git
```

### Usage

- Environment Variables  
  To run this project, you will need to add the following environment variables to your .env file or to _environment_ section in this service on docker-compose.yml file.

  ```bash
  - DISPLAY=$DISPLAY
  - QT_X11_NO_MITSHM=1
  - ZMQ_SERVER_HOST=<zmq_server_microservice_name>
  - ZMQ_SERVER_PORT=<port_number>
  - NVIDIA_VISIBLE_DEVICES=all
  - NVIDIA_DRIVER_CAPABILITIES=compute,utility,video,graphics
  - CAMERA_USERNAME_KEY=<camera_username>
  - CAMERA_PASSWORD_KEY=<camera_password>
  ```

- Docker Dependencies:  
  To run this project, you will need to add the following docker dependencies to _depends_on_ section in this service on docker-compose.yml file.

  ```bash
  - kafka
  ```

- Run the service and its dependencies using Docker Compose:
  ```bash
  docker compose up --build
  ```
  (Use digital_vehicle_docker_compose repository)
- Run Command
  ```bash
  python3 src/main.py
  ```

### Documentation

For full usage and integration details, see the
[algorithm microservice documentation](https://tikshuv-my.sharepoint.com/:w:/r/personal/319045175_idf_il/_layouts/15/Doc.aspx?sourcedoc=%7BF008E976-F9F3-484E-AD9B-66BA1CE6974E%7D&file=digital_vehicle_algorithm.docx&action=default&mobileredirect=true)
