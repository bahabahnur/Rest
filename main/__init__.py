from __future__ import absolute_import, unicode_literals

"""
Это гарантирует, что приложение всегда импортируется при 
запуске Django, чтобы shared_task использовала это приложение. 
"""
from .celery import app as celery_app

__all__ = ('celery_app', )
