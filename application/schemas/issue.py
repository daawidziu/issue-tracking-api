from application import ma
from application.models import Issue


class IssueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Issue
        load_instance = True
        include_fk = True
