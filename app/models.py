# 数据模型的设计与实现
# 建立数据库连接
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/movies'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# 会员
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # id
    uuid = db.Column(db.String(255), unique=True)  # 会员唯一标识符
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now) # 注册时间
    userlogs = db.relationship('UserLog', backref='user')  # 会员日志外键关联
    comments = db.relationship('Comment', backref='user')  # 评论外键关联
    movie_favs = db.relationship('MovieFav', backref='user')  # 收藏外键关联

    def __repr__(self):
        return '<User %r>' % self.name


# 会员登录日志
class UserLog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))  # 最近登录ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 最近登录时间
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员

    def __repr__(self):
        return '<UserLog %r>' % self.id


# 电影标签数据模型
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    movies = db.relationship('Movie', backref='tag')

    def __repr__(self):
        return '<Tag %r>' % self.name


# 电影数据模型
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    playnums = db.Column(db.BigInteger)  # 播放量
    commentnums = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 视频长度
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    comments = db.relationship('Comment', backref='movie')  # 评论外键关联
    movie_favs = db.relationship('MovieFav', backref='moive')  # 收藏外键关联

    def __repr__(self):
        return '<Moive %r>' % self.title


# 上映预告模型
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Preview %r>' % self.title


# 评论模型
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)  # 评论内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Comment %r>'% self.id


# 电影收藏模型
class MovieFav(db.Model):
    __tablename__ = 'movie_fav'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<MovieFav %r>' % self.id


# 权限数据模型
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)   # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Auth %r>' % self.name


# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 角色权限列表
    admins = db.relationship("Admin", backref='role')  # 管理员外键关系关联
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Role %r>'% self.name


# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(255))
    is_super = db.Column(db.SmallInteger)  # 是否超级管理员, 0为超级管理员
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    admin_logs = db.relationship('AdminLog', backref='admin')  # 登录日志外键关联
    operate_logs = db.relationship('OperateLog', backref='admin')  # 操作日志外键关联

    def __repr__(self):
        return '<Admin %r>' % self.account


# 管理员登录日志
class AdminLog(db.Model):
    __tablename__ = 'admin_log'
    id = db.Column(db.Integer, primary_key=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    ip = db.Column(db.String(100))  # 登录ip
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员

    def __repr__(self):
        return '<AdminLog %r>' % self.id


# 操作日志
class OperateLog(db.Model):
    __tablename__ = 'operate_log'
    id = db.Column(db.Integer, primary_key=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    ip = db.Column(db.String(100))  # 登录ip
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    reason = db.Column(db.String(600))  # 操作原因

    def __repr__(self):
        return '<OperateLog %r>' % self.id

if __name__ == '__main__':
    db.create_all()
