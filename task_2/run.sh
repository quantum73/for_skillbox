#!/bin/bash

docker-compose build
docker-compose up -d
docker-compose exec app python app.py db upgrade
