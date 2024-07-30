import asyncio
import json
import random
import re
import string
import sys

import httpx


def generate_random_string(length: int):
    """生成指定长度的随机字符串"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://klpbbs.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 '
                  'Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'operation': 'qiandao',
    'format': 'button',
    'formhash': '',
    'inajax': '1',
    'ajaxtarget': 'midaben_sign',
}

cookies = []


def validate():
    global cookies
    if not cookies:
        print("Please input cookies")
        sys.exit(-1)


async def main():
    global cookies

    cnt = 1

    for cookie in cookies:
        print(f"Start Sign {cnt}")

        print("Get Formhash")
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://klpbbs.com", cookies=cookie, headers=headers)
            formhash = re.search(r'formhash=([a-f0-9]+)', resp.text).group(1) if re.search(r'formhash=([a-f0-9]+)',
                                                                                           resp.text) else None

        if formhash is None:
            print("Can not get formhash")
            sys.exit(-1)

        print("Get formhash successfully")
        params['formhash'] = formhash

        print("Sign")

        async with httpx.AsyncClient() as client:
            resp = await client.get('https://klpbbs.com/k_misign-sign.html', params=params, cookies=cookie,
                                    headers=headers)

        print("Response:\n", resp.text)
        print(f"Sign {cnt} Successfully!")

        cnt += 1


if __name__ == '__main__':
    with open("config.json", 'r', encoding="utf-8") as f:
        cookies = json.loads(f.read())["cookies"]
    validate()
    asyncio.run(main())
