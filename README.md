# django_format_template

Uses BeautifulSoup to parse an HTML file and iterate over the following HTML tags: `a`, `link`, `script`, `img`.  These elements can contain href or src attributes referring to static files through a directory path or URL.  If an element is found to have an href or src attribute using a directory path it's updated to use Django's template tag syntax with an optional prefix.
```
{% static 'prefix/original/resource/path/file.ext' %}
```

### Usage:
```
from django_format_template import StaticFormat

file_path = "index.html"
sf = StaticFormat(file_path)
sf.replace_locators(prefix="home")
sf.write_html("output.html")
```
Now all static file paths will be formatted to use django template tag syntax.

### Intended Use Case
There's an HTML document that you would like to serve through Django that came with some static assets in the following directory structure:
```
 |  index.html
 |  assets/
 |       imgs/
 |           myimg.png
 |       css/
 |           style.css
```

Typically I would like to store static files in my static directory within another subdirectory like `home` in this example
```
|static/
|    home/
|       assets/
|           imgs/
|               myimg.png
|           css/
|               style.css
```                 
This way I can modularize different parts of my static files based on their use in the application.  For example my static dir may have another subdirectory `auth` that contains static files related to authentication.

This means that all of our static resources must be formatted as follows to be served through Django:
```
{% static 'home/resource/path' %}
```
Manually, this would mean going through the document and reformatting all file paths to meet the Django syntax.  Instead, the StaticFormat class can be used to do so automatically.
