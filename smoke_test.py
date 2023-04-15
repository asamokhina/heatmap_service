import subprocess
import time
from contextlib import contextmanager
import requests


@contextmanager
def services(
    be_url="http://localhost:80", fe_url="http://localhost:3000", num_retries=20
):
    try:
        subprocess.run(["docker-compose", "up", "--build", "-d"], check=True)
        for i in range(num_retries):
            try:
                response = requests.get(f"{be_url}/api/org-ids")
                assert response.status_code == 200, f"Error: {response.status_code}"
                assert isinstance(response.json(), list)
                assert len(response.json()) > 0
                break
            except requests.RequestException:
                time.sleep(2)
        else:
            raise RuntimeError("Failed to reach the BE app")

        for i in range(num_retries):
            try:
                response = requests.get(fe_url)
                assert response.status_code == 200, f"Error: {response.status_code}"
                assert "<html" in response.content.decode()
                break
            except requests.RequestException:
                time.sleep(2)
        else:
            raise RuntimeError("Failed to reach the FE app")
        
        yield
    finally:
        # Stop Docker Compose services
        subprocess.run(["docker-compose", "down"])


if __name__ == "__main__":
    with services():
        print("Here can be more tests!")
    print("Done")