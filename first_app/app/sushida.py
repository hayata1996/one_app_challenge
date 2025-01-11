# https://withcation.com/2019/04/08/post-372
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageOps
import pyocr
import pyocr.builders
from utils import logger

logger = logger.get_logger(name=__name__, debug=True)


# ドライバーを開く
# https://qiita.com/Chronos2500/items/7f56898af25523d04598 を参考にしている
# ヘッドレスモードをオフにする
chrome_options = Options()
chrome_options.headless = False  # ヘッドレスモード無効化
driver = webdriver.Chrome(options=chrome_options)

# ウィンドウサイズを固定
# +123としているのは
# 「Chromeは自動テストソフトウェアによって制御されています。」
# という部分を考慮している
window = (800, 600+123)
driver.set_window_size(*window)

# OpenGL版の寿司打を開く
target_url = 'https://sushida.net/play.html'
driver.get(target_url)

# 寿司打のゲーム画面をずらすために書く
# target_xpath = '//*[@id="gameContainer"]'
webgl_element = driver.find_element(By.ID, "#canvas")
logger.debug(f"webgl_element: {webgl_element}")

# Canvasの位置とサイズを取得
location = webgl_element.location
size = webgl_element.size
print(f"Canvasの位置: {location}, サイズ: {size}")

# 要素の詳細情報を取得
element_html = webgl_element.get_attribute('outerHTML')
logger.debug(f"Element HTML: {element_html}")

# クリックする前にロード時間待機
sleep(10)

# Canvasの中央座標を計算
canvas_center_x = size['width'] / 2
canvas_center_y = size['height'] / 2

# スタートボタンの座標
# 実際のクリック位置を取得
click_x = location['x'] + canvas_center_x
click_y = location['y'] + canvas_center_y + 30
logger.debug(f"Canvas中央の座標: ({click_x}, {click_y})")

# Canvas中央をクリック
action = ActionChains(driver)
action.move_to_element_with_offset(webgl_element, 0, 30).perform()
logger.debug(f"移動先座標: ({click_x}, {click_y})")

# # JavaScriptを使用してクリック位置にマーカーを表示
# although this is useful, it interacts ocr quite a bit since it just on top of the caracters
# driver.execute_script("""
#     var marker = document.createElement('div');
#     marker.style.position = 'absolute';
#     marker.style.background = 'red';
#     marker.style.width = '20px';
#     marker.style.height = '20px';
#     marker.style.borderRadius = '50%';
#     marker.style.left = arguments[0] + 'px';
#     marker.style.top = arguments[1] + 'px';
#     marker.style.zIndex = '1000';  // マーカーを前面に表示
#     document.body.appendChild(marker);
# """, click_x, click_y)
logger.debug("JavaScriptを使用してクリック位置にマーカーを表示しました。")

# 実際にクリックを実行
action.click().perform()
logger.debug("Canvas中央をクリックしました。")

# ボタンが表示されるまで待つ
sleep(2)

# お勧めコースをクリックする
actions = ActionChains(driver)
actions.move_to_element_with_offset(webgl_element, 0, 30).perform()
logger.debug(f"移動先座標: ({click_x}, {click_y})")
actions.click().perform()
logger.debug("お勧めコースのボタンをクリックしました。")

# <body>に向かってキーを入力させる
target_xpath = '/html/body'
element = driver.find_element(By.XPATH, target_xpath)
element.send_keys(" ")

# 画像の範囲を指定するためのリスト
im_ranges = [136, 124, 112, 100, 88, 76]

# PyOCRのツール
# tesseractが必要になる。参考: https://dev.classmethod.jp/articles/ocr-on-a-mac-device-with-pytesseract/
tool = pyocr.get_available_tools()[0]

from time import time
start = time()
while time() - start < 90.0:

    # 移動した
    # ファイル名
    fname = "sample_image.png"
    # スクショをする
    driver.save_screenshot(fname)

    # 画像をPILのImageを使って読み込む
    # ローマ字の部分を取り出す
    # im = Image.open(fname).crop((0,230,500,254))
    # this depends on the screen size, this didn't work with bigger screens. 
    # Need modification for production
    im = Image.open(fname).crop((530, 690, 1030, 744))

    # 画像の範囲を指定する
    for im_range in im_ranges:
        if im.getpixel((im_range, 0)) == (255, 255, 255, 255):
            im = im.crop((im_range+20, 0, 500-im_range-20, 24))

            # 画像を二値化する
            im = im.convert("L")
            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    if im.getpixel((i, j)) >= 128:
                        im.putpixel((i, j), 0)
                    else:
                        im.putpixel((i, j), 255)
            break

    im.save("sample.png")

    # tool で文字を認識させる
    text = tool.image_to_string(im, lang='eng', builder=pyocr.builders.TextBuilder())

    # text を確認
    print(text)

    # 文字を入力させる
    element.send_keys(text)


input("何か入力してください")

# ドライバーを閉じる
driver.close()
driver.quit()