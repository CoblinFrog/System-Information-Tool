import platform
import webbrowser
import os
processer = platform.processor()

from yattag import Doc

doc, tag, text = Doc().tagtext()

with tag('html'):
    with tag('body'):
        with tag('p', id='main'):
            text("Your processor is " + processer)


result = doc.getvalue()

with open("index.html", "w") as file:
    file.write(result)

file_path = os.path.abspath("index.html")
webbrowser.open(f"file://{file_path}")
