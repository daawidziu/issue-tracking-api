from flask_sqlalchemy import Pagination
from sqlalchemy.orm import declared_attr
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from application import db


class BaseModel(db.Model):
    __abstract__ = True

    # Base Information
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def get(cls, **kwargs) -> 'BaseModel':
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def filter_by(cls, limit=100, **filters) -> list['BaseModel']:
        return cls.query.filter_by(**filters).limit(limit).all()

    @classmethod
    def paginate(cls, page: int, per_page: int = 25, **kwargs) -> Pagination:
        return cls.query.filter_by(**kwargs).paginate(page, per_page)

    def update(self, new_data: dict) -> None:
        try:
            for key, value in new_data.items():
                setattr(self, key, value)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
        except IntegrityError as e:
            db.session.rollback()
            print(e)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)

    def __repr__(self) -> str:
        return str(self.__dict__)
