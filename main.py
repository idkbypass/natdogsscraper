import requests
import time
from colorama import Fore, Style, init

init(autoreset=True)

def make_api_calls(start_block, end_block):
    base_url = "https://dogechain.info/api/v1/block/{blocknumber}"
    webhook_url = "https://discord.com/api/webhooks/..."

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Dnt": "1",
        "Referer": "https://natdogs.gitbook.io/natdogs-dogecoin-digital-matter-theory/how-to-store-find-mint-and-verify-natdogs",
        "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    for block_number in range(start_block, end_block + 1):
        print(f"Scanning Block: {block_number}")
        url = base_url.format(blocknumber=block_number)
        response = requests.get(url, headers=headers)

        try:
            response.raise_for_status()
            data = response.json()
            bits_field = data.get("block", {}).get("bits", "")
            hash_field = data.get("block", {}).get("hash", "")
            height = data.get("block", {}).get("height", "")

            if "3b" in bits_field and "42" in hash_field:
                print(
                    f"Height: {height}, Hash: {Fore.BLUE}{hash_field}{Style.RESET_ALL}, Bits: {Fore.BLUE}{bits_field}{Style.RESET_ALL}"
                )

                send_discord_webhook(height, hash_field, bits_field, webhook_url)

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")

def send_discord_webhook(height, hash_field, bits_field, webhook_url):
    embed_data = {
        "title": "Found a NatDog",
        "fields": [
            {"name": "Block Height", "value": height},
            {"name": "Hash", "value": hash_field},
            {"name": "Bits", "value": bits_field}
        ],
        "footer": {"text": "NatDog scraper by @valeesec"},
        "color": 0x0000
    }

    webhook_data = {
        "embeds": [embed_data]
    }

    response = requests.post(webhook_url, json=webhook_data)

    if response.status_code != 204:
        print(f"Failed to send Discord webhook. Status code: {response.status_code}")

start_block = 61000
end_block = 830000

make_api_calls(start_block, end_block)
