# api


## 開發環境設定

- pipenv shell: 啟動虛擬環境
- pipenv sync: 同步 package
- pipenv install -e .: 把 project 變成 package (主要是為了將 project 路徑新增到 pythonpath)
- python genenv.py

## run api server

- docker

    up: docker-compose -f docker-compose.yml up -d

    down: docker-compose -f docker-compose.yml down

    docker url : http://127.0.0.1:9000/docs

- non-docker

    pipenv run uvicorn api.main:app --reload --host 0.0.0.0

    url: http://127.0.0.1:8000/docs

## future work

- todo list
FIXME:
- db 資料型態問題
- 資料格式:
    https://jsoneditoronline.org/#left=local.zenibe&right=local.zadopu
- keyword api 還有需要有
    - filter (每次調整filter 參數就會重新request)
        keyword (完成, 必須給的參數)
        聲量,  (完成, 最大值跟最小值同時都要有?!)
        爆發力(kiko晚點弄),
        立場(producer, position),  (完成)
        管道(目前只有新聞)
    - 立場 api 跟 kiko 討論 (完成hard code)
    - 管道 api 跟 kiko 討論 (完成hard code)
- api group id, for 分享使用 跟kiko討論
- docker
- ci 目前還無法正常執行
    - 不確定是不是因為 DB 防火牆
- add test
- hotinfo api
- api 分頁 跟 kiko 討論 (完成)
