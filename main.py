from flask import Flask, request, jsonify
import os, sys
import helpers
import logging
import config

from rdflib.namespace import Namespace

##############
# INIT CONFIG
##############
CONFIG = config.load_config(os.environ.get('ENVIRONMENT', "DEBUG"))
app = Flask(__name__)

handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(CONFIG["LOG_LEVEL"])
app.logger.addHandler(handler)

# vocabularies
mu = Namespace('http://mu.semte.ch/vocabularies/')
mu_core = Namespace('http://mu.semte.ch/vocabularies/core/')
mu_ext = Namespace('http://mu.semte.ch/vocabularies/ext/')

graph = CONFIG['MU_APPLICATION_GRAPH']

# sparql wrapper
sparql_wrapper = helpers.init_sparql_wrapper(CONFIG)


#################
# Example method
#################
@app.route('/carts', methods=["POST"])
def associate_cart():
    """
    associates cart with mu-session
    :return:
    """
    session_id = helpers.session_id_header(request)
    return jsonify(session_id)
    # q = " SELECT *"
    # q += " WHERE{"
    # q += "   GRAPH <http://mu.semte.ch/application> {"
    # q += "     ?s ?p ?o"
    # q += "   }"
    # q += " }"
    # return jsonify(helpers.query(app.logger, sparql_wrapper["sparql_query"], q))


@app.route('/carts')
def return_associate_cart():
    print("todo")

#######################
## Start Application ##
#######################
if __name__ == '__main__':
    app.logger.info("---cart-service is starting")
    app.run(host='0.0.0.0', port=8091)