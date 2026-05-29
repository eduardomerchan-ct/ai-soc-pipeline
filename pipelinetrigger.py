import os
from datetime import datetime
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
 
load_dotenv()
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
DAILY_LOGS_CONTAINER = "daily-logs"
FILTERED_LOGS_CONTAINER = "filtered-logs"
today = datetime.now().strftime("%Y-%m-%d")
 
 
def download_logs():
    try:
        client = BlobServiceClient.from_connection_string(connection_string)
        container = client.get_container_client(DAILY_LOGS_CONTAINER)
        blob_name = f"{today}.txt"
        blob = container.get_blob_client(blob_name)
        contents = blob.download_blob().readall().decode("utf-8", errors="ignore")
        print(f"[AI-SOC] Downloaded {blob_name} from daily-logs")
        return contents
    except Exception as error:
        print(f"[AI-SOC] No log file found for today: {error}")
        return None
 
 
def filter_bad_logs(log_contents):
    lines = log_contents.splitlines()
    total = len(lines)
    filtered = [line for line in lines if "WARNING" in line or "CRITICAL" in line]
    count = len(filtered)
    if not filtered:
        print("[AI-SOC] No suspicious activity found in today's logs")
        return None
    print(f"[AI-SOC] Filtered {count} suspicious entries from {total} total log lines")
    return "\n".join(filtered)
 
 
def upload_filtered_logs(filtered_contents):
    try:
        client = BlobServiceClient.from_connection_string(connection_string)
        container = client.get_container_client(FILTERED_LOGS_CONTAINER)
        blob_name = f"{today}-filtered.txt"
        data = filtered_contents.encode("utf-8")
        container.upload_blob(blob_name, data, overwrite=True)
        print(f"[AI-SOC] Filtered logs uploaded to filtered-logs container: {blob_name}")
    except Exception as error:
        print(f"[AI-SOC] Upload failed: {error}")
 
 
def run_pipeline():
    log_contents = download_logs()
    if log_contents is None:
        print("[AI-SOC] Pipeline stopped — no logs available")
        return
 
    filtered_contents = filter_bad_logs(log_contents)
    if filtered_contents is None:
        print("[AI-SOC] Pipeline stopped — no suspicious activity today")
        return
 
    upload_filtered_logs(filtered_contents)
    print("[AI-SOC] Pipeline trigger complete — Eduardo-agent will process filtered-logs automatically")
 
 
if __name__ == "__main__":
    run_pipeline()