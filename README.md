# 超越神力解脱機（緑栄会公式マスク着用ツール）

ある日、お人好しで気弱な冴えない会社員オガワ（非ネ申）は、業務中に応対した料理人の土井善晴という美女に一目惚れ。しかし、その後散々な目にあい再会した土井善晴の前でも醜態をさらしてしまい、揚句ゴミの塊を水難者だと思い救助のためKIアトリウムの噴水に飛び込んでしまう。その際ゴミに混ざっていた変わった布製のマスクを拾い、オフィスに帰りそれを顔につけた途端、猛烈な緑の竜巻とともに超型破りな魔人**キュアハッピー**に変身してしまう。マスクの魔力でオガワ（非ネ申）は過剰な本性を引き出され不死身の身体、数々の超能力を身に着ける。

－－－－－

光栄にもAmong Us優勝記念で頂いた、世界に一つだけのマスクを皆様にも着用して頂きたいと思い、顔が写っている画像にマスクを着用させるアプリを作成いたしました。何枚あっても何人写っていても顔認識できるだけ片っ端から着用させます。皆で解脱しましょう。

**着用前→着用後（１人）**

<img src="/image/input/face.png" width=45%> → <img src="/image/output/face_weared.png" width=45%>

**着用前→着用後（複数人）**

<img src="/image/input/sample.png" width=45%> → <img src="/image/output/sample_weared.png" width=45%>

<br><br>

## つかいかた

### 0. ソースコードのダウンロード

- 適当なディレクトリでこのリポジトリをクローン

    ``` bash
    $ git clone https://github.com/running1017/the_mask.git
    ```

- または[the_mask.zip](https://github.com/running1017/the_mask/blob/master/the_mask.zip)をダウンロードして解凍

### 1. 顔画像の準備

- `./image/input`にマスクを着けさせたい人物の画像ファイルを保存
- 拡張子が`.png`もしくは`.jpg`のファイルのみ対応
- 証明写真的な真正面からの画像だとうまくいきやすい

### 2. 実行

- ルートディレクトリに移動

- Dockerで実行する場合（推奨）

    - docker-composeで実行

        ``` bash
        $ docker-compose up
        ```

    - 初回実行時のみコンテナイメージのビルドに数分かかる

- 通常のpython実行環境で実行する場合

    - 必要なPythonライブラリ（requirements.txtに記載）をインストール

        ``` bash
        $ pip install -r ./requirements.txt
        ```

    - `./main.py`を実行

        ``` bash
        $ python ./main.py
        ```

    - OpenCV絡みで諸々のエラーが出る場合はググって対処する

### 3. マスク着用を確認

- `./image/output`にマスク着用後の画像が作成されているので適宜利用する

<br><br>

## フォルダ構成

<pre>
./                                  ルートディレクトリ
├── README.md                       このファイル
├── make_package.sh                 配布用zip作成スクリプト
├── docker-compose.yml              コンテナ実行設定ファイル
├── Dockerfile                      コンテナイメージ定義ファイル
├── requirements.txt                実行に必要なPythonライブラリ
├── main.py                         メインプログラム
├── param_adjust.ipynb              パラメータ調整用jupyterファイル
├── data/
│   ├── cascades/                   カスケード分類に用いるxmlファイル
│   └── mask/
│        ├── mask.png               着用させるマスク画像
│        └── mask_parts.json        マスク画像上の顔パーツ位置パラメータ
├── image/
│   ├── input/                      入力フォルダ
│   │   ├── face.png                サンプル入力（1人）
│   │   └── sample.png              サンプル入力（複数人）
│   └── output/                     出力フォルダ
│        ├── face_weared.png        サンプル出力（1人）
│        └── sample_weared.png      サンプル出力（複数人）
└── mod/                            マスク着用モジュール
     ├── __init__.py
     └── wear.py
</pre>

<br><br>

## 参考

- [Python, OpenCVで顔検出と瞳検出（顔認識、瞳認識）](https://note.nkmk.me/python-opencv-face-detection-haar-cascade/)
- 利用カスケードファイル
    - https://github.com/opencv/opencv/tree/master/data/haarcascades
    - https://github.com/opencv/opencv_contrib/tree/1311b057475664b6af118fd1a405888bad4fd839/modules/face/data/cascades
- [最小二乗法によるホモグラフィ行列の計算（DLT法）](https://qiita.com/manteopel/items/ac435755eeebcadabf6a)
- [OpenCVで透過画像を扱う　～スプライトを舞わせる～](https://qiita.com/mo256man/items/f7524dd34718a01fb3df)
