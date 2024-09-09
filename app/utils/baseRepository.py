# utils/baseRepository.py

import logging

from app.extensions import db
from .singletonMeta import SingletonMeta


class BaseRepository(metaclass=SingletonMeta):
    """Classe base para operações CRUD usando SQLAlchemy."""

    def __init__(self, model):
        self.model = model

    def save(self, entity):
        """
        Salva uma ou mais entidades no banco de dados.

        Args:
        - entities (list or db.Model): Entidade ou lista de entidades a serem salvas.

        Returns:
        - list or db.Model: A(s) entidade(s) salva(s).
        """
        if isinstance(entity, list):
            db.session.add_all(entity)
        else:
            db.session.add(entity)
        db.session.commit()
        return entity

    def find_all(self):
        """
        Recupera todas as entidades do modelo.

        Returns:
        - list: Lista de todas as entidades.
        """
        return db.session.query(self.model).all()

    def find_by_id(self, id: int):
        """
        Busca uma entidade pelo seu ID.

        Args:
        - id (int): O identificador da entidade.

        Returns:
        - db.Model: A entidade correspondente ao ID fornecido, ou None se não encontrada.
        """
        return db.session.get(self.model, id)

    def update(self, new_entity, id):
        """Sincroniza a nova entidade com a entidade existente na sessão.

        Args:
            new_entity: A nova entidade que deve ser mesclada ou adicionada.
            id: O ID da entidade existente que deve ser mesclada com a nova entidade.
                Caso a entidade com o ID não seja encontrada, um novo registro será criado.

        Returns:
            A entidade mesclada ou a nova entidade adicionada.
        """

        # Carrega a entidade existente na sessão, se houver
        existing_entity = self.find_by_id(id)

        if existing_entity:
            # Mescla a nova entidade com a entidade existente na sessão
            merged_entity = db.session.merge(new_entity)
            db.session.commit()
            return merged_entity
        else:
            return None

    def update_partial(self, entity_fields, id):
        """"""
        rows_updated = self.model.query.filter_by(id=id).update(entity_fields)
        db.session.commit()
        return rows_updated

    def delete(self, id):
        entity = self.find_by_id(id)
        db.session.delete(entity)
        db.session.commit()

    def delete_all(self, id):
        self.model.query.filter_by(id=id).delete()
        db.session.commit()

    @staticmethod
    def transactional(func):
        """Envolve a execução de uma função em uma transação.

        Args:
        - func (callable): A função a ser executada dentro da transação.

        Returns:
        - O resultado da função executada.

        Raises:
        - Exception: Lança a exceção capturada após rollback.
        """
        try:
            result = func()
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e
