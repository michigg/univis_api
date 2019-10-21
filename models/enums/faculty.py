from enum import Enum


class Faculty(Enum):
    GuK = "Fakultät Geistes- und Kulturwissenschaften"
    SoWi = "Fakultät Sozial- und Wirtschaftswissenschaften"
    HuWi = "Fakultät Humanwissenschaften"
    WIAI = "Fakultät Wirtschaftsinformatik"


CHOICES = {
    "GuK": Faculty.GuK.value,
    "SoWi": Faculty.SoWi.value,
    "HuWi": Faculty.HuWi.value,
    "WIAI": Faculty.WIAI.value
}
