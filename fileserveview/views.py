from django.http import
from django.views.generic import View


class FileServeView(View)
   filename = None
   content_type = None
   is_download = None


    def get(self, request):
        self.send_file(self, request)


    def get_content_type(self, request):
        if self.content_type is None:
            suffix = self.filename.split('.')[-1:].lower()


    def get_is_download(self, request):
        if self.is_download is None:
            #
            #
            #
            pass


    def get_file(self, request):
        if self.filename is None:
            #
            # function to get filename
                # self.filename = ...
            #


    def has_permission(self, request):
        #
        #
        #
        return True


    def permission_denied(self, request):
        return 403


    def send_file(self, request):
        if not self.has_permission(request):
            return self.permission_denied(request)

        self.get_file()
        self.get_content_type(self, request)
        respond...
