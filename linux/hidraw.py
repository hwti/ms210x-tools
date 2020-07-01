import fcntl
import os

from ioctl_opt import IOC, IOC_READ, IOC_WRITE

HIDIOCSFEATURE = lambda length: IOC(IOC_WRITE|IOC_READ, ord('H'), 0x06, length)
HIDIOCGFEATURE = lambda length: IOC(IOC_WRITE|IOC_READ, ord('H'), 0x07, length)

class HIDRaw():
    """Searches for a Linux hidraw device with the specifed VID/PID, and allows to send/get feature reports."""
    def __init__(self, vid=0, pid=0, devname=None):
        if devname is not None:
            self.devname = devname
        else:
            with os.scandir('/sys/class/hidraw') as devices:
                for entry in devices:
                    with open('/sys/class/hidraw/{}/device/modalias'.format(entry.name), 'r') as modalias:
                        if modalias.read().rstrip().endswith('v{:08X}p{:08X}'.format(vid, pid)):
                            self.devname = '/dev/' + entry.name
                            break
                else:
                    raise IOError('No device found')
        self._device = open(self.devname, 'r+b', buffering=0)

    def _ioctl(self, request, arg):
        result = fcntl.ioctl(self._device, request, arg)
        if result < 0:
            raise IOError(result)

    def send_feature_report(self, report, report_num=0):
        length = len(report) + 1
        buf = bytearray(length)
        buf[0] = report_num
        buf[1:] = report
        self._ioctl(HIDIOCSFEATURE(length), buf)

    def get_feature_report(self, length, report_num=0):
        buf = bytearray(length + 1)
        buf[0] = report_num
        self._ioctl(HIDIOCGFEATURE(length + 1), buf)
        return buf[1:]
