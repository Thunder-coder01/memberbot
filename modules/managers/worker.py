import aiohttp
import asyncio
import random
from modules.client import Authorization


class Worker:
    def __init__(
        self: "Worker",
        Amount: int,
        Guild: int,
    ) -> None:
        self.guild = Guild
        self.endpoint: str = "https://canary.discord.com/api/v9"
        self.amount = Amount

    async def check_member(
        self,
        session,
        account_id,
        auth_token,
    ):
        url = f"{self.endpoint}/guilds/{self.guild}/members/{account_id}"

        headers = {
            "Authorization": f"Bot {Authorization.token}",
            "Content-Type": "application/json",
        }

        data = {
            "access_token": f"{auth_token}",
        }

        try:
            async with session.put(url, headers=headers, json=data) as response:
                data = await response.json()
                if response.status == 200:
                    print(f"Member {account_id} is already in the server. Skipping.")
                    return True
                elif response.status == 429:
                    retry_after = response.headers.get("Retry-After", 5)
                    print(f"Rate limited. Waiting for {retry_after} seconds.")
                    await asyncio.sleep(float(retry_after))
                elif response.status == 204:
                    print(f"{data}")
                else:
                    print(f"{data}")
        except Exception as e:
            print(f"Error while processing member {account_id}: {e}")

        return False

    async def startspammer(self):
        async with aiohttp.ClientSession() as session:
            with open("modules/managers/authtokens.txt", "r") as file:
                tokens = file.readlines()

            added_members = 0
            successful_attempts = 0

            while added_members < self.amount and tokens:
                for token in tokens:
                    token_parts = token.split(":")
                    account_id, idk, auth_token = (
                        token_parts[0],
                        token_parts[1],
                        token_parts[2],
                    )
                    failed = await self.check_member(session, account_id, idk)

                    if not failed:
                        added_members += 1
                        successful_attempts += 1
                    else:
                        tokens.remove(token)

                    if added_members >= self.amount:
                        break

                if successful_attempts < self.amount:
                    print(
                        f"Exhausted all tokens. Only {successful_attempts} members added."
                    )

    async def start(self):
        async with aiohttp.ClientSession() as session:
            with open("tokens.txt", "r") as file:
                tokens = file.readlines()

            added_members = 0
            successful_attempts = 0

            while added_members < self.amount and tokens:
                token = random.choice(tokens)
                token_parts = token.split(":")
                account_id, idk, auth_token = (
                    token_parts[0],
                    token_parts[1],
                    token_parts[2],
                )
                failed = await self.check_member(session, account_id, idk)

                if not failed:
                    added_members += 1
                    successful_attempts += 1
                else:
                    tokens.remove(token)

                if added_members >= self.amount:
                    break

            if successful_attempts < self.amount:
                print(
                    f"Exhausted all tokens. Only {successful_attempts} members added."
                )
