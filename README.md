# django_format_template

Uses BeautifulSoup to parse an HTML file and iterate over the following HTML tags which can load static resources: a, link, script, img.  If any element of any of these types contains a src or href attribute that does not represent a valid URL, the attribute value is formatted to meet django static template tag syntax.  This is to help with converting prebuilt HTML templates with local file paths to be served through Django.

### Usage
An HTML file can be converted to serve static files through Django as follows:
```
from django_format_template import StaticFormat

file_path = "index.html"
sf = StaticFormat(file_path)
sf.replace_locators(prefix="home")
```
Now all static file paths will be formatted to be (using passed prefix home):
```
{% static 'home/orignial/resource/path' %}
```
### Intended Use Case

Let's say you have this HTML document which you purchased/found online and would like to serve through Django that came with some static assets in the following directory structure:

 -  index.html
 -  assets/
 -       imgs/
 -           myimg.png
 -       css/
 -           style.css


Typically I would like to store static files in my static directory within another directory called `home` like

- static/
-    home/
-        assets/
-            imgs/
-                myimg.png
-            css/
-                style.css
                 
This way I can modularize different parts of my static files based on their use in the application.  For example my static dir may have another subdirectory `auth` that contains static files related to authentication.

This means that all of our static resources must be formatted as follows to be served through Django:
```
{% static 'home/resource/path' %}
```
Manually, this would mean going through the document and reformatting all file paths to meet the Django syntax.  Instead, the StaticFormat class can be used to do so automatically.
