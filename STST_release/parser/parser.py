# https://translated.turbopages.org/proxy_u/en-ru.ru.c56960ed-68b2dcfe-7b81abbd-74722d776562/https/stackoverflow.com/questions/71764301/how-to-bypass-cloudflare-with-python-on-get-requests
import requests.utils
import cloudscraper
from bs4 import BeautifulSoup


urls = (
    'https://scrap.tf/buy/items',
    'https://scrap.tf/buy/hats'
)
headersSessionList = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    f'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'Cache-Control': 'max-age=0',
    # 'Cookie': 'scraptf=1an0eoevpak8i12utnb38t7dmo; _lr_env_src_ats=false; panoramaId_expiry=1756913120500; panoramaId=3e302021e3f0ec02100f81727db4185ca02c4f030fcb2f78e25e83529ad1fae8; nitro-uid=%7B%22TDID%22%3A%22f385fca7-9978-496a-8117-243073b7ab29%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222025-08-27T15%3A25%3A20%22%7D; nitro-uid_cst=V0fMHQ%3D%3D; ncmp.domain=scrap.tf; _lr_sampling_rate=100; _lr_geo_location_state=SVE; _lr_geo_location=RU; _gid=GA1.2.192275571.1756488810; _ga=GA1.1.1393398107.1756309693; _cc_id=3774124d748c0815c052c0532037a485; _lr_retry_request=true; cf_clearance=PEOF.OhV.Y_JoD7KKuVjdAsKsNLIe2q6Con7GRyODCw-1756550714-1.2.1.1-7RMfufMsobhhUAhetqzePhtfSPkjdZeKA4Mw6CNZS4S3x63uUFT4RYTyP9rB6Cn25GCieLujlO_IcIR1TNT51_KQAbYUrYkX6fmwsoVGPxeMgDyWjvoqEh.JwmKTFu7uZsaLG5Eg.RdFAbFQhWfNwRI47HGcsNXKdPTOgfMpo8323B0CB_0uzXDXDBhIRW.Lwn3SaKEt0fruh_6tvvGPykRak0T2lYa4CeGOuiaY0DU; _ga_CRS9KN52XK=GS2.1.s1756549830$o16$g1$t1756550725$j46$l0$h0; cto_bundle=EleQh19aTyUyQjlOViUyQmUwUkJPJTJGeUZOS2xhS3NrQmc3TVpITFJxUUh5RHdDOXJ2JTJCTnlpSWZ1NU5sTHRRRSUyQm1JdG02c1cyWUdEWmdqQ0NCdG1McFJvdnA0NWlkOG05U09JczdZaEppZzJmOGZRQ1NYQjR5eTg5M29nTnE5WHZ1WVQ2dDdkZ29URVNxenp6Zm9hanFnUE9rbnhiU3hBJTNEJTNE; cto_bidid=0RovLF9UTkRHWUw3cExJOVglMkI0SlJ3Uml6YTFlMkVnTTRaQlZxZTZtRU14bFpBUm1EazJleTJac3dZNTZtZlIwTU5sTkRkckJ0VXBaelFKQkRIRyUyQjNNMVZkVDVzTFRQNkcyVVVCdlRPazhieUlta0ElM0Q; cto_dna_bundle=pEVb3l9aTyUyQjlOViUyQmUwUkJPJTJGeUZOS2xhS3NzUXFNUWtOYkNVdkluNzVkdnVXQlMzVGw3NThQbkpuVzNzVlY4SGpxZTFWNlJVbFJyeSUyQnppRGF5ZVFMREdDJTJGQ2clM0QlM0Q',
    'Priority': 'u=0, i',
    'Referer': 'https://scrap.tf/',
    'Sec-Ch-Ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
}
cookiesSessionList = {
    '_cc_id': '3774124d748c0815c052c0532037a485',
    '_ga': 'GA1.1.1393398107.1756309693',
    '_ga_CRS9KN52XK': 'GS2.1.s1756537934$o15$g1$t1756541987$j59$l0$h0',
    '_gid': 'GA1.2.192275571.1756488810',
    '_lr_env_src_ats': 'false',
    '_lr_geo_location': 'RU',
    '_lr_geo_location_state': 'SVE',
    '_lr_retry_request': 'true',
    '_lr_sampling_rate': '100',
    'cf_clearance': 'BlRM3ry1zvhWxX6GODY.QeDGGrRWgGTvwLgkjTbS5Ck-1756541988-1.2.1.1-mHt16jOcPaHBBbcwWVKBRk827S8HXiHg1o9aLqv8_Td.9y5HgyQqNao4TvREliq8K0TSCLauN54kbCvH1G6Bv16PyH8IFANrmtZjiH9iEWmhG7I7YbwNsDtbLH52oS_v_cThMv8qH5Z8Jfa8ljOsZrCihPkNqIAynZmTG1wc3Fvt8EBlNUgTqan19KrMhj7no5.9kYQnorHn2ZAFrcCAhKd7.53NKgeoJIEQbcg4jcw',
    'cto_bidid': 'tjBJrF9UTkRHWUw3cExJOVglMkI0SlJ3Uml6YTFlMkVnTTRaQlZxZTZtRU14bFpBUm1EazJleTJac3dZNTZtZlIwTU5sTkRkckJ0VXBaelFKQkRIRyUyQjNNMVZkVDBpMXlhU2YlMkYlMkJ4RWN6bXNrRFJab0lJJTNE',
    'cto_bundle': 'Jfulll9aTyUyQjlOViUyQmUwUkJPJTJGeUZOS2xhS3NuNGVQNWdsWCUyRlRmV2dDJTJCQjRlelc2VnN3MHZKJTJGaUs0QmpaZ2JVNUdWdkc1WUwlMkJQRTZyUzNZMHRuJTJGcXB3UlpJR0RDcXNQWHd4bkhmS1c0R012dTNUTExSYzBRaHRZdGM1eTNzM0xKTCUyQlA5bm1rOUxlOE1RWFVCZTNjZHBjSldBemclM0QlM0Q',
    'cto_dna_bundle': 'qaP3Vl9aTyUyQjlOViUyQmUwUkJPJTJGeUZOS2xhS3NzUXFNUWtOYkNVdkluNzVkdnVXQlMzVGw3NThQbkpuVzNzVlY4SGpxZTFWNUsxU0MydzRwblA4ZmhKTmElMkZYMUxRJTNEJTNE',
    'ncmp.domain': 'scrap.tf',
    'nitro-uid': '%7B%22TDID%22%3A%22f385fca7-9978-496a-8117-243073b7ab29%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222025-08-27T15%3A25%3A20%22%7D',
    'nitro-uid_cst': 'V0fMHQ%3D%3D',
    'panoramaId': '3e302021e3f0ec02100f81727db4185ca02c4f030fcb2f78e25e83529ad1fae8',
    'panoramaId_expiry': '1756913120500',
    'scraptf': 'fja23j26ine1tptlb4s3mq2chi'
}

