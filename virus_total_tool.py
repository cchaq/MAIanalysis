from typing import Literal
from langchain_core.tools import tool
import requests
import vt
import os

@tool
def getFileAttributes(file):
    """We will upload a file to VirusTotal via its API. 
    VirusTotal will then analyze it and provide its response. We will then use that response, analyze it further, 
    and provide the information to the user. This will help in understanding if the file provided is malicious, why it is deemed malicious, 
    and use the information from VirusTotal to provide additional information"""

    client = vt.Client(os.environ.get("VIRUS_TOTAL_API_KEY"))
    file_hash = "81f14d1e37afbbffff14a20a431fb0ac4b69adffe2c07de8bdf30c0de1bcf888" # testing purposes
    file_info = client.get_object(f"/files/{file_hash}")
    file_attributes = file_info.to_dict()
    return file_info
