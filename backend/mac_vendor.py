import requests


def get_vendor(mac):

    try:

        url = f"https://api.macvendors.com/{mac}"

        response = requests.get(
            url,
            timeout=3
        )

        if response.status_code == 200:
            return response.text

    except:
        pass

    return "Unknown"