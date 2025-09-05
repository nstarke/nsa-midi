from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os, argparse, requests

# Adapted from https://gist.github.com/geobabbler/5a0a03827792a3f1915897e94416edb5

def get_extension(url):
    path = urlparse(url).path   # extract the path part of the URL
    _, ext = os.path.splitext(path)  # split filename and extension
    return ext

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to download an image
def download_image(image_url, save_path):
    try:
        response = requests.get(image_url, headers=headers, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded {save_path}")
    except Exception as e:
        print(f"Failed to download {image_url}. Error: {e}")

# Function to get image URLs from Wikimedia Commons search results
def get_image_urls(search_url, max_images=10):
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.find_all('img', {'class': 'sd-image'}, limit=max_images)
    image_urls = [img['src'] for img in image_tags]
    return image_urls

def main():
    parser = argparse.ArgumentParser(description="Process query parameters.")

    # First parameter: query (string)
    parser.add_argument(
        "query",
        type=str,
        help="Search query string"
    )

    # Second parameter: count (integer)
    parser.add_argument(
        "count",
        type=int,
        help="Number of items to return (must be an integer)"
    )

    # Third parameter: type (choice of audio, video, image)
    parser.add_argument(
        "type",
        choices=["audio", "video", "image"],
        help="Type of item (must be one of: audio, video, image)"
    )

    parser.add_argument(
        "output_dir",
        type=str,
        help="Directory to save the output files"
    )

    args = parser.parse_args()  
    os.makedirs(args.output_dir, exist_ok=True)

    # Get image URLs
    search_url = f"https://commons.wikimedia.org/w/index.php?search={args.query}&title=Special:MediaSearch&go=Go&type=image"
    file_urls = get_image_urls(search_url, args.count)

    l = len(str(args.count))
    # Download images
    for idx, file_url in enumerate(file_urls):
        ext = get_extension(file_url)
        save_path = os.path.join(args.output_dir, f"{args.query}_{args.type}_{(idx+1).rjust(l)}{ext}")
        download_image(file_url, save_path)

if __name__ == "__main__":
    main()