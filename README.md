# python-rest2cliapi
Provide a Gateway: Server which receives JSON/REST request and translates it to a Command Line Run (CLI). Please be aware that this might be a security hazard!

A quick an dirty gateway, build in python to provide a REST Server (Bottle) which accepts POST request and interprets the URL to use it as a command to execute in the shell. Additionally standard arguments can be configured in a JSON configuration file or given as a JSON body in the call. If developed further this would give a powerful custom and flexible API!

__Attention__: there is no authentication / encryption whatsoever! There is no command validation and escaping, you could easily damage something! I suggest to use this in controlled environments only - run only as super-unprivileged user (a good idea to create a seperate one!) or within a secured container!

This program should be used behind a reverse-proxy (like nginx) which can handle the authentication and pass the username as header in the request.

You should not configure 0.0.0.0 as host listening IP.


Example calls
```bash
curl -X POST -H "user: testuser" -H "Content-Type: application/json" -d "{\"arguments\":[\"ping from host\"]}" http://localhost:8180/echo
curl -X POST -H "user: testuser" -H "Content-Type: application/json" -d "{\"arguments\":[\"-la\"]}" http://localhost:8180/ls
```

Create a password file (or use the one within this repo)
```bash
docker run --rm --entrypoint htpasswd registry:2 -bn testuser testpassword > auth/nginx.htpasswd
```

Example with nginx in front (change 192.168.99.100 to whatever IP you have):
```bash
curl -X POST -H "Content-Type: application/json" --user testuser:testpassword -d "{\"arguments\":[\"ping from host\"]}" http://192.168.99.100/rest2cli/echo
```
