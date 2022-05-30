# photo_ai
画像認識モデル作成、モデルを用いたFAST APIでの判別結果表示

## Requirement
- Python 3.7.3

## Module
- ~~tensorflow==1.15~~
- tensorflow==2.9(暫定対応)
- tensorflow hub
- iclawler(photo_get.py)
- pykakasi(photo_get.py)
- fastapi(main.py)

## How To Use

### 使用パッケージのインストール(option)

```
 pip install -r requirements.txt
```

### 学習画像を用意する  
用意したい画像の名前を配列に格納する(get_photo.py)

```python
value_list = [
  'カブトムシ',
  'コカブトムシ',
  'サイカブトムシ',
  'アカアシクワガタ',
  'オオクワガタ',
  (etc...)
]
```  

get_photo.pyを実行して画像収集(./resizeが作成され、保存)

```
python get_photo.py
```

### 学習モデルの作成
get_photo.py実行後のresizeフォルダ内に集められた画像で学習モデルを作成
- 学習モデルの保存先が引数で設定可能ですが、非推奨(フォルダが存在しない場合のエラー防止,API使用時のモデル読み込み時のデフォルトパスが既に設定されている為)

```
python retrain.py --image_dir=resize --how_many_training_steps [学習回数]

python retrain.py --image_dir=resize --how_many_training_steps 5000
```

### 画像判定APIの起動
起動後、index.phpで画像をpostして動作確認可能です

```
python main.py
```

