from src.energyml.utils.epc import Epc


def import_modules():
    import energyml.opc.opc
    import energyml.resqml.v2_0_1.resqmlv2


if __name__ == "__main__":
    # import_modules()
    epc201 = Epc.read_file(
        "D:/Geosiris/OSDU/manifestTranslation/#Data/VOLVE_STRUCT.epc"
    )
    print(epc201)
