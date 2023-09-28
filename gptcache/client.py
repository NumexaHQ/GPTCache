import asyncio
import json

from gptcache.utils import import_httpx

import_httpx()

import httpx  # pylint: disable=C0413


_CLIENT_HEADER = {"Content-Type": "application/json", "Accept": "application/json"}


class Client:
    """GPTCache client to send requests to GPTCache server.

    :param uri: the uri leads to the server, defaults to "http://localhost:8000".
    :type uri: str

    Example:
        .. code-block:: python

            from gptcache import client

            client = Client(uri="http://localhost:8000")
            client.put("Hi", "Hi back")
            ans = client.get("Hi")
    """

    def __init__(self, uri: str = "http://localhost:8000"):
        self._uri = uri

    async def _put(self, question: str, answer: str, user_id: int):
        async with httpx.AsyncClient() as client:
            data = {
                "prompt": question,
                "answer": answer,
                "user_id": user_id
            }

            response = await client.post(
                f"{self._uri}/put", headers=_CLIENT_HEADER, data=json.dumps(data)
            )

        return response.status_code

    async def _get(self, question: str, user_id: int):
        async with httpx.AsyncClient() as client:
            data = {
                "prompt": question,
                "user_id": user_id
            }

            response = await client.post(
                f"{self._uri}/get", headers=_CLIENT_HEADER, data=json.dumps(data)
            )

        return response.json().get("answer")

    def put(self, question: str, answer: str, user_id: int):
        """
        :param question: the question to be put.
        :type question: str
        :param answer: the answer to the question to be put.
        :type answer: str
        :param user_id: the user_id to be put.
        :type user_id: str
        :return: status code.
        """
        return asyncio.run(self._put(question, answer, user_id))

    def get(self, question: str, user_id: int):
        """
        :param question: the question to get an answer.
        :type question: str
        :param user_id: the user_id to get an answer.
        :type user_id: int
        :return: answer to the question.
        """
        return asyncio.run(self._get(question, user_id))
