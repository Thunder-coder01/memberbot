import asyncio
import random
import threading

import aiohttp
from aiohttp import ClientSession

from modules.managers.worker import Worker


class Spammerworker:
    def __init__(
        self,
        Amount: int,
        Guild: int,
        Channel: int,
        Message: str,
        *args,
        **kwargs,
    ):
        self.guild = Guild
        self.channel = Channel
        self.amount = Amount
        self.message = Message
        self.api_url = f"https://discord.com/api/v9/channels/{self.channel}/messages"
        self.messages_sent = 0

    async def remove_token(self, token):
        with open("modules/managers/spammers.txt", "r") as file:
            lines = file.readlines()
        with open("modules/managers/spammers.txt", "w") as file:
            for line in lines:
                if line.strip() != token:
                    file.write(line)

    async def get_random_message(self):
        messages = open("modules/managers/messages.txt", "r").readlines()
        return random.choice(messages).strip()

    def load_proxies(self):
        proxies = []
        with open(self.proxies_file, "r") as file:
            for line in file:
                line = line.strip()
                parts = line.split(":")
                if len(parts) == 4:
                    username, password, domain, port = parts
                    proxy = f"http://{username}:{password}@{domain}:{port}"
                    proxies.append(proxy)
        return proxies

    async def __spammer__(self: "Spammerworker", token: str) -> None:
        try:
            p = Worker(
                Amount=self.amount,
                Guild=self.guild,
            )
            # await p.startspammer()
            tokens = open("modules/managers/spammers.txt", "r").readlines()
            for tok in tokens:
                tok = tok.strip()
                while self.messages_sent < self.amount:
                    message = await self.get_random_message()
                    async with ClientSession() as session:
                        headers = {
                            "Authorization": f"{token}",
                            "Content-Type": "application/json",
                        }
                        data = {
                            "content": self.message if self.message else message,
                            "tts": "false",
                            "flags": "0",
                            "mobile_network_type": "unknown",
                        }
                        async with session.post(
                            self.api_url,
                            headers=headers,
                            json=data,
                        ) as response:
                            re = await response.json()
                            if response.status == 200:
                                print(f"Message sent with token: {tok} ({re})")
                                self.messages_sent += 1
                            elif response.status == 401:
                                print(f"Token {tok} has missing access, removing it.")
                                await self.remove_token(tok)
                            else:
                                r = await response.json()
                                await self.remove_token(tok)
                                print(
                                    f"Failed to send message with token -> {tok} ({r})"
                                )
        except Exception as e:
            print(e)

    async def run(self):
        num_threads = 30
        tasks = []
        tokens = open("modules/managers/spammers.txt", "r").readlines()
        for token in tokens:
            t = token.rstri()
            await self.__spammer__(
                token=t,
            )
