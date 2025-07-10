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
