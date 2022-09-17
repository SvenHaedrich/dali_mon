from logging import _Level
import source.DALI as DALI

def test_broadcast_dapc():
    frame = DALI.Raw_Frane()
    frame.length = 16
    for level in range(0,255):
        frame.data = 0xFE00 + _Level
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        target_command = "BC".ljust(10, " ") + F"DAPC {level}"
        assert decoded_command == target_command