from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


# 接收到500错误时，回滚数据库提交并转到500页面（500为数据库错误，此处是提交重名数据库信息，即导致500错误的一种情况）
@app.errorhandler(500)
def not_found_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

