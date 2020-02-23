from flask import current_app as app

# hello world
@app.route('/hello')
def hello():
    return 'hello, world'