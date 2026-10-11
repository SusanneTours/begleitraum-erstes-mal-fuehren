import pathlib
r=pathlib.Path(__file__).parent
css=open('/tmp/claude-0/-home-claude/88d19f3e-f7e3-5f34-a7b4-c0d4a0c4e6fc/scratchpad/base.css').read() if pathlib.Path('/tmp/claude-0/-home-claude/88d19f3e-f7e3-5f34-a7b4-c0d4a0c4e6fc/scratchpad/base.css').exists() else (r/'base.css').read_text()
(r/'base.css').write_text(css)
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
