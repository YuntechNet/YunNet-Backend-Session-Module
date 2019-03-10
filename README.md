
# YunNet Backend Session Module

| master  |   dev   |  
|:--------|:--------|  
| [![Build Status](https://travis-ci.com/YuntechNet/YunNet-Backend-Session-Module.svg?branch=master)](https://travis-ci.com/YuntechNet/YunNet-Backend-Session-Module) [![codecov](https://codecov.io/gh/YuntechNet/YunNet-Backend-Session-Module/branch/master/graph/badge.svg)](https://codecov.io/gh/YuntechNet/YunNet-Backend-Session-Module) | [![Build Status](https://travis-ci.com/YuntechNet/YunNet-Backend-Session-Module.svg?branch=dev)](https://travis-ci.com/YuntechNet/YunNet-Backend-Session-Module) [![codecov](https://codecov.io/gh/YuntechNet/YunNet-Backend-Session-Module/branch/dev/graph/badge.svg)](https://codecov.io/gh/YuntechNet/YunNet-Backend-Session-Module/branch/dev)  |  

## Production
```
$ docker-compose up -d
```

## Development
```
$ docker run -p 127.0.0.1:6379:6379 -d redis
$ python main.py --host=127.0.0.1 --port=5000 --db-host=127.0.0.1 --db-port=6379
```