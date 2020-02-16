# Crawler

Scrape data from web sites and save data to the es.

### Prerequisites

- Docker
- Python

### How to start

1. Create ES (project root directory)
    ```
    docker-compose up
    ```

2. Install analysis-nori plug-in
    ```
    docker exec -it <container_id> /bin/bash
    cd /usr/share/elasticsearch/bin/
    ./elasticsearch-plugin install nalysis-nori
    ```

3. Restart ES

4. Install modules
    ```
    pip install requirements.txt
    ```

5. Start cralwer (crawler directory)
    ```
    python app.py
    ```