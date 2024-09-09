# permission.py

from sqlalchemy.orm import relationship

from app.extensions import db


class Permission(db.Model):
    __tablename__ = "permission"
    __table_args__ = {"schema": "deltruck"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String, nullable=False, unique=True
    )  # ex., 'create', 'edit', 'view', 'archive'

    def __repr__(self):
        return "id:{}, name:{}".format(self.id, self.name)
