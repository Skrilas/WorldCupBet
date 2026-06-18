from services.time_service import TimeService
import requests

if __name__ == "__main__":
    TimeService.criar_times()

    # print(requests.get("https://1.1.1.1", timeout=10).status_code)
    # print(requests.get("https://google.com", timeout=10).status_code)