import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from recommend import recommend


# 실시간 날씨 정보 받아오기
# 현재 시간 정보 
service_key = st.secrets['service_key']
vilage_open_api = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?'

now = datetime.now()
base_date = now.strftime("%Y%m%d")
base_time = now.strftime("%H%M")

base_minute = int(base_time[2:])

if base_minute >= 30:
    base_hour = base_time[:2]
    base_minute = "30"   
else:
    base_hour = str(int(base_time[:2]) - 1).zfill(2)
    base_minute = "30"

base_time = base_hour + base_minute

# 회기동 좌표 : (nx, ny) = (61, 127)
nx = 61
ny = 127
num_row = 40

data = dict()
data['date'] = base_date
weather_data = dict() # 실시간 날씨 '그룹'
weather_info = dict() # 실시간 날씨 '정보'

for page_num in range(1, 10):

    params = f'serviceKey={service_key}&pageNo={page_num}&numOfrows={num_row}&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}'

    res = requests.get(vilage_open_api + params)
    soup = BeautifulSoup(res.content, 'html.parser')

    items = soup.find_all('item')
    
    for i, item in enumerate(items):
        fcst_time = item.find('fcsttime').get_text() # 예측시간
        category = item.find('category').get_text() # 카테고리
        fcst_value = item.find('fcstvalue').get_text() # 예보값
        
        # 기간별 온도 : [-12.1 8.4 17.9 23.9 31.7]
        # -12.1보다 작은 경우 - 0
        # 31.7보다 큰 경우 - 3
        if category == 'T1H':
            weather_info['기온'] = int(fcst_value)
            if (int(fcst_value) < 8.4):
                weather_data['기온'] = 0
            elif (8.4 <= int(fcst_value) < 17.9):
                weather_data['기온'] = 1
            elif (17.9 <= int(fcst_value) < 23.9):
                weather_data['기온'] = 2
            else:
                weather_data['기온'] = 3
            
        # 하늘 상태 : [1, 2, 3, 5]
        # 1(맑음), 2(구름 적음) - 맑음(0)
        # 3(구름 많음), 4(흐림) - 흐림(1)
        if category == 'SKY':
            weather_info['흐림'] = fcst_value
            if (fcst_value == '1') | (fcst_value == '2'):
                weather_data['흐림'] = 0
                weather_info['흐림'] = '맑음'
            else:
                weather_data['흐림'] = 1
                if fcst_value == '3':
                  weather_info['흐림'] = '구름 많음'
                else:
                  weather_info['흐림'] = '흐림'
                
        # 강수 형태 : 0 / 1 ~ 7
        # 비/소나기/눈 X : 0, 비/소나기/눈 O : 1,
        if category == 'PTY':
            weather_info['비/소나기/눈'] = fcst_value
            if (fcst_value == '0'):
                weather_data['비/소나기/눈'] = 0
                weather_info['비/소나기/눈'] = '-'
            else:
                weather_data['비/소나기/눈'] = 1
                if (fcst_value == '1'):
                  weather_info['비/소나기/눈'] = '비'
                elif fcst_value == '2':
                  weather_info['비/소나기/눈'] = '비/눈'
                elif fcst_value == '3':
                  weather_info['비/소나기/눈'] = '눈'
                elif fcst_value == '4':
                  weather_info['비/소나기/눈'] = '소나기'
                elif fcst_value == '5':
                  weather_info['비/소나기/눈'] = '빗방울'
                elif fcst_value == '6':
                  weather_info['비/소나기/눈'] = '빗방울눈날림'
                else:
                  weather_info['비/소나기/눈'] = '눈날림'

#추천 결과
recommendation = recommend(weather_data['기온'], weather_data['흐림'], weather_data['비/소나기/눈'])

