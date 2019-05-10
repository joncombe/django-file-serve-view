django-file-serve-view
====

*Note: proper documentation coming soon*

This small class-based view allows you to serve static files via Django.

A common use-case would be have a "downloads" section of your website, but the downloads are only available to certain users, i.e. where `user.is_authenticated == True` and, optionally, pass other criteria of your choosing.

---

To install:
 - `pip install django-file-serve-view`
 - Add `fileserveview` to your `INSTALLED_APPS` within `settings.py`.

---

To serve files anyone can access, you can do something like this in your `urls.py`:
```
    path('robots.txt', FileServeView.as_view(
        authenticated_user_only=False,
        filename=os.path.join(settings.STATIC_ROOT, 'robots.txt'),
        is_download=False
    )),
```
*Yes, this may not be the most efficient method of serving a robots file, but it illustrates the point*

---

To serve files only authenticated users can download, try:
```
    path('my-special-download', FileServeView.as_view(
        filename=os.path.join(
            settings.BASE_DIR,
            '/path/to/get-rich-quick.pdf'
        ),
    )),
```

---

To do things more complex, including url path rules... docs coming soon. Sorry.