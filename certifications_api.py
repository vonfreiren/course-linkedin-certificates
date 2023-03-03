def get_certifications(self, public_id=None, urn_id=None):

    res = self._fetch(f"/identity/profiles/{public_id or urn_id}/certifications", params={"count": 200, "start": 0})

    data = res.json()
    if data and "status" in data and data["status"] != 200:
        self.logger.info("request failed: {}".format(data["message"]))
        return {}

    certifications = data.get("elements", [])

    # massage [certifications] data
    certifications = data["elements"]

    return certifications
