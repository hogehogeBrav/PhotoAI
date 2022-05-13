# photo_ai
画像認識モデル作成、モデルを用いたFAST APIでの判別結果表示

## Requirement
- Python 3.7.3

## Module
- tensorflow==1.15
- tensorflow hub
- iclawler(photo_get.py)
- pykakasi(photo_get.py)
- fastapi(main.py)

## How To Use
- 学習画像を用意する
```py


- 学習モデルの作成
```
python retrain.py --image_dir=resize --output_graph=[保存先] --output_labels=[保存先] --how_many_training_steps [学習回数]
python retrain.py --image_dir=resize --output_graph=./model/output_graph.pb --output_labels=./model/output_labels.txt --how_many_training_steps 5000
```
