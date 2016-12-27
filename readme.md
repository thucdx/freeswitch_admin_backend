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

Either:

    - 404 Not Found
    - 200 OK, room number

### 4. Init monitoring

It must be called when new admin join conference. This makes user seeing each other, while admin can see user.

- Request

```
POST $HOST/conferences/<conf_name>/init
```

- Response

OK

### 5. Set view for admin

- Request

```
POST $HOST/conferences/<conference_name>/<viewer>/<viewee>
```

`<viewer>` must be number of an admin
`<viewee>` must be number of a normal user
- Response

Either:

    - OK
    - NOK: in case command is invalid



