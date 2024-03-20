# Weather Station Client
### Description
Software to get weather data from a Raspberry Pi based weather station using Bosch's BME280 or BME680.
It connects to the API specified in the [openapi spec file](openapi.json)

### Default GPIO-Pin Setup
Default GPIO pin:
1. sda_pin: 3
2. scl_pin: 2

#### Requirements / Prerequesits
1. Enable I2C in raspi-config
2. docker
3. git
4. i2c-tools (to check whether the sensor is detected correctly)
5. python3-venv

Requirements can be installed via the script install_prerequisits.sh in installation

### Docker - Containerization
#### Build docker container:
```
docker build -t weather_station:latest .
```

#### Run docker container:
**Run container for testing:**
```
docker run --device /dev/gpiomem --privileged --env-file=environments/example.env <path_to_config_folder>:/app/config -v /etc/localtime:/etc/localtime:ro weather_station:latest
```

**Run container with automatic restart and deteached:**
```
docker run -d --device /dev/gpiomem --privileged --env-file=environments/example.env -v <path_to_config_folder>:/app/config -v /etc/localtime:/etc/localtime:ro [--name <weather_station_date>] [--restart always] weather_station:latest
```
Note that path_to_config_folder must contain a file called "config.yaml" that follows the structure in config/conf.yaml in the repo.

**Run container with docker-compose:**
The service can be run with docker-compose with the following requirements:
1. Configuration yaml resides in "/opt/weather_station/config/conf.yaml"
2. Environment file resides in "/opt/weather_station/environment.env"

The container can be started with: ```docker compose up -d --restarart=always```
