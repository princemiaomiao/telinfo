# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.conf import settings


def site_processor(request):
    site_name = _(getattr(settings, 'PHONE_RECORD_SITE_NAME', ''))
    login_url_name = getattr(settings, 'LOGIN_URL_NAME', 'focus:login')
    return {
        'site_name': site_name,
        'login_url_name': login_url_name
    }
