# Real Estate Chatbot

Chatbot hỗ trợ tư vấn và định giá bất động sản, sử dụng FastAPI, OpenAI GPT và SerpAPI.

## Yêu cầu

- Python 3.8+
- Tài khoản OpenAI (API key)
- Tài khoản SerpAPI (API key)
- [ngrok](https://ngrok.com/) (nếu muốn chia sẻ public)

## Cài đặt

1. **Clone repo:**
   ```bash
   git clone https://github.com/dncq/real_estate_chatbot.git
   cd real_estate_chatbot

2. **Cài đặt các thư viện:**
   ```bash
   pip install -r requirements.txt

3. **Tao file .env trong thư mục backend với nội dung:**
   ```sh
   OPENAI_API_KEY=your_openai_api_key
   SERPAPI_KEY=your_serpapi_key

## Chạy ứng dụng (localhost)

1. **Chạy backend FastAPI:**
    ```baah
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000
2. **Chạy file** `frontend/index.html` **bằng trình duyệt để sử dụng giao diện chatbot.**

## Chia sẻ public với ngrok (tùy chọn)

1. **Cài đặt ngrok** [Download ngrok](https://ngrok.com/downloads/windows?tab=download)
2. **Chạy ngrok sau khi chay backend:**
   ```sh
   ngrok http 8000

3. **Copy link forwarding  và chia sẻ với người dùng**