import httpx

class Remnawave:
    def __init__(self, panel_url: str, token: str):
        self.panel_url = panel_url
        self.token = token

        self.client = httpx.AsyncClient(headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        })

    async def _get(self, url: str):
        r = await self.client.get(self.panel_url + url)
        return r.json()["response"]

    async def _post(self, url: str, data: dict = None):
        r = await self.client.post(self.panel_url + url, json=data)
        return r.json()["response"]

    async def _patch(self, url: str, data: dict = None):
        r = await self.client.patch(self.panel_url + url, json=data)
        return r.json()["response"]

    async def inbound(self, tag: str):
        inbounds = await self._get("/inbounds")
        for x in inbounds:
            if x["tag"] == tag:
                return x["uuid"]

    async def get(self, username: str = None, uuid: str = None):
        if username:
            user = await self._get("/users/by-username/" + username)
        else:
            user = await self._get("/users/by-short-uuid/" + uuid)
        return user

    async def create(self,
                     username: str,
                     traffic_limit: int,
                     traffic_strategy: str,
                     inbounds: list,
                     expire: str,
                     description: str = None):
        user = await self._post("/users", {
            "username": username,
            "trafficLimitBytes": traffic_limit,
            "trafficLimitStrategy": traffic_strategy,
            "activeUserInbounds": [await self.inbound(x) for x in inbounds],
            "expireAt": expire,
            "description": description or ""
        })
        return user

    async def edit(self,
                   username: str,
                   traffic_limit: int = None,
                   traffic_strategy: str = None,
                   inbounds: list = None,
                   expire: str = None,
                   description: str = None):
        user = await self.get(username)
        data = {
            "uuid": user["uuid"]
        }
        if traffic_limit:
            data.setdefault("trafficLimitBytes", traffic_limit)
        if traffic_strategy:
            data.setdefault("trafficLimitStrategy", traffic_strategy)
        if inbounds:
            data.setdefault("activeUserInbounds", [await self.inbound(x) for x in inbounds])
        if expire:
            data.setdefault("expireAt", expire)
        if description:
            data.setdefault("description", description)
        return await self._patch("/users/", data)
