from sqlalchemy.orm import relationship

from application import db
from .base import BaseModel


class Issue(BaseModel):

    # Project Information
    name = db.Column(db.String(256))
    status = db.Column(db.String(64))
    description = db.Column(db.Text)
    # Relationships
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = relationship("Project", back_populates="issues")
    comments = relationship("Comment", back_populates="issue")