def getHtmlPage(url: str) -> str:
    session = requests.Session()
    session.headers = headersSessionList
    requests.utils.add_dict_to_cookiejar(session.cookies, cookiesSessionList)
    scraper = cloudscraper.create_scraper(session)
    response = scraper.get(url)
    return response.text

def clearItemName(itemName: str) -> str:
    stringGarbage = ('<span class=', '</span>')
    if (stringGarbage[0] in itemName) or (stringGarbage[1] in itemName):
        itemName = itemName[itemName.find('>') + 1:itemName.rfind('<')]
    return itemName

def getPageItemsInfo(url: str) -> list:
    htmlPage = getHtmlPage(url)
    itemsInfo = []
    soup = BeautifulSoup(htmlPage, 'html.parser')
    soup = soup.find('div', id='buy-container')
    for itemContainer in soup.find_all('div', class_="items-container"):
        # Getting an array of item's tags
        for item in itemContainer.find_all(recursive=False):
            value = item.find('div', class_="item-value-indicator").text
            itemInfo = {'name': clearItemName(item['data-title']), 'amount': item['data-num-available'], 'value': value}
            itemsInfo.append(itemInfo)
    return itemsInfo

def getAllItemsInfo() -> dict:
    itemsInfo = {}
    for url in urls:
        itemsInfo[url] = getPageItemsInfo(url)
        # itemsInfo = itemsInfo + getPageItemsInfo(url)
    return itemsInfo
