# transportadora.py

from sqlalchemy.orm import relationship

from app.extensions import db


class Transportadora(db.Model):
    __tablename__ = "transportadora"
    __table_args__ = {"schema": "deltruck"}
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False, unique=True)
    id_contacto = db.Column(
        db.Integer, db.ForeignKey("deltruck.contacto.id"), nullable=False
    )
    id_endereco = db.Column(
        db.Integer, db.ForeignKey("deltruck.endereco.id"), nullable=False
    )

    contacto = relationship(
        "Contacto",
        lazy="joined",
        passive_deletes=True,
        cascade="all, delete",
    )

    endereco = relationship(
        "Endereco", lazy="joined", passive_deletes=True, cascade="all, delete"
    )

    # 'cascade="all, delete"' remove pai e filhos associados. Usado em um-para-um.

    # 'cascade="all, delete-orphan"' remove pai, filhos associados e órfãos. Usado em um-para-muitos.
