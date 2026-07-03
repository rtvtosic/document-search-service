import os
import requests
import streamlit as st

from datetime import datetime


API_URL = os.getenv("API_URL", "http://localhost:8000")

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
        st.header(f"#{doc['id']}", divider="violet")
        st.write(doc["text"])
        date_obj = datetime.fromisoformat(doc['created_date'])
        st.caption(f"{date_obj.hour}:{date_obj.minute} {date_obj.day}.{date_obj.month}.{date_obj.year}")
        st.caption(f"Рубрики: {', '.join(doc['rubrics'])}")

        # если подтверждение запрошено ИМЕННО для этого документа — показываем вопрос
        if st.session_state.get("confirm_delete") == doc["id"]:
            st.warning("Удалить этот документ?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Да, удалить", key=f"yes_{doc['id']}"):
                    del_response = requests.delete(f"{API_URL}/documents/{doc['id']}")
                    if del_response.status_code == 200:
                        st.session_state["results"] = [
                            d for d in st.session_state["results"] if d["id"] != doc["id"]
                        ]
                        st.session_state["confirm_delete"] = None   # сбросить подтверждение
                        st.rerun()
                    else:
                        st.error("Не удалось удалить")
            with col2:
                if st.button("Отмена", key=f"no_{doc['id']}"):
                    st.session_state["confirm_delete"] = None       # сбросить, ничего не делая
                    st.rerun()
        else:
            # обычная кнопка удаления — по клику запрашивает подтверждение
            if st.button("Удалить", key=f"del_{doc['id']}"):
                st.session_state["confirm_delete"] = doc["id"]      # запомнить, что подтверждаем
                st.rerun()