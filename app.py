__author__ = "Jeremy Nelson"
__version__ = "0.0.1"

import urllib.parse
import lxml.etree as etree
import click
import responder

NAMESPACES = {"ncip": "http://www.niso.org/2008/ncip"}

api = responder.API()

@api.route("/item/{message}")
async def request_item(req, resp, message=None):
    if message is None:
        resp.status_code = api.status_codes.HTTP_400
        resp.text = "Missing message"
    raw_request = await req.content
    try:
        message_xml = etree.XML(raw_request)
    except etree.XMLSyntaxError:
        raw_queries = await req.content
        queries = urllib.parse.parse_qs(raw_queries)    
        if message.startswith("RequestItem"):
            # Returns RequestItemResponse
            message_xml = api.template("RequestItem.xml", **queries)
        elif message.startswith("CancelRequestItem"):
            # Returns Success or Failure
            message_xml = api.template("CancelRequestItem.xml", **queries)
        elif message.startswith("CheckOutItem"):
            # Returns CheckOutItemResponse or ItemCheckoutOut message
            message_xml = api.template("CheckOutItemResponse.xml")
        elif message.startswith("CheckInItem"):
            # Returns Success or Failure
            pass
        elif message.startswith("RenewItem"):
            # Returns Success or Failure
            pass
        elif message.startswith("LookupItem"):
            # Returns LookupItem Response
            pass
        else:
            resp.status_code = api.status_codes.HTTP_400
            resp.text = f"Unknown {message}"

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
