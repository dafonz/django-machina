# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mimetypes
import os

from PIL import Image
from django.http import HttpResponse
from django.views.generic import DetailView

from machina.core.db.models import get_model
from machina.core.loading import get_class

Attachment = get_model('forum_attachments', 'Attachment')

PermissionRequiredMixin = get_class('forum_permission.viewmixins', 'PermissionRequiredMixin')


class AttachmentView(PermissionRequiredMixin, DetailView):
    """
    Allows to retrieve a forum attachment.
    """
    model = Attachment

    def render_to_response(self, context, **response_kwargs):
        filename = os.path.basename(self.object.file.name)

        # Try to guess the content type of the given file
        content_type, _ = mimetypes.guess_type(self.object.file.name)
        if not content_type:
            content_type = 'text/plain'

        # Check if the attachment is an image
        is_image = False
        if content_type == 'image/jpeg' or content_type == 'image/gif' or content_type == 'image/png':
            try:
                trial_image = Image.open(self.object.file.file.name)
                trial_image.verify()
                is_image = True
            except:
                is_image = False

        response = HttpResponse(self.object.file, content_type=content_type)
        if not is_image:
            # Attachment is not a verified image, let browser download it
            response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        return response

    # Permissions checks

    def get_controlled_object(self):
        return self.get_object().post.topic.forum

    def perform_permissions_check(self, user, obj, perms):
        return self.request.forum_permission_handler.can_download_files(obj, user)
