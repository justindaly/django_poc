from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)


def index(request):
    resp = {}
    logger.info('in index')
    return render(request, 'index.html', resp)
