# ka-rooms

Microservice to keep track of room ids and their corresponding types.

## Setup

1. Build the docker image:
```
docker build -t ka-rooms https://github.com/ITA-Super-Cool-Pals/ka-rooms.git#main
```

2. Run the docker image:
```
docker run --rm -d -p 5001:5000 -v /path/to/db/dir:/app/app-db --name ka-rooms ka-rooms
```
Ensure you replace `/path/to/db/dir` with the path to where you save the database on your local machine

## API Endpoints

### Get list of rooms
- URL: `/rooms`
- Method: `GET`
- Response:
  - **200:** List rooms

### Get list of specific room
- URL: `/rooms/{id}`
- Method: `GET`
- Response:
  - **200:** List specific room by id
  - **404:** Room id not found

### Create new room
- URL: `/rooms`
- Method: `POST`
- Request Body: JSON
   ```
   {
	"roomId": id,
	"type": "type"
   }
   ```
- Response:
  - **201**: Room created
  - **409**: Room ID already exits
  - **400**: Invalid data

### Update existing room's type
- URL: `/rooms/{id}`
- Method: `PATCH`
- Request Body: JSON
   ```
   {
    "type": "type"
   }
   ```
- Response:
  - **200**: Room updated
  - **400**: Invalid data
  - **404**: Room id not found

### Delete existing room
- URL: `/rooms/{id}`
- Method: `DELETE`
- Response:
  - **200**: Room deleted
  - **404**: Room id not found
