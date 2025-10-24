docker-compose up --build



Reference:

Docker Compose 與 Container 網路共用說明
預設網路行為
	•	當你使用 `docker-compose` 啟動多個服務（container）時，這些 container 會自動被加入同一個預設網路（通常名稱為 `專案名_default`）。
	•	在這個共用網路下，container 之間可以直接用服務名稱（如 `lab`、`frontend`）互相通訊，不需要額外設定。
實際效果
	•	例如，`frontend` container 可以直接用 `http://lab:9012/` 連線到 `lab` 服務，無需指定 IP。
	•	這種設計讓多服務架構的 microservice 專案部署變得簡單且一致。
進階說明
	•	你也可以在 `docker-compose.yml` 內自訂網路，或讓多個 compose 專案共用同一網路。
	•	除非你特別設置 `network_mode: host` 或明確隔離網路，否則所有服務都會自動共用同一個 bridge network。
小結
	•	是的，使用 docker-compose 啟動的不同 container 預設會共用一個網路。
	•	這讓 container 之間的服務名稱解析與互通變得非常方便，無須額外手動設定。



這段 log 顯示你的 RAG_Agent_with_LLM 專案成功啟動了 兩個容器，各自扮演不同角色：

🧱 1️⃣ frontend-1
Container: rag_agent_with_llm-frontend-1
Port: 8090
Framework: FastAPI + Gunicorn + Uvicorn


📌 功能：前端 API / Web 服務層

這是你專案的主要 入口點。

它透過 gunicorn 啟動 FastAPI / Uvicorn 應用伺服器。

使用者（或其他服務）會透過 http://localhost:8090 向它發送請求。

通常負責：

接收 query（例如使用者輸入的問題）

調用 LLM / RAG 模組進行推理

回傳答案

🧠 2️⃣ lab-1
Container: rag_agent_with_llm-lab-1
Port: 9012
Framework: Uvicorn (FastAPI)

這裡的後端，是做給 FAISS 做向量查找的。
語言模型那端，是用雲端，跟Nvidia server 溝通的，
所以才要提供 API key


📌 功能：後端實驗 / 模型服務層

這是內部的「LLM / RAG 推理後端」。

啟動了另一個 FastAPI 應用，通常會被 frontend-1 呼叫。

可能負責：

連接 LLM（例如 NVIDIA NIM、Ollama、或本地模型）

文檔檢索（RAG 的 retriever 部分）

向量搜尋（例如 FAISS、Chroma）

整合嵌入、摘要或生成任務

⚙️ 兩者關係

整體流程大致如下：

User → frontend (8090) → lab (9012) → LLM / RAG pipeline → frontend 回傳結果


例如：

你在網頁或 API 發送問題到 localhost:8090/query

frontend 收到後，把問題轉發給 http://lab:9012/api/ask

lab container 執行檢索 + 調用 LLM

結果傳回 frontend，再回給使用者

🔍 補充說明

你可以用以下命令檢查：

docker ps


會看到：

CONTAINER ID   IMAGE                         PORTS
xxx            rag_agent_with_llm-frontend   0.0.0.0:8090->8090/tcp
yyy            rag_agent_with_llm-lab        0.0.0.0:9012->9012/tcp
