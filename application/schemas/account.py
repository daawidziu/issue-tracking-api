from application import ma
from application.models import Account


class AccountPublicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Account

    created_at = ma.auto_field()
    email = ma.auto_field()
    public_id = ma.auto_field()
    role = ma.auto_field()


class AccountPrivateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Account
