
from attck_pe.planner import client

def fetch_techniques():
    try:
        return client.get_techniques()
    except Exception as e:
        raise RuntimeError(f"Error fetching techniques: {e}")
