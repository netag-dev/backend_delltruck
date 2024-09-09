# utils/hateoasLinkGenerator.py

import logging

from flask import url_for


class HateoasLinkGenerator:
    def __init__(self, base_endpoints_dict, resource_id):
        """
        Inicializa o gerador de links HATEOAS com um dicionário de endpoints base.

        Args:
            base_endpoints_dict (dict): Um dicionário onde a chave é o nome do link e o valor é o
            nome do endpoint para gerar a URL.
        """
        self.base_endpoints_dict = base_endpoints_dict
        self.resource_id = resource_id

    def generate_response(self, resource_id: int):
        """
        Gera um dicionário de links HATEOAS para um recurso específico com base no ID fornecido.

        Args:
            resource_id (int): ID do recurso para o qual os links devem ser gerados.

        Returns:
            dict: Um dicionário de links, onde cada chave representa um identificador do link
            (como 'self', 'update', etc.) e cada valor é a URL correspondente.
        """
        links = {}
        logging.info("1: Generated HATEOAS link for %s", resource_id)

        for key, endpoint in self.base_endpoints_dict.items():
            logging.info(
                "2: Generated HATEOAS  endpoint forbase_endpoints_dict %s",
                self.base_endpoints_dict,
            )
            # url_for(endpoint, resource_id=resource_id, _external=True) -> '{BASE_API_URL}/views_name/resource_id'
            # Ex., url_for('user_api', resource_id=1, _external=True) -> '{BASE_API_URL}/users/1'
            links[key] = url_for(endpoint, resource_id=resource_id, _external=True)
            logging.info("Generated HATEOAS link for %s: %s", key, links[key])
        return links
