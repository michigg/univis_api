from enum import Enum


class RoomUtil(str, Enum):
    BEAM: str = "Projektor"
    DBEAM: str = "Doppelprojektion"
    OHEAD: str = "Overheadprojektor"
    DARK: str = "Verdunkelung"
    LOSE: str = "lose Bestuhlung"
    SMART: str = "Interaktive Tafel"
    VISU: str = "DocCam"
    MIKR: str = "Pultmikrofon"
    PC: str = "Interner PC"
    BLUERAY: str = "Blu-Ray Player"
    DVD: str = "DVD Player"
    PRUEF: str = "Prüfungsraum"


ROOM_UTIL_MAP = {"beam": RoomUtil.BEAM, "dbeam": RoomUtil.DBEAM, "ohead": RoomUtil.OHEAD, "dark": RoomUtil.DARK,
                 "lose": RoomUtil.LOSE, "smart": RoomUtil.SMART, "visu": RoomUtil.VISU, "mikr": RoomUtil.MIKR,
                 "pc": RoomUtil.PC, "blueray": RoomUtil.BLUERAY, "dvd": RoomUtil.DVD, "pruef": RoomUtil.PRUEF}
