import os
import requests
from tqdm import tqdm

url = "https://huggingface.co/datasets/David-Egea/Creditcard-fraud-detection/resolve/main/creditcard.csv"
output_path = "creditcard.csv"

if os.path.exists(output_path):
    print(f"{output_path} already exists ({os.path.getsize(output_path)} bytes).")
else:
    print(f"Downloading {output_path} from Hugging Face...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))

    with open(output_path, "wb") as f, tqdm(
        total=total_size, unit='B', unit_scale=True, desc="creditcard.csv"
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))
    print(f"Successfully downloaded {output_path}! Size: {os.path.getsize(output_path)} bytes.")
