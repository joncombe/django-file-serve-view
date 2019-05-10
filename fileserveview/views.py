from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import View


class FileServeView(View):
    authenticated_user_only = True
    content_type = None
    download_filename = None
    filename = None
    is_download = True

    def error401(self, request, *args, **kwargs):
        return HttpResponse('Unauthorized', status=401)

    def error403(self, request, *args, **kwargs):
        return HttpResponseForbidden()

    def get(self, request, *args, **kwargs):
        return self.send_file(request, *args, **kwargs)

    def get_content_type(self, request, *args, **kwargs):
        if self.content_type is None:
            try:
                suffix = self.filename.lower().split('.')[-1:][0]
                # thank you:
                # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Complete_list_of_MIME_types
                self.content_type = {
                    'aac': 'audio/aac',
                    'abw': 'application/x-abiword',
                    'arc': 'application/x-freearc',
                    'avi': 'video/x-msvideo',
                    'azw': 'application/vnd.amazon.ebook',
                    'bin': 'application/octet-stream',
                    'bmp': 'image/bmp',
                    'bz': 'application/x-bzip',
                    'bz2': 'application/x-bzip2',
                    'csh': 'application/x-csh',
                    'css': 'text/css',
                    'csv': 'text/csv',
                    'doc': 'application/msword',
                    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'eot': 'application/vnd.ms-fontobject',
                    'epub': 'application/epub+zip',
                    'gif': 'image/gif',
                    'htm': 'text/html',
                    'html': 'text/html',
                    'ico': 'image/vnd.microsoft.icon',
                    'ics': 'text/calendar',
                    'jar': 'application/java-archive',
                    'jpeg': 'image/jpeg',
                    'jpg': 'image/jpeg',
                    'js': 'text/javascript',
                    'json': 'application/json',
                    'jsonld': 'application/ld+json',
                    'mid': 'audio/midi audio/x-midi',
                    'midi': 'audio/midi audio/x-midi',
                    'mjs': 'text/javascript',
                    'mp3': 'audio/mpeg',
                    'mpeg': 'video/mpeg',
                    'mpkg': 'application/vnd.apple.installer+xml',
                    'odp': 'application/vnd.oasis.opendocument.presentation',
                    'ods': 'application/vnd.oasis.opendocument.spreadsheet',
                    'odt': 'application/vnd.oasis.opendocument.text',
                    'oga': 'audio/ogg',
                    'ogv': 'video/ogg',
                    'ogx': 'application/ogg',
                    'otf': 'font/otf',
                    'png': 'image/png',
                    'pdf': 'application/pdf',
                    'ppt': 'application/vnd.ms-powerpoint',
                    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                    'rar': 'application/x-rar-compressed',
                    'rtf': 'application/rtf',
                    'sh': 'application/x-sh',
                    'svg': 'image/svg+xml',
                    'swf': 'application/x-shockwave-flash',
                    'tar': 'application/x-tar',
                    'tif': 'image/tiff',
                    'tiff': 'image/tiff',
                    'ttf': 'font/ttf',
                    'txt': 'text/plain',
                    'vsd': 'application/vnd.visio',
                    'wav': 'audio/wav',
                    'weba': 'audio/webm',
                    'webm': 'video/webm',
                    'webp': 'image/webp',
                    'woff': 'font/woff',
                    'woff2': 'font/woff2',
                    'xhtml': 'application/xhtml+xml',
                    'xls': 'application/vnd.ms-excel',
                    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'xml': 'application/xml',
                    'xul': 'application/vnd.mozilla.xul+xml',
                    'zip': 'application/zip',
                    '3gp': 'video/3gpp, *args, **kwargs',
                    '3g2': 'video/3gpp2',
                    '7z': 'application/x-7z-compressed'
                }[suffix]
            except:
                self.content_type = 'application/octet-stream'

    def get_is_download(self, request, *args, **kwargs):
        #
        # Add your own logic here whether the files should be
        # sent to the visitor as a download or displayed in
        # their browser, e.g.
        #
        #    if not request.user.wants_download:
        #        self.is_download = False
        #
        pass

    def get_filename(self, request, *args, **kwargs):
        #
        # Add your own logic here to set the filename, e.g.
        #     self.filename = '....'
        #
        pass

    def has_permission(self, request, *args, **kwargs):
        #
        # Add your own logic here to set the permissions on this file, e.g.
        #
        #    if not request.user.can_download:
        #       return False
        #
        return True

    def send_file(self, request, *args, **kwargs):
        # 401 for non-authenticated users who should be authenticated
        if self.authenticated_user_only and not request.user.is_authenticated:
            return self.error401(request, *args, **kwargs)

        # 403 for authenticated users who do not have permission
        if not self.has_permission(request, *args, **kwargs):
            return self.error403(request, *args, **kwargs)

        # init response
        self.get_filename(request, *args, **kwargs)
        self.get_content_type(request, *args, **kwargs)
        self.get_is_download(request, *args, **kwargs)

        # load file
        fp = open(self.filename, 'rb')
        response = HttpResponse(fp.read(), content_type=self.content_type)
        response['Content-Length'] = len(response.content)
        fp.close()

        # download?
        if self.is_download:
            if self.download_filename is None:
                self.download_filename = \
                    self.filename.replace('\\', '/').split('/')[-1:][0]
            response['Content-Disposition'] = 'attachment; filename="%s"' % \
                self.download_filename

        # serve
        return response