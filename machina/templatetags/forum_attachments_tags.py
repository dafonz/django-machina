# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mimetypes

from PIL import Image
from django import template

register = template.Library()


@register.simple_tag
def is_image(attachment):
    content_type, _ = mimetypes.guess_type(attachment.file.name)
    if content_type == 'image/jpeg' or content_type == 'image/gif' or content_type == 'image/png':
        try:
            trial_image = Image.open(attachment.file.file.name)
            trial_image.verify()
            return True
        except:
            return False

    return False
