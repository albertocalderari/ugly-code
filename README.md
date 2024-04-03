# Order Worker

Order worker.

 - Installation: `make install-dev`
 - Coverage: `make coverage`
 - Run: `make run`
 - Docker Run: ` docker run -it -e AWS_DEFAULT_REGION=us-east-1 -e MONITOR=true -p 8000:8000 <container_id> -w <workers_count> --bind 0.0.0.0:8000 --access-logfile -`