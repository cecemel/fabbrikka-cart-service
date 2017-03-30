# -*- coding: utf-8 -*-
"""
service tries to guess locale from user.
"""
import logging


def load_config(environment="DEBUG"):
    config = {}

    config["LOG_LEVEL"] = logging.INFO
    config["MU_SPARQL_ENDPOINT"] = "http://localhost:8890/sparql"
    config["MU_SPARQL_UPDATEPOINT"] = "http://localhost:8890/sparql"
    config["MU_APPLICATION_GRAPH"] = "http://mu.semte.ch/application"

    if not environment == "DEBUG":
        config["LOG_LEVEL"] = logging.INFO
        config["MU_SPARQL_ENDPOINT"] = "http://database:8890/sparql"
        config["MU_SPARQL_UPDATEPOINT"] = "http://database:8890/sparql"
        config["MU_APPLICATION_GRAPH"] = "http://mu.semte.ch/application"

    return config