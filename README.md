# 読んでミーア！ (manga_recommend)
「まだ知らない漫画に、出会おう」をコンセプトとしたマンガレコメンドWebアプリケーション

http://ec2-54-249-164-152.ap-northeast-1.compute.amazonaws.com/

電気代が高く常時実行はしていないため、URLに飛んでも使えないときもあります

# 使い方
## 環境：
- Python 3.8
  - gunicorn
  - flask
  - requests
  - numpy==1.24.3
  - wheel==0.38.4
  - gensim==3.8.3
  - pandas
  - pot
  - mecab-python3
  - fasttext
  - pickle
- MeCab

## ディレクトリ構成


## MeCabの設定



## フォルダの設定
本リポジトリのクローン：
```bash
git clone https://github.com/mokemoke3/manga_recommend.git
```

モデルダウンロード：
https://github.com/mokemoke3/manga_recommend/releases

/manga_recommend　直下に移動

ライブラリのインストール：
```bash
pip install -r requirements.txt
```

実行：
```bash
python app.py
```


