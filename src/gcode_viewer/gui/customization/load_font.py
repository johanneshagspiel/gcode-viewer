"""
A helper module for loading custom font files for Tkinter on Windows.
The contents of this file are adapted from
https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
"""
import platform
from ctypes import byref, create_unicode_buffer, windll
from pathlib import Path

FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20


def load_font(font_path: Path, private: bool = True, enumerable: bool = True) -> int:
	"""
    Makes fonts located in the specified file available to the font system.
    See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx

    :param font_path: Path of the font file.
    :param private: If True, other processes cannot see this font, and this font will be unloaded when the process dies.
    :param enumerable: If True, this font will appear when enumerating fonts.
    :return: The number of fonts added.
    """

	# If not on Windows we assume that the desired font is already available
	if platform.system() != "Windows":
		return 0

	path_buf = create_unicode_buffer(str(font_path))
	add_font_resource_ex = windll.gdi32.AddFontResourceExW

	flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
	return add_font_resource_ex(byref(path_buf), flags, 0)
