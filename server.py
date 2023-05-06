import platform
import json
import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta



link_2 = 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'


async def get_http_response(date):
    """Current function connecting to API and gather all data"""
    link = f'https://api.privatbank.ua/p24api/exchange_rates?date={date}'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{link}', ssl = False) as response:
                if response.status == 200:
                    html = await response.json()

                    print("Status:", response.status)
                    print("Content-type:", response.headers['content-type'])
                    print('Cookies: ', response.cookies)

                    # with open('data.json', 'w+') as j_file:
                    #     json.dump(result, j_file)
                    # print(f'Result : {html}')
                    print(link, type(html))
                else:
                    print(f'Error status: {response.status} for {link}')
                    html = None
    except aiohttp.ClientConnectorError as err:
        print(f'Connection erroe {link}, {str(err)}')

    return html



def parse_html_dict(html_list: list[dict]):
    result_list = []
    for html in html_list:
        date = html.get("date")
        date_dict = {}
        exchange_rate_list = html.get("exchangeRate")
        for exchange_dict in exchange_rate_list:

            base_currency = exchange_dict.get("baseCurrency")
            currency = exchange_dict.get("currency")
            sale_rate = exchange_dict.get("saleRateNB")
            purchase_rate_nb = exchange_dict.get("purchaseRateNB")

            if currency in ['EUR', 'USD']:
                date_dict.update({currency: {'sale':sale_rate, "purchase": purchase_rate_nb}})

        result_list.append({date : date_dict})

    return result_list


    # '03.11.2022': {
    #     'EUR': {
    #         'sale': 39.4,
    #         'purchase': 38.4

# async def get_date():
#     current_date = datetime.now().date()
#     format_date = current_date.strftime('%d-%m-%Y')
#
#     return format_date

async def get_timedelta(sys_num):
    current_datetime = datetime.now().date()
    data_list = []
    for i in range(1, sys_num+1):
        print(i)
        day_off = current_datetime - timedelta(days=i)
        print(day_off.strftime('%d.%m.%Y'))
        data_list.append(day_off.strftime('%d.%m.%Y'))

    print(f'get_timedelta returns: {data_list}')
    return data_list

async def main():
    sys_num = int(sys.argv[1])
    data_list = await get_timedelta(sys_num)
    results = []
    for i in data_list:

        # result = await asyncio.run(get_http_response(i))
        results.append(asyncio.create_task(get_http_response(i)))
        print(results)
    return await asyncio.gather(*results)

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = asyncio.run(main())

    day_data_dict = parse_html_dict(result)
    with open('data.json', 'w+') as j_file:
        json.dump(day_data_dict, j_file, indent=4)
