import csv
import re
import isystem.connect as ic

INPUT_CSV   = r"C:\Data\_GITProj\Check_Pin_Config\Results.csv"
START_ROW   = 2           # skip header row
COL_A       = 0           # Pin Name
COL_B       = 1           # Pin Number  e.g. P02_0
COL_C       = 2           # Pin Function
COL_D       = 3           # Matched Label / Functionality
OUTPUT_CSV  = r"C:\Data\_GITProj\Check_Pin_Config\SFR_Comparison_Results.csv"

winidea_id  = ''

# Register types to read — order defines output column order (E‥K)
SFR_TYPES = ["P", "PM", "PFC", "PFCE", "PFCAE", "PFCEAE", "PMC"]

# Expected bit values for each alternative function mode (Table 2.20)
# Keys match AF labels that may appear in column D, e.g. "AF4_Out"
ALT_FUNC_EXPECTED = {
    "AF1_Out":  {"PFCEAE": 0, "PFCAE": 0, "PFCE": 0, "PFC": 0, "PM": 0},
    "AF1_In":   {"PFCEAE": 0, "PFCAE": 0, "PFCE": 0, "PFC": 0, "PM": 1},
    "AF2_Out":  {"PFCEAE": 0, "PFCAE": 0, "PFCE": 0, "PFC": 1, "PM": 0},
    "AF2_In":   {"PFCEAE": 0, "PFCAE": 0, "PFCE": 0, "PFC": 1, "PM": 1},
    "AF3_Out":  {"PFCEAE": 0, "PFCAE": 0, "PFCE": 1, "PFC": 0, "PM": 0},
    "AF3_In":   {"PFCEAE": 0, "PFCAE": 0, "PFCE": 1, "PFC": 0, "PM": 1},
    "AF4_Out":  {"PFCEAE": 0, "PFCAE": 0, "PFCE": 1, "PFC": 1, "PM": 0},
    "AF4_In":   {"PFCEAE": 0, "PFCAE": 0, "PFCE": 1, "PFC": 1, "PM": 1},
    "AF5_Out":  {"PFCEAE": 0, "PFCAE": 1, "PFCE": 0, "PFC": 0, "PM": 0},
    "AF5_In":   {"PFCEAE": 0, "PFCAE": 1, "PFCE": 0, "PFC": 0, "PM": 1},
    "AF6_Out":  {"PFCEAE": 0, "PFCAE": 1, "PFCE": 0, "PFC": 1, "PM": 0},
    "AF6_In":   {"PFCEAE": 0, "PFCAE": 1, "PFCE": 0, "PFC": 1, "PM": 1},
    "AF7_Out":  {"PFCEAE": 0, "PFCAE": 1, "PFCE": 1, "PFC": 0, "PM": 0},
    "AF7_In":   {"PFCEAE": 0, "PFCAE": 1, "PFCE": 1, "PFC": 0, "PM": 1},
    "AF8_Out":  {"PFCEAE": 0, "PFCAE": 1, "PFCE": 1, "PFC": 1, "PM": 0},
    "AF8_In":   {"PFCEAE": 0, "PFCAE": 1, "PFCE": 1, "PFC": 1, "PM": 1},
    "AF9_Out":  {"PFCEAE": 1, "PFCAE": 0, "PFCE": 0, "PFC": 0, "PM": 0},
    "AF9_In":   {"PFCEAE": 1, "PFCAE": 0, "PFCE": 0, "PFC": 0, "PM": 1},
    "AF10_Out": {"PFCEAE": 1, "PFCAE": 0, "PFCE": 0, "PFC": 1, "PM": 0},
    "AF10_In":  {"PFCEAE": 1, "PFCAE": 0, "PFCE": 0, "PFC": 1, "PM": 1},
    "AF11_Out": {"PFCEAE": 1, "PFCAE": 0, "PFCE": 1, "PFC": 0, "PM": 0},
    "AF11_In":  {"PFCEAE": 1, "PFCAE": 0, "PFCE": 1, "PFC": 0, "PM": 1},
    "AF12_Out": {"PFCEAE": 1, "PFCAE": 0, "PFCE": 1, "PFC": 1, "PM": 0},
    "AF12_In":  {"PFCEAE": 1, "PFCAE": 0, "PFCE": 1, "PFC": 1, "PM": 1},
    "AF13_Out": {"PFCEAE": 1, "PFCAE": 1, "PFCE": 0, "PFC": 0, "PM": 0},
    "AF13_In":  {"PFCEAE": 1, "PFCAE": 1, "PFCE": 0, "PFC": 0, "PM": 1},
    "AF14_Out": {"PFCEAE": 1, "PFCAE": 1, "PFCE": 0, "PFC": 1, "PM": 0},
    "AF14_In":  {"PFCEAE": 1, "PFCAE": 1, "PFCE": 0, "PFC": 1, "PM": 1},
    "AF15_Out": {"PFCEAE": 1, "PFCAE": 1, "PFCE": 1, "PFC": 0, "PM": 0},
    "AF15_In":  {"PFCEAE": 1, "PFCAE": 1, "PFCE": 1, "PFC": 0, "PM": 1},
    "AF16_Out": {"PFCEAE": 1, "PFCAE": 1, "PFCE": 1, "PFC": 1, "PM": 0},
    "AF16_In":  {"PFCEAE": 1, "PFCAE": 1, "PFCE": 1, "PFC": 1, "PM": 1},
}


