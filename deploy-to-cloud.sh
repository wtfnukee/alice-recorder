#!/bin/bash

set -xe

DIR=$(dirname $0)

function _fail() {
    echo $0
    exit 1
}
which yc > /dev/null || _fail "Please install Yandex Cloud CLI, see: https://cloud.yandex.ru/docs/cli/quickstart"

NAME=alice-recorder
#yc serverless function create \
#   --name  $NAME \
#   --description "Alice Recorder v0"

yc serverless function version create \
   --function-name=$NAME \
   --runtime=python312 \
   --entrypoint=skill.handler \
   --source-path $DIR/skill\
   --memory=128M \
   --execution-timeout=3s\
   --environment TELEGRAM_BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN skill/.env | cut -d= -f2),TELEGRAM_CHAT_ID=$(grep TELEGRAM_CHAT_ID skill/.env | cut -d= -f2)
