from flask import Flask, request, jsonify
import os, sys
import helpers, escape_helpers
import logging
import config

from rdflib.namespace import Namespace

##############
# INIT CONFIG
##############
CONFIG = config.load_config(os.environ.get('ENVIRONMENT', "DEBUG"))
app = Flask(__name__)

handler = logging.StreamHandler(stream=sys.stderr)
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
# API
#################
@app.route('/shopping-carts', methods=["PATCH"])
def associate_cart():
    """
    associates cart with mu-session
    :return:
    """
    # validates
    data = request.get_json(force=True)['data']

    errors = [helpers.validate_resource_type("shopping-carts", data), helpers.validate_json_api_content_type(request)]
    if any(errors):
        return next(e for e in errors if e)

    cart_id = data.get("id", None)

    if not cart_id:
        return helpers.error("CART ID missing")

    # get session id in the request
    session_id = helpers.session_id_header(request)

    if not session_id:
        return helpers.error("MU_SESSION_ID missing")

    # now fetch the cart
    query = """SELECT ?cart
    WHERE{
        GRAPH <http://mu.semte.ch/application> {
            ?cart <http://mu.semte.ch/vocabularies/core/uuid> %s
            }
        }
    """ % escape_helpers.sparql_escape(cart_id)

    carts = helpers.query(app.logger, sparql_wrapper["sparql_query"], query).get('results', []).get('bindings')
    if not len(carts) == 1:
        return helpers.error("no/too many cart(s) found for {}".format(cart_id))

    cart_uri = carts[0]['cart']['value']

    # update the cart with session
    query = """
        PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>
            INSERT DATA
            {
                GRAPH <http://mu.semte.ch/application> {
                <%s> ext:ownerSession <%s>.
                }
            }
    """ % (cart_uri, session_id)

    helpers.query(app.logger, sparql_wrapper["sparql_update"], query)

    return "", 204


@app.route('/shopping-carts')
def return_associate_cart():
    # get session id in the request
    session_id = helpers.session_id_header(request)

    if not session_id:
        return helpers.error("MU_SESSION_ID missing")

    # now fetch the carts uid
    query = """PREFIX mu: <http://mu.semte.ch/vocabularies/core/>
    SELECT ?uid
    WHERE {
        GRAPH <http://mu.semte.ch/application> {
        ?uri <http://mu.semte.ch/vocabularies/ext/ownerSession> <%s>.
        ?uri mu:uuid ?uid
        }
    }
    """ % session_id

    uids = helpers.query(app.logger, sparql_wrapper["sparql_query"], query).get('results', []).get('bindings')
    return jsonify([e["uid"]["value"] for e in uids]), 200


#######################
## Start Application ##
#######################
if __name__ == '__main__':
    app.logger.info("---cart-service is starting")
    app.run(host='0.0.0.0', port=80, debug=True)