# userService.py

import logging

from sqlalchemy.exc import IntegrityError

from app.utils import SingletonMeta
from app.security.securityConfig import SecurityConfig
from app.exceptions import EntityUniqueViolationException, EntityNotFoundException

from .user import User
from .userRepository import UserRepository


class UserService(metaclass=SingletonMeta):
    def __init__(self):
        self.user_repository = UserRepository()

    def create(self, user: User):
        try:
            logging.debug("0: UserService().create()")
            # Criptografar a password antes de salvar
            user.password = SecurityConfig.hash_password(user.password)

            logging.debug("1: UserService().create()")
            user_criado = self.user_repository.save(user)

            logging.info("2: UserService.create()")
            return user_criado

        except IntegrityError as ex:
            if "unique constraint" in str(ex.orig):
                logging.error("IntegrityError %s", ex.orig)
                raise EntityUniqueViolationException(ex.orig)

        except Exception as ex:
            logging.error("%s", ex)

    def get_all_except_role_user_and_root(self):
        return self.user_repository.find_all_except_role_user_and_root()

    def get_all(self):
        return self.user_repository.find_all()

    def get_by_id(self, user_id):
        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise EntityNotFoundException(f"Usuário com id {user_id} não encontrado.")
        return user

    def get_user_by_user_email(self, user_email):
        user = self.user_repository.find_user_by_user_email(user_email)
        if user is None:
            raise EntityNotFoundException(
                f"Usuário com user_email: {user_email} não encontrado."
            )
        return user

    def update(self, novo_user, user_id):
        updated = self.user_repository.update(novo_user, user_id)
        if updated is None:
            raise EntityNotFoundException(f"Usuário com id {user_id} não encontrado.")
        return updated

    def update_partial(self, user_fields, id):
        return self.user_repository.update_partial(user_fields, id)
