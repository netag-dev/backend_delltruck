# role.py

from sqlalchemy.orm import relationship

from app.extensions import db


class Role(db.Model):
    __tablename__ = "role"
    __table_args__ = {"schema": "deltruck"}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String, nullable=False, unique=True
    )  # ex., 'ADMIN', 'LOGISTA', 'USER', etc
    description = db.Column(
        db.Text,
    )

    # Relacionamento 1:N user
    # O atributo 'users' permite acessar todos os usuários associados a esta role.
    # 'back_populates' criar uma ligação bidirecional entre Role e User
    users = relationship("User", back_populates="role", lazy="select")

    def __repr__(self):
        return "id:{}, name:{}".format(self.id, self.name)
