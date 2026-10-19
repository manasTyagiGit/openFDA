import requests
import json
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

OPENFDA_FILE_PATH = "/home/manas_tyagi/Workspace/Commons/openFDA/src/openfda/data/data_openFDA.json"
OPENFDA_API_BASE = "https://api.fda.gov/drug/event.json"
OPENFDA_API_PARAMS = {'limit' : '10'}

CTGOV_FILE_PATH = "/home/manas_tyagi/Workspace/Commons/openFDA/src/openfda/data/data_ctgov.json"
CTGOV_API_BASE = "https://clinicaltrials.gov/api/v2/studies"
CTGOV_API_PARAMS = {'pageSize' : '21'}

INDENT = 4
TIMEOUT = 10

def save_files(json_data_stream, FILE_PATH) :
    try :
        with open(FILE_PATH, "w") as FILE_HANDLER:
            json.dump(json_data_stream, FILE_HANDLER, indent=INDENT)

    except Exception as e :
        print(e)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=4),
    retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.Timeout)),
    reraise=True
)
def get_api_data() :
    try:
        resp_client_fda = requests.get(f"{OPENFDA_API_BASE}", params=OPENFDA_API_PARAMS, timeout=TIMEOUT)
        resp_client_fda.raise_for_status()

        return resp_client_fda.json()
    
    except Exception as e :
        print(e)
        return None

def fetch_openfda_data() :
    try :
        api_data = get_api_data()
        save_files(api_data, OPENFDA_FILE_PATH)
        return True
    
    except Exception as e :
        print(e)
        return False    

def fetch_ctgov_data() :
    try:
        resp_client_ctgov = requests.get(f"{CTGOV_API_BASE}", params=CTGOV_API_PARAMS, timeout=TIMEOUT)
        resp_client_ctgov.raise_for_status()

        ctgov_json_data = resp_client_ctgov.json()

        save_files(ctgov_json_data, CTGOV_FILE_PATH)
        
        return True
    except Exception as e :
        print(e)
        return False

def main() -> None :
    fda_status = fetch_openfda_data()

    if not fda_status :
        print("Failed to get FDA Data")
    else :
        print(f"FDA data is saved at {OPENFDA_FILE_PATH}")

    ctgov_status = fetch_ctgov_data()

    if not ctgov_status :
        print("Failed to get CTGOV Data")
    else :
        print(f"CTGOV data is saved at {CTGOV_FILE_PATH}")



if __name__ == "__main__" :
    main()