from sqlalchemy.orm import relationship

from application import db
from .base import BaseModel


class Comment(BaseModel):

    # Comment Information
    text = db.Column(db.Text)
    # Relationships
    issue_id = db.Column(db.Integer, db.ForeignKey("issue.id"))
    issue = relationship("Issue", back_populates="comments")
    author_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    author = relationship("Account")
