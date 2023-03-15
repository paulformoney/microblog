from app import app,db
from app.models import User, Post


# 添加上下文，每次执行项目无需手动输入Import db等内容
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


if __name__ == '__main__':
    app.run(debug=False)