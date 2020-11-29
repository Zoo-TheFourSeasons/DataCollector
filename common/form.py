from wtforms import validators
from wtforms import StringField
from flask_wtf import FlaskForm


class IVsForm(FlaskForm):
    ids = StringField('ids', [validators.required(message='ids is required')])
    versions = StringField('versions', [validators.required(message='versions is required')])

    def get_ivs(self):
        ids = self.ids.data.split(',')
        versions = self.versions.data.split(',')
        versions = [int(version) for version in versions]
        zipped = zip(ids, versions)
        return zipped

    def get_ids(self):
        return self.ids.data.split(',')
