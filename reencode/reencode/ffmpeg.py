
import logging
import shlex
import subprocess
import time

from .utils import wrap_command

logger = logging.getLogger(__name__)


class FFMpeg:
    def __init__(self, input_path, output_path):
        if not input_path.is_file():
            raise RuntimeError("Input file not found: %s", input_path)
        self.input_path = input_path

        if output_path.exists():
            raise RuntimeError("Output file alread exists: %s", output_path)
        self.output_path = output_path

    def run(self, dry_run=False):
        start = time.perf_counter()
        logger.info("Encode: %s", self.input_path.name)
        self.encode(dry_run)
        elapsed = time.perf_counter() - start
        logger.debug("Command ran in %.2f seconds", elapsed)

    def encode(self, dry_run):
        args = (
            'ffmpeg',
            '-hide_banner',
            '-v', 'quiet',
            '-stats',
            '-i', str(self.input_path),
            '-c:v', 'libx265',
            '-x265-params', 'log-level=warning',
            '-preset', 'slow',
            '-crf', '26',
            '-ac', '2',
            '-c:a', 'copy',    #'aac',
            # ~ '-b:a', '160k',
            str(self.output_path),
        )

        command = shlex.join(args)
        print(wrap_command(command, width=80))

        if dry_run:
            return

        try:
            result = subprocess.run(args, check=True)
        except subprocess.CalledProcessError as e:
            pp(e)
            pp(e.stdout)
            pp(e.stderr)
            raise
        return result.stdout
