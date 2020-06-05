
file = open("C:\\Users\\maite\\Blok8\\GenPanels_merged_DG-2.17.0.txt")
gennamen = []
for regel in file:
    if regel.startswith("Symbol_HGNC"):
        print("Dit zijn alle genen: ")
    else:
        genpanel = regel.split("\t")
        gennaam = genpanel[0]
        gennamen.append(gennaam)

print(gennamen)