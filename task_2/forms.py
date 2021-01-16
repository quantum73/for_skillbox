import wtforms
from wtforms.validators import DataRequired


class SearchForm(wtforms.Form):
    search = wtforms.StringField('search', validators=[DataRequired()])
