from app import app


@app.route('/')
@app.route('/index')
def index():
    return "hello,world"


@app.route('/user/<name>')
def user(name):
    return f"hello,{name}"
# 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