# 이미지 url (이디야커피)
url_link = dict()
url_link['딸기라떼'] = 'https://www.ediya.com/files/menu/IMG_1672618018525.png'
url_link['레몬에이드'] = 'https://www.ediya.com/files/menu/IMG_1647322413547.png'
url_link['아메리카노'] = 'https://www.ediya.com/files/menu/IMG_1647320805422.png'
url_link['자몽에이드'] = 'https://www.ediya.com/files/menu/IMG_1647322422524.png'
url_link['유자차'] = 'https://www.ediya.com/files/menu/IMG_1647323168645.png'
url_link['청포도에이드'] = 'https://www.ediya.com/files/menu/IMG_1647322445174.png'
url_link['유자에이드'] = 'https://www.ediya.com/files/menu/IMG_1647322677153.png'
url_link['아이스티복숭아'] = 'https://www.ediya.com/files/menu/IMG_1647322896670.png'
url_link['아이스 레몬차'] = 'https://www.ediya.com/files/menu/IMG_1647322413547.png'
url_link['아이스 유자차'] = 'https://www.ediya.com/files/menu/IMG_1647322677153.png'
url_link['아이스 민트초코라떼'] = 'https://www.ediya.com/files/menu/IMG_1647321879153.png'
url_link['아이스 오곡라떼'] = 'https://www.ediya.com/files/menu/IMG_1647319854660.png'
url_link['아이스 초코라떼'] = 'https://www.ediya.com/files/menu/IMG_1647321814289.png'
url_link['아이스 밀크티'] = 'https://www.ediya.com/files/menu/IMG_1647321814289.png'
url_link['아이스 그린티라떼'] = 'https://www.ediya.com/files/menu/IMG_1647321741180.png'
url_link['아이스 카라멜마끼아또'] = 'https://www.ediya.com/files/menu/IMG_1647321212721.png'
url_link['아이스 카페라떼'] = 'https://www.ediya.com/files/menu/IMG_1647324719307.png'
url_link['아이스 바닐라라떼'] = 'https://www.ediya.com/files/menu/IMG_1647321034823.png'
url_link['콜드브루라떼블랜딩'] = 'https://www.ediya.com/files/menu/IMG_1647320848557.png'
url_link['콜드브루블랜딩'] = 'https://www.ediya.com/files/menu/IMG_1647320805422.png'
url_link['콜드브루싱글'] = 'https://www.ediya.com/files/menu/IMG_1647320805422.png'
url_link['카푸치노'] = 'https://www.ediya.com/files/menu/IMG_1671582405654.png'
url_link['카페라떼'] = 'https://www.ediya.com/files/menu/IMG_1647324689152.png'
url_link['바닐라라떼'] = 'https://www.ediya.com/files/menu/IMG_1647324689152.png'
url_link['크리스틴 캐모마일'] = 'https://www.ediya.com/files/menu/IMG_1647322717592.png'
url_link['에스프레소'] = 'https://www.ediya.com/files/menu/IMG_1647320254869.png'
url_link['밀크티'] = 'https://www.ediya.com/files/menu/IMG_1647322607583.png'
url_link['오곡라떼'] = 'https://www.ediya.com/files/menu/IMG_1647319867876.png'
url_link['모과차'] = 'https://www.ediya.com/files/menu/IMG_1647323168645.png'

# 사이드바
# 실시간 정보
with st.sidebar:
  st.metric(':orange[날짜]', now.strftime("%Y-%m-%d"))
  st.metric(':red[기온]', str(weather_info['기온']) + '°C')
  st.metric(':green[날씨]', weather_info['흐림'])
  st.metric(':blue[비/소나기/눈]', weather_info['비/소나기/눈'])

# 첫 화면
# 버튼 누를 시 실시간 날씨 정보 기반 음료 추천
x = st.empty()
_, col, _ = x.columns((2, 6, 2))
col.markdown('----')
col.markdown("<h1 style='text-align: center;'>KHUDA Recsys</h1>", unsafe_allow_html=True)
col.markdown("<h2 style='text-align: center; color: grey;'><i>DRINK OF THE DAY</i></h2>", unsafe_allow_html=True)
col.markdown('----')

col1, col2, col3 = col.columns([3,3,3])
button_pressed = col2.button(':red[Recommend]')

if button_pressed:
  # col3.markdown("<h2 style='text-align: center; '>[Recommendation List]</h2>", unsafe_allow_html=True)
  x.empty()
  col1, col2, col3 = st.columns([1, 1, 1])
  col1.markdown("----", unsafe_allow_html=True)
  col1.markdown(f"<h5 style='text-align: center;'>[1] {recommendation[0]}</h5>", unsafe_allow_html=True)
  col1.image(url_link[recommendation[0]])
  col1.markdown("----", unsafe_allow_html=True)

  col1.markdown("----", unsafe_allow_html=True)
  col1.markdown(f"<h5 style='text-align: center;'>[4] {recommendation[3]}</h5>", unsafe_allow_html=True)
  col1.image(url_link[recommendation[3]])
  col1.markdown("----", unsafe_allow_html=True)

  col2.markdown("----", unsafe_allow_html=True)
  col2.markdown(f"<h5 style='text-align: center;'>[2] {recommendation[1]}</h5>", unsafe_allow_html=True)
  col2.image(url_link[recommendation[1]])
  col2.markdown("----", unsafe_allow_html=True)

  col2.markdown("----", unsafe_allow_html=True)
  col2.markdown(f"<h5 style='text-align: center;'>[5] {recommendation[4]}</h5>", unsafe_allow_html=True)
  col2.image(url_link[recommendation[4]])
  col2.markdown("----", unsafe_allow_html=True)

  col3.markdown("----", unsafe_allow_html=True)
  col3.markdown(f"<h5 style='text-align: center;'>[3] {recommendation[2]}</h5>", unsafe_allow_html=True)
  col3.image(url_link[recommendation[2]])
  col3.markdown("----", unsafe_allow_html=True)

  col3.markdown("----", unsafe_allow_html=True)
  col3.markdown(f"<h5 style='text-align: center;'>[6] {recommendation[5]}</h5>", unsafe_allow_html=True)
  col3.image(url_link[recommendation[5]])
  col3.markdown("----", unsafe_allow_html=True)
