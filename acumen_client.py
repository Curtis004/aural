import httplib2
from urllib import parse


class AcumenClient:
    def __init__(self, config):
        self.config = config
        self.connection = httplib2.Http()

    def process(self, said):
        uri = parse.urljoin(
            self.config["acumen"]["service"],
            self.config["acumen"]["commands"]["voice"]
        )

        room = parse.urlencode({"room": self.config["aural"]["room"]})

        resp, content = self.connection.request(
            uri=uri + "?" + room,
            body=said,
            method="POST",
        )

        assert resp.status == 200
