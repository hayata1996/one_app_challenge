# https://withcation.com/2019/04/08/post-372
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pyocr
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

# PyOCRのツール
# tesseractが必要になる。
# 参考: https://dev.classmethod.jp/articles/ocr-on-a-mac-device-with-pytesseract/
tool = pyocr.get_available_tools()[0]

from time import time
start = time()
# Since this is just for fun, we will only run this for 30 seconds
while time() - start < 30.0:

    # 移動した
    # ファイル名
    fname = "sample_image.png"
    # スクショをする
    driver.save_screenshot(fname)

    # 画像をPILのImageを使って読み込む
    # ローマ字の部分を取り出す
    im = Image.open(fname).crop((530, 690, 1030, 744))
    im.save("sample.png")

    # tool で文字を認識させる
    text = tool.image_to_string(
        im,
        lang='eng',
        builder=pyocr.builders.TextBuilder()
    )

    # text を確認
    print(text)

    # 文字を入力させる
    element.send_keys(text)


input("何か入力してください")

# ドライバーを閉じる
driver.close()
driver.quit()