
#AI-SOC
#this scripts generates a daily realistic security Log files
#containing both normal and random attacks

import logging #writes log messages to files
import os #interacts with the operating system
import random
from datetime import datetime

from faker import Faker  #third party library that generates realistic data
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# ── Setup & Configuration ─────────────────────

fake = Faker() 


os.makedirs("logs", exist_ok=True) #Creats a logs folder if it does not already exist.


today = datetime.now().strftime("%Y-%m-%d") #This gets todays dates and formast it as YYYY-MM-DD
log_filename = f"logs/{today}.txt" #this builds the file path for the current days log file

# Configure the root logger
logging.basicConfig( #This allows to configure the logging ystem in order to have it known where to write and how to format them
    filename=log_filename,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

load_dotenv() #This line reads the .env file and loads the contents into here so that python can use it
connection_string=os.getenv("AZURE_STORAGE_CONNECTION_STRING") #This grabs the string without actually showing it in the script
#Pulls out the actual connection string put inside that variable
container_name="daily-logs" #makes a new varaible for the actual container name

#Function 1: Normal Activity (SImuilates regular log traffic)

def generate_normal_logs():
    """Emit five realistic INFO-level log entries."""

    # 1. Successful SSH login
    logging.info(
        f"Successful SSH login from {fake.ipv4()} for user {fake.user_name()}"
    )

    # 2. Successful HTTP GET
    logging.info(
        f"HTTP GET {fake.uri()} from {fake.ipv4()} — 200 OK"
    )

    # 3. Successful HTTP POST
    logging.info(
        f"HTTP POST {fake.uri()} from {fake.ipv4()} — 200 OK"
    )

    # 4. Routine database connection
    logging.info(
        f"Database connection established by {fake.user_name()} on host {fake.hostname()}"
    )

    # 5. Scheduled task completion
    job_name = f"job_{fake.word()}_{random.randint(100, 999)}"
    completed_at = fake.date_time_this_month().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(
        f"Scheduled task '{job_name}' completed successfully at {completed_at}"
    )


#Function 2: Attack Sequences(Simulates multiple different attack log)

def generate_attack_logs():
    """Emit a full set of attack-pattern log entries."""

    # ── 2a. SSH Brute-Force 
    brute_ip = fake.ipv4()
    brute_user = fake.user_name()

    for _ in range(5):
        logging.warning(
            f"Failed login attempt from {brute_ip} for user {brute_user}"
        )

    logging.critical(
        f"Successful root login after brute force from {brute_ip} targeting user {brute_user}"
    )

    # ── 2b. Port Scan Detection
    scan_ip = fake.ipv4()
    common_ports = [21, 22, 23, 80, 443, 3306, 5900, 8080]
    logging.warning(
        f"Port scan detected from {scan_ip} — probed ports: {common_ports}"
    )

    # ── 2c. FTP Backdoor Exploit (CVE-2011-2523) ──
    attacker_ip = fake.ipv4()
    target_ip = fake.ipv4()
    logging.critical(
        f"CVE-2011-2523 vsftpd backdoor triggered by {attacker_ip} against {target_ip} "
        f"— root shell established on port 6200"
    )

    # ── 2d. SQL Injection Attempt 
    sqli_ip = fake.ipv4()
    payload = "' OR 1=1 --"
    logging.warning(
        f"SQL injection attempt from {sqli_ip} — malicious payload detected: {payload}"
    )

    # ── 2e. Privilege Escalation ──────────────
    escalating_user = fake.user_name()
    logging.critical(
        f"Privilege escalation detected: user '{escalating_user}' successfully escalated to root"
    )


#Function 3:Upload to blob(This will automatically upload all the logs to Blob storage)

def upload_to_blob():
    try:
        blob_service_client=BlobServiceClient.from_connection_string(connection_string) #This logs into the Azure storage account using the connection string
        container_client=blob_service_client.get_container_client(container_name) #This sets the location to the actual container in which we will be updating to
        blob_name=os.path.basename(log_filename) #strips the path into just the actual name of the text file instead of the whole path
        
        with open(log_filename, "rb") as log: #azure needs raw bytes so we open it as binary
            container_client.upload_blob(blob_name, log, overwrite=True) #THIS uploads what to name the file in Azure, the file contents, and makes it so that
            #if the script is ran twice the previous data is overwritten and the old file is replace as to not cause an error

        print(f'Upload complete -{blob_name} uploaded to {container_name}')




    except Exception as e:
        print(f'UPLOAD FAILED - {e}')


#Function 4: Daily Log Orchestrator(Actually calls both functions and randomises the daily logs)

def generate_daily_logs():
    """
    Compose a full daily log file:
      - one pass of normal activity
      - 1–3 randomly selected attack sequences
    """
    generate_normal_logs()

    attack_count = random.randint(1, 3)
    for _ in range(attack_count):
        generate_attack_logs()

    print(
        f"[AI-SOC] Log generation complete.\n"
        f"  File    : {log_filename}\n"
        f"  Attacks : {attack_count} sequence(s) embedded\n"
        f"  Entries : see file for full detail"
    )

    upload_to_blob()



# ── Entry Point ───────────────────────────────



if __name__ == "__main__":
    generate_daily_logs()