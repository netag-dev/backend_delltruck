import secrets
from pathlib import Path
from dotenv import load_dotenv, set_key
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os


def generate_symmetric_key(length=32):
    """Gera uma chave simétrica aleatória.
    - 'secrets.token_hex': gera chaves strings hexadecimais, útil para configurações e tokens.
    - 'os.urandom()': gera bytes brutos para criptografia (ex.: AES).
    """
    return secrets.token_hex(length)


def generate_asymmetric_keys():
    """Gera chaves RSA privadas e públicas."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    return private_pem, public_pem


def update_env_file(file_path, symmetric_key, private_key, public_key):
    """Atualiza as chaves no arquivo .env."""
    # Carregar as variáveis de ambiente do arquivo .env
    load_dotenv(dotenv_path=file_path)

    # Atualizar ou adicionar as chaves no arquivo .env
    set_key(file_path, "SECRET_KEY", symmetric_key, )
    set_key(file_path, "JWT_PRIVATE_KEY", private_key)
    set_key(file_path, "JWT_PUBLIC_KEY", public_key)


if __name__ == "__main__":
    # Caminho para o arquivo .env
    env_file_path = Path(__file__).resolve().parent.parent / '.env'

    # Gerar chaves
    symmetric_key = generate_symmetric_key()
    private_key, public_key = generate_asymmetric_keys()

    # Atualizar as chaves no arquivo .env
    update_env_file(env_file_path, symmetric_key, private_key, public_key)

    print("Chaves geradas e atualizadas no arquivo .env com sucesso.")
