import os

import requests
import streamlit as st
from dotenv import load_dotenv

API = {
    "날씨": "https://api.openweathermap.org/data/2.5/weather",  # 🔌 OpenWeather 현재 날씨
}
SEOUL = {"lat": 37.5665, "lon": 126.9780}

ERRORS = {
    401: "날씨 키가 틀렸거나 아직 켜지지 않았어요(가입 후 최대 2시간).",
    404: "그 도시를 찾지 못했어요.",
    429: "1분에 너무 많이 불렀어요. 잠시 뒤에 다시 해 주세요.",
}


def get_weather(key):
    params = {**SEOUL, "appid": key, "units": "metric", "lang": "kr"}
    try:
        res = requests.get(API["날씨"], params=params, timeout=10)  # 🔌 API 호출
    except requests.RequestException:
        # 예외 메시지에 주소(키 포함)가 들어갈 수 있어 출력하지 않는다
        return None, "날씨 서버에 연결하지 못했어요. 인터넷을 확인해 주세요."
    if res.status_code != 200:
        return None, ERRORS.get(res.status_code, f"날씨를 가져오지 못했어요. (오류 코드 {res.status_code})")
    return res.json(), None


@st.cache_data(ttl=600, show_spinner="날씨를 불러오는 중...")
def fetch_weather(key):
    # 새로고침 때마다 API를 부르지 않도록 10분간 결과를 재사용한다
    return get_weather(key)


def main():
    st.set_page_config(page_title="서울 날씨", page_icon="☁")
    st.title("📍 서울 현재 날씨")

    load_dotenv()
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key:
        st.error(".env에 OPENWEATHER_API_KEY가 없어요. .env.example을 보고 채워 주세요.")
        return

    if st.button("🔄 새로고침"):
        st.cache_data.clear()

    data, error = fetch_weather(key)
    if error:
        st.error(error)
        return

    temp = data["main"]["temp"]  # data["main"]["temp"] = 지금 기온
    feels = data["main"]["feels_like"]  # data["main"]["feels_like"] = 체감 온도
    humidity = data["main"]["humidity"]  # data["main"]["humidity"] = 습도(%)
    desc = data["weather"][0]["description"]  # data["weather"][0]["description"] = 날씨 설명

    st.subheader(f"☁ {desc}")
    col1, col2, col3 = st.columns(3)
    col1.metric("🌡 기온", f"{temp:.1f}°C")
    col2.metric("🧥 체감 온도", f"{feels:.1f}°C")
    col3.metric("💧 습도", f"{humidity}%")
    st.caption("출처: 날씨: OpenWeather")


main()
