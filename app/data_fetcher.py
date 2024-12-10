
from attck_planner.planner import client

def fetch_techniques():
    try:
        return client.get_techniques()
    except Exception as e:
        raise RuntimeError(f"Error fetching techniques: {e}")
