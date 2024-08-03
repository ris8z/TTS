import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import os

def get_downloadlink(url: str) -> str:
    cookies = {
        '_ga': 'GA1.1.1979845980.1722522379',
        'FCCDCF': '%5Bnull%2Cnull%2Cnull%2C%5B%22CQCrCAAQCrCAAEsACBENA_FoAP_gAEPgACgAINJB7C7FbSFCwH5zaLsAMAhHRsAAQoQAAASBAmABQAKQIAQCgkAQFASgBAACAAAAICZBIQIECAAACUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAAAAEAAIAAAAEAAAmAgAAIIACAAAhAAAAAAAAAAAAAAAAgCAAAAAAAAAAAAAAAAAAQOhSD2F2K2kKFkPCmwXYAYBCujYAAhQgAAAkCBMACgAUgQAgFJIAgCIFAAAAAAAAAQEiCQAAQABAAEIACgAAAAAAIAAAAAAAQQAABAAIAAAAAAAAEAAAAIAAQAAAAIAABEhCAAQQAEAAAAAAAQAAAAAAAAAAABAAA%22%2C%222~70.89.93.108.122.149.196.236.259.311.313.323.358.415.449.486.494.495.540.574.609.827.864.981.1029.1048.1051.1095.1097.1126.1205.1276.1301.1365.1415.1423.1449.1514.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.2072.2253.2299.2357.2373.2415.2506.2526.2568.2571.2575.2624.2677~dv.%22%2C%2212586B38-67DA-45A8-B1EE-D7E059C7935F%22%5D%5D',
        'FCNEC': '%5B%5B%22AKsRol-AVXCfJKXp8PqL-3RF4pW9uNIXCo3UHClhJ9dJgO19gcaKJg2fffozXWuaEPIIAfeD-JZ3SO0DX2tMgofcBnZI-16iXFrO2NRrimSd9nN5tiMFuSAeSB_QMWhmbb3j45TD-VwQoQspMMiX9TcEdnt1jB_HfQ%3D%3D%22%5D%5D',
        '__gads': 'ID=409c7e7640aae23a:T=1722522386:RT=1722522386:S=ALNI_MZFfTEFeA77fWl4JRHJT3RULlkARg',
        '__gpi': 'UID=00000e8258428df8:T=1722522386:RT=1722522386:S=ALNI_MbDLWUnyWK3I1A7lNKt2s9SsdI3bw',
        '__eoi': 'ID=1b531def24abbee9:T=1722522386:RT=1722522386:S=AA-Afjaliq6RUeaqc8v3MgAcd_qQ',
        '_ga_ZSF3D6YSLC': 'GS1.1.1722522379.1.1.1722522486.0.0.0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'hx-current-url': 'https://ssstik.io/en-1',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'priority': 'u=1, i',
        'referer': 'https://ssstik.io/en-1',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': url.strip(),
        'locale': 'en',
        'tt': 'a1FNOGE2',
    }

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, 'html.parser') 

    
    search_strings = ['download as video']
    slides_video = downloadSoup.find_all('a', string=lambda text: text and any(s in text.lower() for s in search_strings))
    
    if slides_video:
        print("It'is a sequence of slides so it will take a bit more time")
        endpoint = slides_video[0]['hx-post']
        value = downloadSoup.find_all('input', attrs={'name': 'slides_data'})[0]['value']
        response = requests.post(endpoint, headers=headers, data={"slides_data": value})
        downloadLink = response.headers['hx-redirect']
    else:
        #it is a normal video
        downloadLink = downloadSoup.find_all('a')[0]['href']

    return downloadLink


def download_video(url, fileName, dirOutPath=".") -> bool:
    try:
        req = Request(url.strip())

        headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-GB,en;q=0.5',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }
        
        for key, value in headers.items():
            req.add_header(key, value)
        
        mp4File = urlopen(req)

        if mp4File.status != 200 and mp4File.status != 204:
            raise Exception(f"Error in the response, response.status = {mp4File.status}")

        with open(os.path.join(dirOutPath, fileName), "wb") as output:
            while True:
                data = mp4File.read(4096)
                if data:
                    output.write(data)
                else:
                    break
        print("Download done")
        return True
    except Exception as e:
        print(f"Error during the download: {e}")
        return False


if __name__ == "__main__":
    url = input("which url?: ")
    link = get_downloadlink(url)
    print(link)
    download_video(link, "az.mp4")
