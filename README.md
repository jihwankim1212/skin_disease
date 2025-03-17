# GC skin disease AI model classification API
skin disease API

---

## Environment
<ddetails>
  <summary>Docker build</summary>

Release mode

```
docker build -t skin_disease:1.x.x  -f dockerfile .
```
1.x.x 버전은 기입 필수

</details>

<ddetails>
  <summary>Docker run</summary>

## docker run
---

### Release mode image (1.0.0 버전) 
```
docker run -d -it -p 5502:5502 -e HOST=0.0.0.0 -e PORT=5502 --ipc=host skin_disease:1.0.0
```

</details>

---

## Project

```
.
├── app                 (서버코드)
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── app.py
│   └── utils.py
├── classification      (피부 질환 분류)
├── log_config          (로그 설정)
├── logs                (로그 저장폴더)
├── dockerfile          (dockerfile for release mode)
├── README.md
├── requirements.txt
└── server.py           (server start script )
```

---
## Log

내부 로그는 logs directory 밑에 저장되며 
아래 명령어로 docker container 외부로 가져와서 볼 수 있다. (현재 위치로 복사)
```
docker cp <컨테이너 이름 또는 ID>:/app/logs .
```

---
## Version History

|      Version       |       Description        |   Date   |
|:------------------:|:------------------------:|:--------:|
| skin_disease:1.0.0 |          초기 버전           | 23-12-18 |
| skin_disease:1.0.1 | 피부 분류 15 -> 12 Class로 변경 | 24-01-23 |

## Todo
1. 15개 class에서 확대 -> class가 늘어나면 인식률이 낮아짐 : pass
2. 과적합 해결 (자주 나오는 것만 나옴)
3. 사진 촬영에 대한 더 좋은 방법 개선
