# tracker
## Deploying
### Generate ssl-certificate
https://core.telegram.org/bots/self-signed
```
$ openssl req -newkey rsa:2048 -sha256 -nodes -keyout ./nginx/cert.key -x509 -days 365 -out ./nginx/cert.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=YOURDOMAIN.EXAMPLE"
```
### Run docker-compose
```
$ docker-compose up -d
```
