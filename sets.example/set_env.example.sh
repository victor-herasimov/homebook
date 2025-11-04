#!/bin/sh

export SECRET_KEY="secret key"
export DEBUG="0"

export DATABASE_HOST="db host"
export DATABASE_PORT="db port"
export POSTGRES_USER="db user"
export POSTGRES_PASSWORD="db passs"
export POSTGRES_DB="db name"

export CELERY_BROKER_URL="celery url"

export DEVELOP_EMAIL_SERVER="0"
export MAILDEV_WEB_HOST="maildev"
export MAILDEV_WEB_PORT="1025"

export EMAIL_HOST="email host"
export EMAIL_HOST_USER="email user"
export EMAIL_HOST_PASSWORD="email pass"
export EMAIL_PORT="email port"
export EMAIL_USE_TLS="1"
# EMAIL_USE_SSL=1
export DEFAULT_FROM_EMAIL="email user"

export ALLOWED_HOSTS="allowed hosts"
export CSRF_TRUSTED_ORIGINS="csrf trusted origins"