def get_all_sfr_args(pin_number):
    """Convert 'P02_0' -> dict of {reg_type: (top_group, sub_group, sfr_name)}."""
    match = re.match(r'^P(\d+)_(\d+)$', pin_number.strip())
    if not match:
        return None
    port_num = match.group(1)
    bit_num  = match.group(2)
    top = "PORT0"
    return {
        "P":      (top, "P{}".format(port_num),      "P{}_{}".format(port_num, bit_num)),
        "PM":     (top, "PM{}".format(port_num),     "PM{}_{}".format(port_num, bit_num)),
        "PFC":    (top, "PFC{}".format(port_num),    "PFC{}_{}".format(port_num, bit_num)),
        "PFCE":   (top, "PFCE{}".format(port_num),   "PFCE{}_{}".format(port_num, bit_num)),
        "PFCAE":  (top, "PFCAE{}".format(port_num),  "PFCAE{}_{}".format(port_num, bit_num)),
        "PFCEAE": (top, "PFCEAE{}".format(port_num), "PFCEAE{}_{}".format(port_num, bit_num)),
        "PMC":    (top, "PMC{}".format(port_num),    "PMC{}_{}".format(port_num, bit_num)),
    }


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


def check_alt_function(val_d, sfr_values):
    """Return PASS/FAIL/'' by comparing SFR values against Table 2.20 expectations.

    Only runs when PMC=1 and an AF mode label (e.g. AF4_Out) is found in val_d.
    """
    if sfr_values.get("PMC", "") != "1":
        return ""

    match = re.search(r'(AF\d+_(Out|In))', val_d, re.IGNORECASE)
    if not match:
        return ""

    # Find the matching key in ALT_FUNC_EXPECTED (case-insensitive)
    af_label = match.group(1)
    af_key   = next((k for k in ALT_FUNC_EXPECTED if k.lower() == af_label.lower()), None)
    if af_key is None:
        return "Unknown: {}".format(af_label)

    expected   = ALT_FUNC_EXPECTED[af_key]
    mismatches = []
    for reg in ["PM", "PFC", "PFCE", "PFCAE", "PFCEAE"]:
        actual = sfr_values.get(reg, "")
        if actual == "":
            mismatches.append("{}: N/A".format(reg))
        elif int(actual) != expected[reg]:
            mismatches.append("{}: got {} exp {}".format(reg, actual, expected[reg]))

    return "PASS" if not mismatches else "FAIL ({})".format(", ".join(mismatches))


if __name__ == "__main__":
    try:
        connMgr   = ic.ConnectionMgr()
        connMgr.connect(ic.CConnectionConfig().instanceId(winidea_id))
        dataCtrl2 = ic.CDataController2(connMgr)

        rows = []
        with open(INPUT_CSV, newline="", encoding="cp1252") as f:
            reader = csv.reader(f)
            for row_num, row in enumerate(reader, start=1):
                if row_num < START_ROW:
                    continue
                val_a = row[COL_A] if len(row) > COL_A else ""
                val_b = row[COL_B] if len(row) > COL_B else ""
                val_c = row[COL_C] if len(row) > COL_C else ""
                val_d = row[COL_D] if len(row) > COL_D else ""

                all_args = get_all_sfr_args(val_b)
                if all_args:
                    sfr_values = {}
                    for reg_type in SFR_TYPES:
                        top_group, sub_group, sfr_name = all_args[reg_type]
                        result = read_sfr(dataCtrl2, top_group, sub_group, sfr_name, bit_size=1)
                        sfr_values[reg_type] = str(result) if result is not None else ""

                    check = check_alt_function(val_d, sfr_values)
                    print("{} -> {}  Check: {}".format(
                        val_b,
                        "  ".join("{}: {}".format(t, sfr_values[t]) for t in SFR_TYPES),
                        check if check else "N/A"
                    ))
                else:
                    print("Skipping unrecognised pin: '{}'".format(val_b))
                    sfr_values = {t: "" for t in SFR_TYPES}
                    check = ""

                rows.append(
                    (val_a, val_b, val_c, val_d) +
                    tuple(sfr_values[t] for t in SFR_TYPES) +
                    (check,)
                )

        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Pin Name", "Pin Number", "Pin Function", "Functionality"] +
                            SFR_TYPES + ["AF Check"])
            writer.writerows(rows)

        print("\nDone. {} rows written to {}".format(len(rows), OUTPUT_CSV))

    except Exception as e:
        print("Error: {}".format(e))
    finally:
        input("\nPress Enter to exit...")



