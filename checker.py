import os
import time
import requests
from logger import my_logger
import traceback

timeout = (10, 10)

items = {
    'Internet connection': "https://www.baidu.com/",
    'SIHE Cloud Console': "https://mono-backend.sihe.cloud/api/test",
}

os.makedirs("data", exist_ok=True)


def check_item(item_key):
    assert item_key in items
    url = items[item_key]
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except Exception as e:
        my_logger.error(e)
        my_logger.error(traceback.format_exc())
        return False

def check_and_log(item_key):
    assert item_key in items
    result = check_item(item_key)
    my_logger.info(f"Check result for {item_key} = {result}")
    if result:
        with open(f"data/{item_key}.txt", "a") as f:
            f.write(str(time.time()))
            f.write("\n")
            
def read_log(item_key):
    assert item_key in items
    filepath = f"data/{item_key}.txt"
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return [float(x.strip()) for x in f]
    return []



if __name__ == '__main__':
    print(check_item("Internet connection"))
    print(check_item("SIHE Cloud Console"))