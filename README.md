# calm-dashboard
Demo Custom Calm Dashboard

To run the dashboard in docker:

```shell
docker run --rm -p 8080:8080 -e PRISM_HOST=PRISM_CENTRAL_IP hexadtech/calm-dashboard
```


For VM console access, nginx is required. Run docker-compose:
```shell
git clone https://github.com/halsayed/calm-dashboard.git
cd calm-dashboard
docker-compose up
```

**Note:** Change the enviroement variables in docker-compose.yaml or create .env file locally
