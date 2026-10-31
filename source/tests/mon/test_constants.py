import pytest

from DALI.forward_frame_16bit import DeviceType
from DALI.forward_frame_24bit import DeviceAddressType, EventType, InstanceAddressType
from DALI.forward_frame_25bit import DeviceClass


def constants(cls: type) -> dict[str, int]:
    return {name: value for name, value in vars(cls).items() if name.isupper()}


# the constants of each class have different values
@pytest.mark.parametrize(
    "cls",
    [DeviceType, EventType, InstanceAddressType, DeviceAddressType, DeviceClass],
)
def test_unique_values(cls):
    values = constants(cls)
    assert values, cls.__name__
    assert all(isinstance(value, int) for value in values.values())
    assert len(set(values.values())) == len(values), values
