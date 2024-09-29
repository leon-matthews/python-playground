
from dataclasses import dataclass
import json
import logging
import subprocess
import time


logger = logging.getLogger(__name__)


@dataclass
class MediaInfo:
    """
    Basic information about media file.
    """
    audio_codec: str            # eg. 'aac'
    bitrate: int                # bits per second
    duration: float             # seconds
    height: int                 # pixels
    num_streams: int
    size: int                   # bytes
    video_codec: str            # eg. 'h264'
    width: int                  # pixels


class FFProbe:
    def __init__(self, path):
        self.path = path

    def run(self):
        # Run command
        start = time.perf_counter()
        stdout = self.ffprobe(self.path)
        elapsed = time.perf_counter() - start
        logger.debug("Command ran in %.2f seconds", elapsed)

        # Process results
        data = self.load_json(stdout)
        self.mediainfo = self.get_media_info(data)
        return self.mediainfo

    def get_media_info(self, data):
        """
        Build a `MediaInfo` instance from raw JSON data.

        Raises:
            `RuntimeError` if there are an unexpected number of streams.

        Args:
            data (dict): Raw data from ``ffmpeg`` command.

        Returns (MediaInfo): Basic media information.
        """
        # Format
        f = data['format']
        bitrate = f['bit_rate']
        duration = f['duration']
        size = f['size']

        # Streams
        streams = data['streams']
        num_streams = len(streams)
        if num_streams != 2:
            raise RuntimeError("Unexpected number of streams: %s", num_streams)
        for stream in streams:
            is_video = 'width' in stream
            if is_video:
                video_codec = stream['codec_name']
                height = stream['height']
                width = stream['width']
            else:
                audio_codec = stream['codec_name']

        # MediaInfo
        info = MediaInfo(
            audio_codec=audio_codec,
            bitrate=int(bitrate),
            duration=float(duration),
            height=int(height),
            num_streams=num_streams,
            size=int(size),
            video_codec=video_codec,
            width=int(width),
        )
        return info

    def load_json(self, stdout):
        data = json.loads(stdout)
        return data

    def ffprobe(self, path):
        """
        Run ``ffprobe`` and parse results as json.

        Args:
            path (Path): Path to media file.

        Returns (bytes):
            STDOUT from command.
        """
        args = (
            'ffprobe',
            '-v', 'error',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            path,
        )
        try:
            result = subprocess.run(args, capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            pp(e)
            pp(e.stdout)
            pp(e.stderr)
        return result.stdout
