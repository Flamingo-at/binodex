import asyncio
import aiohttp

from re import findall
from loguru import logger
from aiohttp import ClientSession
from random import choice, randint
from aiohttp_proxy import ProxyConnector


def random_tor_proxy():
    proxy_auth = str(randint(1, 0x7fffffff)) + ':' + \
        str(randint(1, 0x7fffffff))
    proxies = f'socks5://{proxy_auth}@localhost:' + str(choice(tor_ports))
    return(proxies)


def get_connector():
    connector = ProxyConnector.from_url(random_tor_proxy())
    return(connector)


async def sending_captcha(client: ClientSession):
    try:
        response = await client.get(f'http://api.captcha.guru/in.php?key={user_key}&method=userrecaptcha \
            &googlekey=6LdYnqcjAAAAAAnZtwWb46q3wHJKm4lj2-VTyJw6&pageurl=https://binodex.space/')
        data = await response.text()
        if 'ERROR' in data:
            logger.error(print(data))
            return(await sending_captcha(client))
        id = data[3:]
        return(await solving_captcha(client, id))
    except:
        raise Exception()


async def solving_captcha(client: ClientSession, id: str):
    for i in range(100):
        try:
            response = await client.get(f'http://api.captcha.guru/res.php?key={user_key}&action=get&id={id}')
            data = await response.text()
            if 'ERROR' in data:
                logger.error(print(data))
                raise Exception()
            elif 'OK' in data:
                return(data[3:])
            return(await solving_captcha(client, id))
        except:
            raise Exception()
    raise Exception()


async def create_email(client: ClientSession):
    try:
        response = await client.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        email = (await response.json())[0]
        return email
    except:
        logger.error("Failed to create email")
        await asyncio.sleep(1)
        return await create_email(client)


async def check_email(client: ClientSession, login: str, domain: str, count: int):
    try:
        response = await client.get('https://www.1secmail.com/api/v1/?action=getMessages&'
                                    f'login={login}&domain={domain}')
        email_id = (await response.json())[0]['id']
        return email_id
    except:
        while count < 30:
            count += 1
            await asyncio.sleep(1)
            return await check_email(client, login, domain, count)
        logger.error('Emails not found')
        raise Exception()


async def get_code(client: ClientSession, login: str, domain: str, email_id):
    try:
        response = await client.get('https://www.1secmail.com/api/v1/?action=readMessage&'
                                    f'login={login}&domain={domain}&id={email_id}')
        data = await response.text()
        code = findall(r"\w{32}", data)[0]
        return code
    except:
        logger.error('Failed to get code')
        raise Exception()


async def get_id(client: ClientSession):
    response = await client.get(f'https://binodex.space/?ref={ref}',
                                allow_redirects=False)
    data = str(response.headers)
    index = data.index('PHPSESSID=')
    return data[index:index + 42]


async def register(client: ClientSession, email: str, id: str):
    response = await client.post('https://binodex.space/core.php',
                                 data={
                                     'signup': '1',
                                     'g': await sending_captcha(client),
                                     'login': 'undefined',
                                     'password': email.split('@')[0],
                                     'password1': email.split('@')[0],
                                     'email': email
                                 }, headers={'cookie': id})
    if await response.text() != '':
        raise Exception()


async def worker():
    while True:
        try:
            async with aiohttp.ClientSession(connector=get_connector()) as client:

                logger.info('Create email')
                email = await create_email(client)

                logger.info('Get id')
                id = await get_id(client)

                logger.info('Registration')
                await register(client, email, id)

        except Exception:
            logger.error("Error\n")
        else:
            with open('registered.txt', 'a', encoding='utf-8') as file:
                file.write(f'{email}:{email.split("@")[0]}\n')
            logger.success('Successfully\n')

        await asyncio.sleep(delay)


async def main():
    tasks = [asyncio.create_task(worker()) for _ in range(threads)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    tor_ports = [9150]

    print("Bot Binodex @flamingoat\n")

    ref = input('Referral code: ')
    user_key = input('Captcha key: ')
    delay = int(input('Delay(sec): '))
    threads = int(input('Threads: '))

    asyncio.run(main())