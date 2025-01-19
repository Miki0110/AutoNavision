import pyperclip

header_row = (
    "Bogføringsdato\tOrdretype\tOrdrenr.\tSagBeskrivelse\tOrdrelinjenr.\tOrdreLinSøgeBeskrivelse\tOperationsnr.\tType\tNummer\tBeskrivelse\tNormaltid (timer)\tOvertid 1 (timer)\tOvertid 2 (timer)\tKørsel normaltid (timer)\tKørsel overtid 1 (timer)\tKørsel overtid 2 (timer)\tAntal km egen bil\tAntal km firmabil\tBil nummerplade\tFRA Adresse type\tKørsel FRA\tTIL Adresse type\tKørsel TIL\tUdkald\tVagttillæg 1 (timer)\tVagttillæg 2 (timer)\tVareantal\tLokation\tTillægstype\tRessourcegruppenr.\tUdetid\tService weekend turnus"
)

data_row_1 = (
    "12-01-25\tSag\t010-23-4463\tARLA BRANDERUP - 2,3 kg. prod. linje\t700300\tIndkøring, SSY (indkøring)\t\tRessource\tF3073\tMiki Barlach Pregaard\t2,00\t2,00\t0,00\t4,00\t4,00\t0,00\t0,00\t0,00\t\t \t\t \t\t \t0,00\t0,00\t0,00\t\t\tPROGRAM\tNej\tNej"
)

# Combine the rows with newlines
tab_separated_data = f"{header_row}\r\n{data_row_1}"

# Get the current clipboard contents
# Make sure you copied from Navision before running this script
old_data = pyperclip.paste().encode('utf-8')
new_data = tab_separated_data.encode('utf-8')

min_len = min(len(old_data), len(new_data))

differences_found = False
for i in range(min_len):
    if old_data[i] != new_data[i]:
        differences_found = True
        print(
            f"Difference at byte {i}: "
            f"old={old_data[i]!r}, new={new_data[i]!r}"
        )
        break

if not differences_found and len(old_data) != len(new_data):
    print("The strings match for their entire common length, but have different lengths.")
elif not differences_found:
    print("No differences found at the byte level!")


pyperclip.copy(tab_separated_data)