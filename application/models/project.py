from sqlalchemy.orm import relationship

from application import db
from .base import BaseModel


class Project(BaseModel):

    # Project Information
    name = db.Column(db.String(256))
    description = db.Column(db.Text)
    # Relationships
    issues = relationship("Issue", back_populates="project")
