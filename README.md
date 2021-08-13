# tracker
## Deploying
### Generate ssl-certificate
https://core.telegram.org/bots/self-signed
```
openssl req -newkey rsa:2048 -sha256 -nodes -keyout YOURPRIVATE.key -x509 -days 365 -out YOURPUBLIC.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=YOURDOMAIN.EXAMPLE"
```
### Run docker-compose
```
docker-compose build && docker compose start
```
