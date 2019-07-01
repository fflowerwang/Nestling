from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, session
from App.models import *

blue = Blueprint('blog', __name__)


# 首页
@blue.route('/')
def index():
    articles = Article.query.all()
    lanmus = Lanmu.query.all()
    return render_template('home/index.html', articles=articles, lanmus=lanmus)


@blue.route('/index/lm/')
def lm():
    cid = request.args.get('cid')
    print(cid)
    lanmu = Lanmu.query.get(cid)
    articles = lanmu.articles
    lanmus = Lanmu.query.all()
    return render_template('home/index.html', articles=articles, lanmus=lanmus)

@blue.route('/share/')
def share():
    return render_template('home/share.html')
@blue.route('/about/')
def about():
    return render_template('home/about.html')
@blue.route('/gbook/')
def gbook():
    return render_template('home/gbook.html')
@blue.route('/info/')
def info():
    return render_template('home/info.html')
@blue.route('/infopic/')
def infopic():
    return render_template('home/infopic.html')
@blue.route('/list/')
def list1():
    return render_template('home/list.html')

# 后台登陆
@blue.route('/admin/login/',methods=['GET',"POST"])
def admin_login():
    if request.method == 'POST':
        # 接受登陆参数
        username = request.form.get('username')
        userpwd = request.form.get('userpwd')
        users = User.query.filter_by(name=username).first()
        if users:
            if username == users.name and userpwd == users.passwd:
                res = redirect(url_for('blog.admin_index'))
                session['username'] = users.name
                return res
            else:
                return '先注册用户'
        else:
            return render_template('admin/login.html')

    return render_template('admin/login.html')


@blue.route('/admin/logout/')
def admin_logout():
    session.pop('username')
    res = redirect(url_for('blog.admin_index'))
    return res

#后台主页
@blue.route('/admin/index/')
def admin_index():
    username = session.get('username',default=None)
    return render_template('admin/index.html',username=username)


#栏目分类
@blue.route('/admin/category/')
def admin_category1():
    username = session.get('username', default=None)
    lanmus = Lanmu.query.all()
    return render_template('admin/category.html',lanmus=lanmus,username=username)


#增加栏目
@blue.route('/admin/addcategory/',methods=['POST','GET'])
def admin_category():
    username = session.get('username', '')
    if username:
        if request.method == 'POST':
            name = request.form.get('name')
            alias = request.form.get('alias')
            lm = Lanmu()
            lm.name = name
            lm.another_name = alias
            try:
                db.session.add(lm)
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
            return redirect(url_for('blog.admin_category1'))
        lanmus = Lanmu.query.all()
        return render_template('admin/category.html', lanmus=lanmus, username=username)

    else:
        return render_template('admin/index.html')



#修改栏目
@blue.route('/admin/upcate/',methods=['POST','GET'])
def update_lm():
    username = session.get('username', default=None)
    if username:
        if request.method == 'POST':
            id = request.form.get('id')
            name = request.form.get('name')
            alias = request.form.get('alias')
            lanmu = Lanmu.query.get(id)
            lanmu.name = name
            lanmu.another_name = alias
            db.session.commit()
            return redirect(url_for('blog.admin_category1'))
        id = request.args.get('cid')
        lanmu = Lanmu.query.get(id)
        return render_template('admin/update-category.html',lanmu=lanmu,username=username)
    else:
        return render_template('admin/index.html')


#删除栏目
@blue.route('/admin/deletecate/')
def admin_delete_category():
    username = session.get('username', default=None)
    if username:
        id = request.args.get('cid')
        lanmu = Lanmu.query.get(id)
        try:
            db.session.delete(lanmu)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        res = redirect(url_for('blog.admin_category1'))
        return res
    else:
        return render_template('admin/login.html')

#文章
@blue.route('/admin/article/')
def admin_article():
    username = session.get('username', default=None)
    articles = Article.query.all()
    return render_template('admin/article.html',articles=articles, username=username)


#增加文章
@blue.route('/admin/addarticle/',methods=['POST','GET'])
def admin_add_article():
    username = session.get('username', default=None)
    if username:
        if request.method == 'POST':
            title = request.form.get('title')
            cont = request.form.get("content")
            tag = request.form.get('tags')
            lid = request.form.get('category')
            date = request.form.get('time')
            print(date)
            art = Article()
            art.title = title
            art.cont = cont
            art.tag = tag
            # print(art.tag)
            art.date = date
            # print(art.date)
            art.lanmu = lid
            # print(art.lanmu)
            try:
                db.session.add(art)
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
            res = redirect(url_for('blog.admin_article'))
            return res
        lms = Lanmu.query.all()
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return render_template('admin/add-article.html',lms=lms,date=date,username=username)
    else:
        return render_template('admin/login.html')


#修改文章
@blue.route('/admin/upart/', methods=["POST", "GET"])
def admin_update_article():
    username = session.get('username', default=None)
    if username:
        if request.method == "POST":
            id = request.form.get('id')
            print(id)
            title = request.form.get('title')
            cont = request.form.get('content')
            tag = request.form.get('tags')
            lm_id = request.form.get('category')
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            article = Article.query.get(id)
            article.title = title
            article.cont = cont
            article.tag = tag
            article.date = date
            lanmu1 = Lanmu.query.get(lm_id)
            article.lanmu = lanmu1.id
            try:
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
            res = redirect(url_for('blog.admin_article'))
            return res
        aid = request.args.get('aid')
        article = Article.query.get(aid)
        lanmus = Lanmu.query.all()
        return render_template('admin/update-article.html', article=article, lanmus=lanmus,username=username)
    else:
        return render_template('admin/login.html')

#删除文章
@blue.route('/admin/deleteart/')
def admin_delete_article():
    username = session.get('username', default=None)
    if username:
        aid = request.args.get("aid")
        article = Article.query.get(aid)
        try:
            db.session.delete(article)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        res = redirect(url_for('blog.admin_article'))
        return res
    else:
        return render_template('admin/login.html')




