# Deta Todo service

## Use cases

```puml
actor player
actor players_manager

usecase registration [
    <b>Registration</b>
    Create new user with unique email
]

player -> registration #line:red

usecase get_users [
    <b>Get users list</b>
]

players_manager -> get_users
```

## System design

```puml
actor user

node gateway [
    <b> GATEWAY </b>
    ===
    envoy/nginx etc.
    ---
    horizontal scaling
]
node api [
    <b> API </b>
    ===
    current python application
    ---
    horizontal scaling
]
database database [
    <b> DATABASE </b>
    ===
    postgres
    ---
    vertical scaling
]

user -> gateway: http request
gateway -> api: http request
api -> database: sql query

note bottom of api
    * auth
    * business logic
end note

```

## Code design (layers)

```puml
actor user
participant api
participant service
participant repository
database database

user -> api: http request
api -> service: domain command/query
service -> service: domain logic
service -> repository: domain action
repository -> database: sql query
repository <- database: sql rows
service <- repository: domain data
service -> service: domain logic
api <- service: domain data
user <- api: http response
```

## Database schema design

```puml
hide circle

entity Player {
  <b>id</b> : uuid primary key
  ---
  <b>email</b> : unique string
  <b>name</b> : unique string
  ---
  <b>created_at</b> : datetime
  <b>updated_at</b> : datetime
  <b>deleted_at</b> : nullable datetime
}
```
