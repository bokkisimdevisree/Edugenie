p = "main.py"
s = open(p, encoding="utf-8").read()
old = 'templates.TemplateResponse("index.html", {"request": request})'
new = 'templates.TemplateResponse(request, "index.html")'
if old in s:
    s = s.replace(old, new)
    open(p, "w", encoding="utf-8").write(s)
    print("Patched successfully.")
else:
    print("Pattern not found. main.py may already be updated.")
