"""Forms for blogly."""

from wtforms import widgets, SelectField, StringField, TextAreaField, SelectMultipleField
from wtforms.validators import InputRequired, URL, Optional
from flask_wtf import FlaskForm
from models import Tag


class MultiCheckboxField(SelectMultipleField):
    """Create multi-checkbox form"""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
    # How to set list-style = none (no bullets?)
    # html_tag="ul style='list-style: none'"


class UserForm(FlaskForm):
    """User Form"""

    first_name = StringField("First Name: ", [InputRequired()])
    last_name = StringField("Last Name: ", [InputRequired()])
    image_url = StringField(
        "Image URL: ", [Optional(), URL(message="Please enter a URL")])


class PostForm(FlaskForm):
    """Post Form"""

    title = StringField("Title: ", [InputRequired()])
    content = TextAreaField("Content: ", [InputRequired()])
    tags = MultiCheckboxField("Tags: ", coerce=int)

    def set_choices(self):
        self.tags.choices = [(tag.id, tag.name)
                             for tag in Tag.query.all()]


class TagForm(FlaskForm):
    """Tag Form"""
    name = StringField("Tag: ", [InputRequired()])
