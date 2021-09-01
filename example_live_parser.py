import traceback
from pathlib import Path
from string import ascii_uppercase, ascii_lowercase
from time import sleep
import platform

from live.parser import LiveLogParser


def main():
    """
        ----------------------------------------------------------------------
        LiveLogParser assumes that you"ve configured Power.log to be a symlink.

        In "SOME_PATH/Hearthstone/Logs" folder:
            ln -s Power.log /tmp/hearthstone-redirected.log

        This will redirect all data coming into Power.log
        so we can access it from a RAM disk.
        ----------------------------------------------------------------------
        For better performance make /tmp of type tmpfs (or another location)

        In /etc/fstab add line:
            tmpfs	/tmp	tmpfs	nodev,nosuid,size=1G	0	0

        This will create in-memory storage which is faster then SSD.
        You need to restart the computer for this to take effect.
        ----------------------------------------------------------------------
    """
    system = platform.system()

    hs_path = None
    if system == 'Darwin':
        hs_path = Path('/') / 'Applications' / 'Hearthstone' / 'Logs' / 'Power.log'
    elif system == 'Windows':
        for Disk in ascii_uppercase:
            hs_path = Path(f'{Disk}:\\') / 'Program Files (x86)' / 'Hearthstone' / 'Logs' / 'Power.log'
            if hs_path.exists():
                break
    elif system == 'Linux':
        if 'Microsoft' in platform.release():
            for Disk in ascii_lowercase:
                hs_path = Path('/') / 'mnt' / Disk / 'Program Files (x86)' / 'Hearthstone' / 'Logs' / 'Power.log'
                if hs_path.exists():
                    break

    live_parser = None
    try:
        live_parser = LiveLogParser(hs_path)
        live_parser.start()

        while True:
            sleep(1)

    except Exception as e: # noqa
        print(traceback.format_exc())
        live_parser.stop()


if __name__ == "__main__":
    main()
