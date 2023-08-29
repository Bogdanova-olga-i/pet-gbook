from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from growthbook import GrowthBook, Experiment, Result
from sqlalchemy import select
import yaml
from sqlalchemy import ForeignKey
from datetime import datetime
import pymysql

app = Flask(__name__)

db_conf = yaml.full_load(open('mysql_db.yml'))

# mysql://username:password@host:port/database_name
connection_str = 'mysql+pymysql://' + \
               db_conf['mysql_user'] + \
               ':' + db_conf['mysql_password'] + \
               '@' + db_conf['mysql_host'] + \
               '/' + db_conf['mysql_db']
app.config['SQLALCHEMY_DATABASE_URI'] = connection_str
db = SQLAlchemy(app)


# система сбора метрик
def on_experiment_viewed(experiment = Experiment, result = Result):
    request_url = request.url
    # получаем из url user_id
    try:
      user_id = request.url.split('user_id_')[1]
    except IndexError:
      user_id = 0
    # загружаем название эксперимента
    feature_key = experiment.key
    # проверяем есть ли такой пользователь в эксперименте
    no_user_in_experiment = db.session \
      .query(ExperimentData.user_id) \
      .filter_by(user_id=user_id) \
      .filter_by(feature_key=feature_key).first() is None
    #  если пользователя нет, но в запросе его id есть:
    if no_user_in_experiment and user_id != 0:
        feature_value = result.key
        # если пользователем совершено целевое действие и статус респонса 200
        if request_url.count('target_action/') and response.status_code == 200:
            target_action = 1
        else:
            target_action = 0

        # создаем запись в таблице экспериментов
        experiment_record = ExperimentData(
            user_id=user_id,
            feature_key=feature_key,
            feature_value=feature_value,
            target_action=target_action
        )
        # записываем в БД
        try:
            db.session.add(experiment_record)
            db.session.commit()
        except:
            print ('Не удалось записать данные об эксперименте')

    # если запись о пользователе есть в таблице экспериментальных данных
    elif no_user_in_experiment == False and user_id != 0:
        # если данные о юзере есть в запросе:
        if user_id !=0:
            # смотрим значение целевого действия
            target_action = db.session \
                .query(ExperimentData.target_action) \
                .filter_by(user_id=user_id) \
                .filter_by(feature_key=feature_key).first()

            if target_action == 0 and request_url.count('target_action/') > 0:
                experiment_id = db.session \
                    .query(ExperimentData.id) \
                    .filter_by(user_id=user_id) \
                    .filter_by(feature_key=feature_key).first()
                experiment_record = ExperimentData.query.get(experiment_id)
                experiment_record.target_action = 1
                try:
                    db.session.commit()
                except:
                    print("Не удалось обновить запись эксперимента")
    return 'Данные эксперимента успешно обработаны и записаны в БД'


# делаем  middleware
@app.before_request
def start_middleware():
    print ('\n Начало запроса \n')
    request.gb = GrowthBook(
        api_host="http://localhost:3100",
        client_key="sdk-anpYqAnWvTuLSR"
        )
    try:
        user_id = request.url.split('user_id_')[1]
    except IndexError:
        user_id = 0
    # отладка принтами
    print (f'Experiment my-feture is on? : {request.gb.is_on("my-feature")}')
    print (f'Request.url : {request.url}')
    print (f'User_id: {user_id}')
    request.gb.load_features()



@app.after_request
def stop_middleware(response):
#    experimrnt_recording = on_experiment_viewed()
    request.gb.destroy()
    print ('\n Middleware WORKED!! \n')
#    print (experimrnt_recording)
    return response


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)

class ExperimentData(db.Model):
    __tablename__ = 'experiment_data'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(ForeignKey('user.id'), nullable=False)
    feature_key = db.Column(db.String(100))
    feature_value = db.Column(db.String(100))
    target_action = db.Column(db.Integer)
    entered_at = db.Column(db.DateTime, default=datetime.now())

class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route('/posts/user_id_<int:id>')
def posts_user_id(id):
    articles = Article.query.order_by(Article.date).all()
    return render_template("posts_with_user_id.html", articles=articles, id=id)


@app.route('/posts/article/article_id_<int:art_id>')
def post_detail(art_id):
    article = Article.query.get(art_id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/article/article_id_<int:art_id>/del')
def post_delete(art_id):
    article = Article.query.get_or_404(art_id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"

@app.route('/posts/article/article_id_<int:art_id>/update', methods=['POST', 'GET'])
def post_update(art_id):
    article = Article.query.get_or_404(art_id)

    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При обновлении статьи произошла ошибка"

    else:
        return render_template('post_update.html', article=article)


@app.route('/create_article', methods=['POST', 'GET'])
def create_article_make_author():
    if request.method == 'POST':
        author = request.form['user']

        # проверка есть ли такой юзер
        exists = db.session.query(User.id).filter_by(user=author).first() is None

        if exists:
            user = User(user=author)
            db.session.add(user)
            db.session.commit()

        user_id = db.session.execute(db.select(User.id).where(User.user == author)).first()[0]

        return redirect(f'/create_article2/user_id_{user_id}')

    else:
        return render_template("create_article.html")

@app.route('/create_article2/user_id_<int:id>', methods=['POST', 'GET'])
def create_article_make_article(id):
    if request.method == 'POST':
        if request.gb.is_on("my-feature"):
            print("Feature is enabled!")
            title = f'Control: Экспериментальный заголовок пользователья {id}'
            intro = f'Control: Экспериментальная аннотация пользователья {id}'
            text = f'Control: Экспериментальный текст пользователья {id}'
            user_id = id

        else:
           title = request.form['title']
           intro = request.form['intro']
           text = request.form['text']
           user_id = id


        article = Article(title=title, intro=intro, text=text, user_id=user_id)
        id = id

        db.session.add(article)
        db.session.commit()
        return redirect(f'/posts/user_id_{id}')

    else:
        return render_template("create_article2.html")

@app.route('/target_action/user_id_<int:id>')
def target_action(id):
    return render_template("target_action.html", id=id)


if __name__ == '__main__':
    app.run(debug=True)