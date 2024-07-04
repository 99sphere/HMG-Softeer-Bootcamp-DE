# Week 1 (Pandas, Matplotlib, SQL)
## Environment Setting (venv with Jupyter)
### venv 가상환경 생성, activate, deactivate
#### create virtual env 

```
python3 -m venv {virtual env name}
```

#### activate & deactivate
```
source {virtual env name}/bin/activate
```

```
deactivate
```

### Jupyter Lab에 kernel 추가
```
python3 -m ipykernel install --user --name [virtual env name] --display-name [jupyter kernel name]
```

### Jupyter Lab에서 kernel 제거
```
jupyter kernelspec list (존재하는 kernel 확인)
jupyter kernelspec uninstall {jupyter kernel name}
```

## Intro to Pandas and Matplotlib
### Data Processing
#### Analysis
- df.info: column name, dtype 등 확인
- df.columns: 존재하는 column들의 이름 확인
- df.describe: statistical한 정보 확인 (mean, std, ..., etc)
- 기타 column 별 연산 모두 가능

#### Manipulate
- column 삽입 -> df['key'] = values 
- df.rename: column 이름 변경
- idx로 indexing 할 때는 iloc, condition으로 indexing 할 때는 loc
- stack, unstack으로 multi-index 생성 및 해제 가능

```
(ex)
df.loc[df.Region=="Asia"].iloc[:5]
```

### Visualize (with Matplotlib)
- df.plot() -> line, bar, hist, scatter 등 matplotlib으로 그릴 수 있는 건 대부분 가능
- df.hist() -> 여러 개의 column에 대한 histogram을 아래 처럼 한번에 생성
![image](https://github.com/99sphere/2024-Spring-System-Programming/assets/59161083/e097f655-9366-4adb-8740-b5dec66b93cf)
- option들이 matplot과 거의 동일함.

## Intro to SQL
- DB Browser, Data Grip 같은 tool들로 쉽게 값 확인 가능
- [간단한 명령어 참고](https://github.com/99sphere/HMG_DataEngineering/blob/main/Mission/W1/mission2.ipynb)
- 더 복잡한 상황 연습해야 함 -> 프로그래머스 연습문제 푸는 중

## Missions
1.
2.
3.