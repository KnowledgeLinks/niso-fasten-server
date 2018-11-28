__author__ = "Jeremy Nelson"
__version__ = "0.0.1"

import responder

api = responder.API()

@api.route("/")
async def fasten_home(req, resp):
    resp.text = f"{__version__} of NISO FASTEN Server"

if __name__ == '__main__':
    api.run()
