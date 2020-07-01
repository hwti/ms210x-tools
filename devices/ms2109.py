class Device():
    def __init__(self, hidraw):
        self._hidraw = hidraw

    def status(self):
        # Used as test by MacroSilicon
        if self.read_xdata_byte(0xF800) == 0xA7:
            state = 'OK'
        else:
            state = 'Incorrect test byte'
        print('MS2109 at {}, {}'.format(self._hidraw.devname, state))

    def read_xdata_byte(self, address):
        cmd = bytearray(3)
        cmd[0] = 0xb5
        cmd[1] = address >> 8
        cmd[2] = address & 0xff
        self._hidraw.send_feature_report(cmd)
        rsp = self._hidraw.get_feature_report(length=8)
        if rsp[0:3] != cmd[0:3]:
            raise Exception('Invalid response to {} command : {}'.format(cmd.hex(), rsp.hex()))
        return rsp[3]

    def write_xdata_byte(self, address, byte):
        cmd = bytearray(4)
        cmd[0] = 0xb6
        cmd[1] = address >> 8
        cmd[2] = address & 0xff
        cmd[3] = byte
        self._hidraw.send_feature_report(cmd)

    @staticmethod
    def eeprom_size():
        return 2048

    def read_eeprom_data(self, address):
        cmd = bytearray(8)
        cmd[0] = 0xe5
        cmd[1] = address >> 8
        cmd[2] = address & 0xff
        self._hidraw.send_feature_report(cmd)
        rsp = self._hidraw.get_feature_report(length=8)
        if rsp[0:3] != cmd[0:3]:
            raise Exception('Invalid response to {} command : {}'.format(cmd.hex(), rsp.hex()))
        return rsp[3:]

    def write_eeprom_data(self, address, data):
        assert len(data) == 2

        cmd = bytearray(8)
        cmd[0] = 0xe6
        cmd[1] = address
        cmd[2:] = data
        self._hidraw.send_feature_report(cmd)
