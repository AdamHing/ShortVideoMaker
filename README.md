# ShortVideoMaker


# Video Processing Application

This Python script provides a graphical user interface (GUI) for processing video data, including downloading, clipping, stitching, and adding captions. The GUI is built using the Tkinter library.

## Prerequisites

Before using this application, make sure you have the following dependencies installed:

- `tkinter`: The standard GUI toolkit for Python.
- `pytube`: A lightweight, dependency-free Python library for downloading YouTube videos.
- `BlackSubtitles.VideoTranscriber`: A module for video transcription.
- `VideoClips.Clipper` and `VideoClips.Stitcher`: Modules for clipping and stitching video clips.

You can install the required dependencies using:

```bash
pip install tkinter pytube
```

## How to Use

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/AdamHing/ShortVideoMaker.git
   cd ShortVideoMaker
   ```

2. **Run the Application:**
   ```bash
   python GUI.py
   ```

3. **Fill in the GUI Form:**
   - Enter the main video link in the "MainVideo" field.
   - Optionally, provide a link to another video in the "OtherVideo" field.
   - Specify the number of clips desired in the "Number of Clips" field.
   - Set the timestamp format in the "Timestamp Format" field.
   - Check the "Captions" box if you want to include captions.

4. **Click "Create":**
   - Press the "Create" button to start the video processing.

5. **Review Output:**
   - The script will print information about the processing steps, and the final output will be available in the specified output directories.

## Notes

- The script uses a dark-themed GUI for a better user experience.
- Make sure to provide valid video links and follow the on-screen instructions.
- Some functionality (commented-out lines) might be incomplete or optional.

