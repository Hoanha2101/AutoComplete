import streamlit as st
import pickle
from library import *
from utils import *

# Tải dữ liệu từ các file pickle
with open("./data/tokenized_sentences_data.pickle", 'rb') as handle:
    tokenized_sentences_data = pickle.load(handle)

with open("./data/unique_words.pickle", 'rb') as handle:
    unique_words = pickle.load(handle)

def main():
    st.title("Search")
    # Kiểm tra và khởi tạo giá trị mặc định cho text_input trong session_state
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
        
    # Lấy giá trị hiện tại của text input từ người dùng
    user_input = st.text_input("Please enter text", key='user_input', value = st.session_state.user_input)

    # Cập nhật gợi ý dựa trên giá trị nhập vào
    suggestions = options(user_input, tokenized_sentences_data, unique_words)
    
    # Callback để cập nhật text input khi một lựa chọn được chọn
    def update_input():
        st.session_state.user_input = st.session_state.suggestion
    
    # Tạo selectbox với danh sách các tùy chọn đã cập nhật
    option = st.selectbox(
        "Suggestions",
        options=suggestions,
        index=0,
        key='suggestion',
        on_change=update_input
    )
    
    st.write("You selected:", option)

if __name__ == "__main__":
    main()
