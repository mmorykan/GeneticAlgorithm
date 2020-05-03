# Set up rabbitmq and redis configuration with celery
BROKER_URL = 'amqp://mmorykan:tissuebox1234@3.22.170.142'
CELERY_RESULT_BACKEND = 'redis://:shelbyspurplecollarandharness....@3.22.170.142'
# Make sure that celery knows to use pickle as well as JSON for task serialization
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_TASK_SERIALIZER = ['pickle', 'json']
