## FastAPI Feature Flag Server with Flipt

This project is a FastAPI-based server that uses the Flipt feature flagging service to evaluate feature flags based on an incoming request. 
The FastAPI server interacts with the Flipt server using an asynchronous HTTP request and returns a boolean flag decision based on the Flipt response.<br>
The goal here is to check if `new-feature` flag is enabled or disabled based on on the browser the user is using (user-agent string).
The `new-feature` flag returns `true` for `mac-users` segment with the constraint that the `user_agent` property equals `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`, else returns false.

### Requirements

- Docker

### Setup and Run Instructions

#### Step 1: Clone the Repository

```bash
git clone https://github.com/nisha-sjsu/Knit.git
cd backend
```

#### Step 2: Build and Run the Flipt Server

First, set up the Flipt server. You can run Flipt in a Docker container by following the instructions in the [Flipt documentation](https://docs.flipt.io/introduction#quickstart), or you can use the following Docker command to set it up.

```bash
docker network create flipt-network

docker run --name flipt-server --network flipt-network -p 8080:8080 flipt/flipt:latest
```

This will create a Docker container for Flipt on port `8080`. The `--network flipt-network` option ensures the Flipt server is on the same network as the FastAPI container (to be created in the next step).

#### Step 3: Build the FastAPI Server Docker Image

With Docker configured in the project, build the FastAPI Docker image:

```bash
docker build -t fastapi-server .
```

#### Step 4: Run the FastAPI Server

To ensure the FastAPI container can communicate with the Flipt container, we’ll run it on the same Docker network (`flipt-network`).

```bash
docker run --name fastapi-server --network flipt-network -p 8000:8000 fastapi-server
```

Now, the FastAPI server will be running on port `8000` and can communicate with the Flipt server via the Docker network.

### Step 5: Testing the API

You can use `curl` to test the API. Replace `<key_name>` and `<request_id>` with appropriate values.

```bash
curl -X POST "http://localhost:8000/evaluate/boolean" \
    -H "Content-Type: application/json" \
    -H "useragent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
    -d '{"key_name": "<key_name>", "request_id": "<request_id>"}'
```

The FastAPI server will evaluate the feature flag by sending the request to the Flipt server via an asynchronous HTTP call.

### Important Notes

1. **Networking**: Both the FastAPI server and the Flipt server are running in Docker containers on the same network (`flipt-network`). This allows them to communicate using container names instead of IP addresses. When making an HTTP request from the FastAPI server to Flipt, you should reference the Flipt container by its container name (`flipt-server`) in the async HTTP request, like this:

   ```python
   async with httpx.AsyncClient() as client:
       flipt_response = await client.post(
           "http://flipt-server:8080/api/v1/feature-flags/{key_name}/evaluate",
           json=flipt_payload
       )
   ```

2. **Flipt API**: Make sure to configure your Flipt flags appropriately via the Flipt API or admin interface. You can access the Flipt UI at `http://localhost:8080`.

### Step 6: Stopping and Cleaning Up

To stop the containers:

```bash
docker stop fastapi-server flipt-server
```

To remove the containers:

```bash
docker rm fastapi-server flipt-server
```

---

### Troubleshooting

- If the FastAPI container cannot connect to the Flipt server, ensure both are on the same Docker network (`flipt-network`) and use the container name `flipt-server` in the FastAPI app to communicate with the Flipt container.
  
- Check that the Flipt server is running and accessible at `http://localhost:8080`.

### License

This project is licensed under the MIT License.

---
