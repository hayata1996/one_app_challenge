### プロジェクト案
Mediapipeとpyautoguiを使用してジェスチャーによるGUI操作を実装する

### 必要事項
* デフォルトのジェスチャーは少ないためtensorflowでモデルを作成する
* pyautoguiでモデルを活用して、pcを操作するロジックを組み込む

### 懸念
* 学習を行う際は静止画になるためバイバイなどの動作を学習するには工夫が必要？

### memo
move_to_element_with_offsetは要素の中心からどうオフセットするか設定できる
https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html#selenium.webdriver.common.action_chains.ActionChains.move_to_element_with_offset

