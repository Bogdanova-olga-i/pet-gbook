



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)

class ExperimentData(db.Model):
    __tablename__ = 'experiment_data'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(ForeignKey('user.id'), nullable=False)
    feature_key = db.Column(db.String(100))
    feature_value = db.Column(db.String(100))
    entered_at = db.Column(db.DateTime, default=datetime.now())

class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())