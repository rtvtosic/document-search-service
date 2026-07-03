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
            results = response.json()
            st.write(f"**Найдено документов:** {len(results)}")

            # вывод каждого документа
            for doc in results:
                    st.header(f"#{doc['id']}",
                              divider="violet")
                    
                    st.write(doc["text"])
                    date_obj = datetime.fromisoformat(doc['created_date'])
                    st.caption(f"{date_obj.hour}:{date_obj.minute} {date_obj.day}.{date_obj.month}.{date_obj.year}")
                    st.caption(f"Рубрики: {', '.join(doc["rubrics"])}")
        else:
            st.error(f"Ошибка: {response.status_code}")
    else:
        st.warning("Введите запрос")