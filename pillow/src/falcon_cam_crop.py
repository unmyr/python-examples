import datetime
import os

from PIL import Image


try:
    import win32_setctime
except ImportError:
    pass


def crop_image(base_dir: str, file_name: str):
    """Crop image."""
    source_path = os.path.join(base_dir, file_name)
    if not os.path.exists(source_path):
        return

    stat_obj = os.stat(source_path)
    mtime_infix = datetime.datetime.fromtimestamp(
        stat_obj.st_ctime
    ).strftime('%Y%m%d_%H%M%S')

    _base_name, ext = os.path.splitext(file_name)
    target_path = os.path.join(
        base_dir,
        'FalconCam_' + mtime_infix + ext
    )

    im = Image.open(source_path)
    im_crop = im.crop((269, 159, 269 + 1365, 159 + 768))
    im_crop.save(target_path)

    if os.name == 'nt':
        win32_setctime.setctime(source_path, stat_obj.st_ctime)
    os.utime(target_path, (stat_obj.st_atime, stat_obj.st_mtime))


def main():
    """Run main."""
    base_dir = 'D:/home/share/Downloads'
    for i in range(29, 30):
        crop_image(base_dir, f"Clipboard{i:02}.png")


if __name__ == '__main__':
    main()

# EOF
