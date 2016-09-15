import httplib2
import urllib
import urlparse


class AcumenClient:
    def __init__(self, config):
        self.config = config
        self.connection = httplib2.Http()

    def process(self, said):
        uri = urlparse.urljoin(
            self.config["acumen"]["service"],
            self.config["acumen"]["commands"]["voice"]
        )

        room = urllib.urlencode({"room": self.config["aural"]["room"]})

        resp, content = self.connection.request(
            uri=uri + "?" + room,
            body=said,
            method="POST",
        )

        assert resp.status == 200
