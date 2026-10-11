import pathlib
r=pathlib.Path(__file__).parent
css=(r/'base.css').read_text()

css=css.replace('</style>',(r/'extra.css').read_text()+'\n</style>')
head='''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#190333">
<title>Begleitraum · Das erste Mal führen</title>
'''
out=head+css+'\n</head>\n'+(r/'body.html').read_text().split('<footer')[0]+'\n<script>\n'+(r/'app.js').read_text()+'\n</script>\n<footer'+(r/'body.html').read_text().split('<footer',1)[1]+'</body>\n</html>\n'
(r.parent/'index.html').write_text(out)
print(len(out))
