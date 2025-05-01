import requests
import getpass

from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor, as_completed

"""
    Automatically unmanages computers in a specific smart group (ID: 188)
    in Jamf Pro that have not checked in for more than 120 days. It authenticates with the
    Jamf Pro API, retrieves the list of computers in the group, and unmanages them in parallel.

    You can find your group ID from the smart group's URL
    Ex: https://[your.jamf.server]/smartComputerGroups.html?id=188&o=r

    @author westrm
    @version 1.0
"""

# Prompt for credentials
USERNAME = input("Enter your Jamf API Username: ")
PASSWORD = getpass.getpass("Enter your Jamf API Password: ")

BASE_URL = "https://your.jamf.server"
GROUP_ID = 188  # Adjust this as needed
MAX_THREADS = 10  # Tune this for your environment (5–10 is safe)

# Get a token using the Jamf Pro modern API
session = requests.Session()
auth_response = session.post(
    f"{BASE_URL}/api/v1/auth/token",
    auth=HTTPBasicAuth(USERNAME, PASSWORD)
)
auth_response.raise_for_status()
token = auth_response.json()["token"]

# Shared headers
session.headers.update({
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
    "Content-Type": "application/xml"
})

# Get smart group computers
group_url = f"{BASE_URL}/JSSResource/computergroups/id/{GROUP_ID}"
group_response = session.get(group_url)
group_response.raise_for_status()
computers = group_response.json()["computer_group"]["computers"]

# XML payload to unmanage
payload = """
<computer>
    <general>
        <remote_management>
            <managed>false</managed>
        </remote_management>
    </general>
</computer>
"""

# Unmanage function
def unmanage_device(comp):
    comp_id = comp["id"]
    comp_name = comp["name"]
    unmanage_url = f"{BASE_URL}/JSSResource/computers/id/{comp_id}"

    try:
        response = session.put(unmanage_url, data=payload)
        if response.status_code in (200, 201):
            return f"✓ {comp_name} unmanaged"
        else:
            return f"✗ {comp_name} failed ({response.status_code})"
    except Exception as e:
        return f"✗ {comp_name} error: {str(e)}"

# Run unmanage tasks in parallel
print(f"Unmanaging {len(computers)} devices using {MAX_THREADS} threads...\n")

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = [executor.submit(unmanage_device, comp) for comp in computers]
    for future in as_completed(futures):
        print(future.result())
