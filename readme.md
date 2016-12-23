FreeSWITCH ADMIN API
--------------------


### 1. List of all active conferences

- Request

```
GET $HOST/conferences
```

 - Response

List of all actives conference along with their details. JSON format



### 2. Get detail of a conference

- Request

```
GET $HOST/conferences/<conference_name>/
```

- Response
Either:
    - 404 Not Found
    - 200 OK, JSON content of conference

### 3. Booking a conference

- Request
```
GET $HOST/conferences/free
```

- Response
Either
    - 404 Not Found
    - 200 OK, room number

### 4. Set view for admin

- Request

```
POST $HOST/conferences/<conference_name>/admin/<viewer>/<viewee>
```

- Response
Either
    - OK
    - NOK: in case command is invalid



