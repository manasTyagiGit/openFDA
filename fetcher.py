import requests
import json

def main() :
    file_name="data.json"   
    response = requests.get("https://api.fda.gov/drug/event.json?limit=100")

    json_data = response.json()
    
    with open(file_name, "w") as file_handler :
        json.dump(json_data, file_handler)


if __name__ == "__main__" :
    main()