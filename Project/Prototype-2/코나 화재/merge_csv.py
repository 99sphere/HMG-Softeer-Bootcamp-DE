import os
import pandas as pd

# 루트 폴더 경로를 지정하세요.

root_folder_path = 'raw_data/naver_cafe/posts'


# 모든 하위 폴더에서 CSV 파일을 찾기
csv_files = []
for root, dirs, files in os.walk(root_folder_path):
    for file in files:
        if file.endswith('.csv'):
            csv_files.append(os.path.join(root, file))

# 각 CSV 파일을 데이터프레임으로 읽고 리스트에 저장
dfs = []
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    dfs.append(df)

# 모든 데이터프레임을 하나로 합치기
combined_df = pd.concat(dfs, ignore_index=True)

# 합친 데이터를 새 CSV 파일로 저장
output_file = 'data/naver_cafe_post.csv'
combined_df.to_csv(output_file, index=False)