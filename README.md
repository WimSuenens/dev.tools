
# Deployement

```bash
# Create virtual environment
pipenv --python /usr/bin/python3 install

# Activate virtual environment
pipenv shell

# Run migrations
python ./server/manage.py migrate

# Run application
python ./server/manage.py runserver

pipenv lock
pipenv requirements > requirements.txt
```

```bash
# docker buildx build --platform linux/amd64,linux/arm64 -t wimsuenens/dev.tools:latest -t wimsuenens/dev.tools:1.0.3 .
docker buildx build --platform linux/amd64,linux/arm64 -t wimsuenens/dev.tools:latest -t wimsuenens/dev.tools:1.0.4 .
```

```bash
# docker push -a wimsuenens/dev.tools
docker push wimsuenens/dev.tools --all-tags 
```
