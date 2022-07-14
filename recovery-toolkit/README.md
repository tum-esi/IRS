## Single container build
- docker build -t recovery_image:0.1 .
- docker run -p 5000:5000 recovery_image:0.1

## Docker backup commands
- docker commit container_name repository:tag (e.g. docker commit recovery recovery_image:1.0)
- docker save recovery_image:1.0
- docker load recovery_image:1.0
