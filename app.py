__author__ = "Jeremy Nelson"
__version__ = "0.0.1"

import urllib.parse
import lxml.etree as etree
import responder

NAMESPACES = {"lcf": "http://ns.bic.org.uk/lcf/1.0"}

api = responder.API()

@api.route("/loans/")
@api.route("/loans/{identifier}")
async def loans(req, resp, identifier=None):
    patron, info = None, None
    
    if not identifier and req.method.startswith("post"):
        if req.headers["content-type"].endswith("x-www-form-urlencoded"):
            raw_queries = await req.content
            queries = urllib.parse.parse_qs(raw_queries)
            loan = etree.Element("loan", nsmap=NAMESPACES)
        else:
            raw_xml = await req.content
            loan_xml = etree.XML(raw_xml)

    resp.text = api.template('loans.xml', 
        patron=patron)
        

@api.route("/")
async def fasten_home(req, resp):
    resp.text = f"{__version__} of NISO FASTEN Server"

if __name__ == '__main__':
    api.run()
