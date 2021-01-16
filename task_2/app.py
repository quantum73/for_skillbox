import os

from flask import Flask, redirect, url_for, request
from flask_admin import Admin, BaseView, expose
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from forms import *

POSTS_PER_PAGE = 5
RESULTS_LIMIT = 5

template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')

app = Flask(__name__, template_folder=template_dir)
app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://postgres:postgres@postgres/for_skillbox'

manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class Cats(db.Model):
    __tablename__ = 'cats'

    id = db.Column(db.Integer(), unique=True, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    breed = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return '<Cats %r>' % self.name


@app.route('/')
@app.route('/admin/')
def home():
    return redirect('/admin/admincats')


class AdminCats(BaseView):
    @expose('/')
    @expose('/page/<int:page>')
    @expose('/sorted/<int:sort_type>')
    def index(self, page=1, sort_type=0):
        if sort_type == 1:
            cats = Cats.query.order_by('name').paginate(page, POSTS_PER_PAGE, error_out=False)
        elif sort_type == 2:
            cats = Cats.query.order_by('breed').paginate(page, POSTS_PER_PAGE, error_out=False)
        elif sort_type == 3:
            cats = Cats.query.order_by('age').paginate(page, POSTS_PER_PAGE, error_out=False)
        else:
            cats = Cats.query.paginate(page, POSTS_PER_PAGE, error_out=False)

        return self.render('admin/cats.html', cats=cats, form=SearchForm())

    @expose('/detail/<int:cat_id>')
    def detail(self, cat_id):
        cat = Cats.query.get(cat_id)
        return self.render('admin/detail.html', cat=cat)

    @expose('/search', methods=['POST'])
    def search(self):
        search_data = request.form.get('search')
        return redirect(url_for('.search_results', query=search_data))

    @expose('/search_results/<query>')
    def search_results(self, query):
        results = []
        names = Cats.query.filter(Cats.name.ilike(f'%{query}%')).all()
        breeds = Cats.query.filter(Cats.breed.ilike(f'%{query}%')).all()
        descriptions = Cats.query.filter(Cats.description.ilike(f'%{query}%')).all()
        ages = Cats.query.filter(Cats.age == query).all() if query.isdigit() else []

        results.extend(names)
        results.extend(breeds)
        results.extend(descriptions)
        results.extend(ages)
        results = set(results)
        return self.render('admin/search_results.html',
                           query=query,
                           results=results)


admin = Admin(app)
admin.add_view(AdminCats(name='Cats'))

if __name__ == '__main__':
    manager.run()
