#!/bin/sh
docker stop watermelon_back_end
docker stop watermelon_db
docker rm watermelon_back_end
docker rm watermelon_db
