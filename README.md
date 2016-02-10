# python-rest2cliapi
Provide a Gateway: Server which receives JSON/REST request and translates it to a Command Line Run (CLI). Please be aware that this might be a security hazard!

A quick an dirty build gateway in python to provide a REST Server (Bottle) which accepts POST request and interprets the URL to use it as a command to execute in the shell. Additionally standard arguments can be configured or given as a JSON body in the call. If developed further this would give a powerful custom and flexible API!

__Attention__: there is no authentication / encryption whatsoever! There is no command validation and escaping, you could easily damage something! I suggest to use this in controlled environments only - run only as super-unprivileged user (a good idea to create a seperate one!) or within a secured container!
