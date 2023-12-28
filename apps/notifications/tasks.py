from nexestate.celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


# celery -A nexestate worker -l info
