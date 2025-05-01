# Jamf Pro Smart Group Unmanage Script

This script automatically **unmanages computers** in a specified **Smart Group** in Jamf Pro that have not checked in for over **120 days**. It uses the Jamf Pro API to identify devices and runs the unmanage process in parallel for improved performance.

> ⚠️ Use with caution: This script performs administrative actions on Jamf-managed devices.

---

## 🔧 Features

- Authenticates with Jamf Pro API using basic credentials and token-based auth
- Fetches all devices from a specific Smart Group (by ID)
- Unmanages devices via Jamf Pro API
- Supports parallel execution using threads (configurable)

---

## 🚀 Prerequisites

- Python 3.6+
- Jamf Pro admin API credentials
- The group ID of the Smart Group you want to target (retrievable from the group’s URL)

---

## 📦 Installation

Clone this repository or download the script:

```bash
git clone https://github.com/yourusername/jamf-unmanage-script.git
cd jamf-unmanage-script
```

Install required Python packages (usually included with Python):

```bash
pip install requests
```

---

## ⚙️ Usage

1. Open the script in a text editor and update the `BASE_URL` and `GROUP_ID` variables:

```python
BASE_URL = "https://your.jamf.server"
GROUP_ID = 188  # Your target Smart Group ID
```

2. Run the script:

```bash
python unmanage_smart_group.py
```

3. Enter your Jamf Pro API credentials when prompted.

---

## 📌 Notes

- Devices are selected based on the Smart Group’s criteria (e.g., last check-in date).
- The XML payload used sets the device as **unmanaged**, without deleting it.
- Max threads (`MAX_THREADS`) is configurable; default is 10.

---

## 🛡️ Security

- Credentials are **not stored**—they're entered at runtime.
- No sensitive information is logged or saved.
- Ensure this script is run in a secure environment.

---

## 🧑‍💻 Author

**westrm**  
Version 1.0

---

## 📄 License

This project is released under the MIT License.
