# GLUE STS 내 훈련, 검증 데이터 예제 변환
from sentence_transformers.readers import InputExample
import os
import pandas as pd
import sqlite3

from etc.preproc import replaceURL, removeAtUser, removeHashtagInFrontOfWord

def Preprocess(datasets):
  train_samples = []
  dev_samples = []
  test_samples = []
  for phase in ["train", "validation"]:
      examples = datasets[phase]
      

      for example in examples:
          score = float(example["label"]) / 5.0  # 0.0 ~ 1.0 스케일로 유사도 정규화

          inp_example = InputExample(
              texts=[example["sentence1"], example["sentence2"]],
              label=score,
          )

          if phase == "validation":
              dev_samples.append(inp_example)
          else:
              train_samples.append(inp_example)

  return train_samples, dev_samples




# SQLite3 연결
def get_db(args):
  # conn = sqlite3.connect(f'{args.db_name}')

  # # 쿼리 실행 및 데이터프레임 생성
  # query = 'SELECT * FROM tweet;'
  # ex = pd.read_sql_query(query, conn)
  ex = pd.read_csv(f'./data/{args.db_name}')
  raw = ex[['companyName','tweetDate', 'rawContent']]

  lenn = len(raw) - len(raw.dropna())

  print('결측치 제거',lenn)
  raw = raw.dropna()
  missing_values = raw.isnull().sum()
  print('결측치가 확실하게 없는지 확인, 0이면 없는 것! ',missing_values)

  raw_all = raw.rawContent.values.tolist()

  print('db 얻기 ',type(raw_all))
  return raw_all, raw



def setup(args):
  print('구글 Drive 환경에 폴더를 제작합니다.')
  if args.drive:
    os.makedirs('/content/drive/MyDrive/inisw08', exist_ok=True)
    os.makedirs('/content/drive/MyDrive/inisw08/bertopic', exist_ok=True)
    os.makedirs('/content/drive/MyDrive/inisw08/bertopic/barchart', exist_ok=True)

  
  else:
    print('로컬 환경에 폴더를 제작합니다.')
    os.makedirs('/content/inisw08', exist_ok=True)
    os.makedirs('/content/inisw08/bertopic', exist_ok=True)
    os.makedirs('/content/inisw08/bertopic/barchart', exist_ok=True)




  output_path = args.output_path
  output_path = output_path.split('/')[-1]
  os.makedirs(output_path, exist_ok=True)





preproc = []
def get_preproc(doc):
  for text in doc:
    text = replaceURL(text)
    text = removeAtUser(text)
    text = removeHashtagInFrontOfWord(text)
    preproc.append(text)

  ser = pd.Series(preproc)
  ser_list = ser.tolist()
  return ser_list


  
