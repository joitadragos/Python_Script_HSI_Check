# script that reads the pin configuration from WinIDEA
# This is a starting point for reading pin configuration
# Right now can only read 1-Bit SFRs, but can be extended to read multi-bit SFRs if needed. 

import isystem.connect as ic

winidea_id = ''


def read_sfr(dataCtrl2, top_group, sub_group, sfr_name, bit_size=1):
    """Return the integer value of an SFR, or None if not found."""
    cpuSfrs = dataCtrl2.getCPUSFRs(ic.IConnectEclipse.gcsSFRs)
    try:
        topGroups = cpuSfrs.SFRs()
        for i in range(topGroups.size()):
            if topGroups.at(i).Name() != top_group:
                continue
            subGroups = topGroups.at(i).SFRs()
            for j in range(subGroups.size()):
                if subGroups.at(j).Name() != sub_group:
                    continue
                sfrsInGroup = subGroups.at(j).SFRs()
                for k in range(sfrsInGroup.size()):
                    sfr = sfrsInGroup.at(k)
                    if sfr.Name() == sfr_name:
                        sType = ic.SType()
                        sType.m_byType    = ic.SType.tUnsigned
                        sType.m_byBitSize = bit_size
                        sfrData = dataCtrl2.readSFR(sfr.Handle(), sType)
                        return sfrData.getInt()
    finally:
        dataCtrl2.release(cpuSfrs)
    return None


if __name__ == "__main__":
    try:
        connMgr = ic.ConnectionMgr()
        connMgr.connect(ic.CConnectionConfig().instanceId(winidea_id))
        dataCtrl2 = ic.CDataController2(connMgr)

        # value = read_sfr(dataCtrl2, "PORT0", "PFCE02", "PFCE02_1", bit_size=1)
        value = read_sfr(dataCtrl2, "PORT0", "PM02", "PM02", bit_size=1)
        if value is None:
            print("SFR not found.")
        else:
            print("Reading 'PM02_1'...")
            print("\tValue:    {}".format(value))
    except Exception as e:
        print("Error: {}".format(e))
    finally:
        input("\nPress Enter to exit...")
