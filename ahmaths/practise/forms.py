from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from ahmaths.models import Question


class MarkForm(FlaskForm):
    question = HiddenField('Question')
    mark = IntegerField('Mark', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_mark(self, mark):
        question = self.question
        mark = int(mark.data)
        max_mark = int(Question.query.filter_by(question_id=question.data).first().marks)
        if mark > max_mark or mark < 0:
            raise ValidationError('Mark must be between 0 and ' + str(max_mark) + '.')
