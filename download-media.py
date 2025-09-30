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

def get_audio_urls(search_url, max_audios=10):
    # sdms-audio-result__title
    audio_urls = []
    offset = 0
    audios_per_page = 40  # Wikimedia Commons returns 40 audios per page

    while len(audio_urls) < max_audios:
        paginated_url = search_url + f"&offset={offset}"
        response = requests.get(paginated_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        audio_tags = soup.find_all('h3', {'class': 'sdms-audio-result__title'})

        if not audio_tags:
            break

        page_urls = []
        for h3 in audio_tags:
            if len(audio_urls) + len(page_urls) >= max_audios:
                break
            a_tag = h3.find('a')
            if a_tag and 'href' in a_tag.attrs:
                url = a_tag['href']
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                download_tags = soup.find_all('div', {'class': 'fullMedia'})
                for download_tag in download_tags:
                    a_tag2 = download_tag.find('a', {'class': 'internal'})
                    if a_tag2 and 'href' in a_tag2.attrs:
                        tag = a_tag2['href']
                        if 'upload.wikimedia.org' in tag:
                            page_urls.append(tag)
                            break

        audio_urls.extend(page_urls)
        print(f"Fetched {len(page_urls)} audio URLs from page {offset // audios_per_page + 1} (offset {offset})")

        if len(audio_tags) < audios_per_page:
            break

        offset += audios_per_page

    return audio_urls[:max_audios]

def get_video_urls(search_url, max_videos=10):
    # sdms-audio-result__title
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    video_tags = soup.find_all('div', {'class': 'sdms-search-results__list--video'}, limit=max_videos)
    res = []
    for div in video_tags:
        v_tag = div.find('a', {'class': 'sdms-video-result'})
        if v_tag and 'href' in v_tag.attrs:
            url = v_tag['href']
            url_ext = get_extension(url).lower()
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            download_tags = soup.find_all('a')
            for download_tag in download_tags:
                tag = download_tag.get('href', '')
                ext = get_extension(tag).lower()
                if 'upload.wikimedia.org' in tag and url_ext == ext:
                    res.append(tag)
    return res

# Function to get image URLs from Wikimedia Commons search results
def get_image_urls(search_url, max_images=10):
    image_urls = []
    offset = 0
    images_per_page = 40  # Wikimedia Commons returns 40 images per page

    while len(image_urls) < max_images:
        # Add offset parameter for pagination
        paginated_url = search_url + f"&offset={offset}"
        response = requests.get(paginated_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get all images on this page
        image_tags = soup.find_all('img', {'class': 'sd-image'})

        if not image_tags:
            # No more images found, break the loop
            break

        # Extract URLs from this page
        page_urls = [img['src'] for img in image_tags]
        image_urls.extend(page_urls)

        print(f"Fetched {len(page_urls)} URLs from page {offset // images_per_page + 1} (offset {offset})")

        # If we got fewer than expected images, we've reached the end
        if len(page_urls) < images_per_page:
            break

        offset += images_per_page

    # Return only the requested number of images
    return image_urls[:max_images]

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
    search_url = f"https://commons.wikimedia.org/w/index.php?search={args.query}&title=Special:MediaSearch&go=Go&type={args.type}"
    if args.type == "image":
        file_urls = get_image_urls(search_url, args.count)
    elif args.type == "audio":
        # Placeholder: implement get_audio_urls if needed
        file_urls = get_audio_urls(search_url, args.count)
    elif args.type == "video":
        # Placeholder: implement get_video_urls if needed
        file_urls = get_video_urls(search_url, args.count)  # Replace with actual function to get video URLs

    l = len(str(args.count))
    # Download images
    for idx, file_url in enumerate(file_urls):
        ext = get_extension(file_url)
        save_path = os.path.join(args.output_dir, f"{args.query}_{args.type}_{str(idx+1).rjust(l, '0')}{ext}")
        download_image(file_url, save_path)

if __name__ == "__main__":
    main()
