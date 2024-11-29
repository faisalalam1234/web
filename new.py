import streamlit as st
import yt_dlp
import time

def fetch_resolutions(url):
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])

        available_formats = []
        for format in formats:
            format_note = format.get('format_note', 'N/A')
            height = format.get('height', 'N/A')  # Some formats might not have a height
            ext = format.get('ext', 'N/A')
            format_id = format.get('format_id')
            available_formats.append({
                'format_id': format_id,
                'format_note': format_note,
                'height': height,
                'ext': ext
            })
        return available_formats

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

def download_video(url, format_id):
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        ydl_opts = {
            'format': format_id,
            'noplaylist': True,
            'outtmpl': f'downloaded_video_{timestamp}.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return f"downloaded_video_{timestamp}.mp4"

    except Exception as e:
        st.error(f"Download failed: {str(e)}")
        return None

# Streamlit App
def main():
    st.title("YouTube Video Downloader")

    # Input URL
    url = st.text_input("Enter the YouTube Video URL:")

    if st.button("Fetch Resolutions"):
        if url:
            formats = fetch_resolutions(url)

            if formats:
                # Display available formats
                format_options = [
                    f"{fmt['format_note']} ({fmt['height']}p) - {fmt['ext']}"
                    for fmt in formats
                ]
                selected_option = st.selectbox("Select Resolution:", format_options)

                if selected_option:
                    selected_format = formats[format_options.index(selected_option)]
                    format_id = selected_format['format_id']

                    # Show the download button
                    if st.button("Download"):
                        with st.spinner("Downloading..."):
                            downloaded_file = download_video(url, format_id)
                            if downloaded_file:
                                with open(downloaded_file, "rb") as file:
                                    st.success("Download complete!")
                                    st.download_button(
                                        label="Download Video",
                                        data=file,
                                        file_name=downloaded_file,
                                        mime="video/mp4",
                                    )
        else:
            st.error("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()
