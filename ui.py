import requests
from datetime import datetime
import streamlit as st


API_URL = "http://localhost:8000"

st.title("Поиск по документам")

query = st.text_input("Введите поисковой запрос")

if st.button("Поиск"):
    if query:
        response = requests.post(
            f"{API_URL}/search", json={"query": query}
        )

        if response.status_code == 200:
            st.session_state["results"] = response.json()
        else:
            st.error(f"Ошибка: {response.status_code}")
    else:
        st.warning("Введите запрос")

if "results" in st.session_state:
    for doc in st.session_state["results"]:
        # header, text, caption
        st.header(f"#{doc['id']}", divider="violet")       
        st.write(doc["text"])
        date_obj = datetime.fromisoformat(doc['created_date'])
        st.caption(f"{date_obj.hour}:{date_obj.minute} {date_obj.day}.{date_obj.month}.{date_obj.year}")
        st.caption(f"Рубрики: {', '.join(doc["rubrics"])}")

        if st.button("Удалить", key=f"del_{doc['id']}"):
            del_response = requests.delete(f"{API_URL}/documents/{doc['id']}")

            if del_response.status_code == 200:
                st.session_state["results"] = [
                    d for d in st.session_state["results"] if d["id"] != doc["id"]
                ]
                
                st.rerun()
            else:
                st.error("Не удалось удалить")