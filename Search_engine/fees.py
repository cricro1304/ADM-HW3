import regex as re

def trova_simboli_e_valori(testo):
    pattern = regex.compile(r'(\p{Sc})\s*([0-9,]+(?:\.\d{1,2})?)', re.UNICODE)
    risultati = pattern.findall(testo)
    risultati_list = [[simbolo, float(valore.replace(',', ''))] for simbolo, valore in risultati]
    return risultati_list


esempio = "Il prezzo è di $1000, $500.50 e $3000.75. e $400"
risultati = trova_simboli_e_valori(esempio)
print(risultati)
print("Simboli di valute e valori numerici trovati:")
for simbolo, valore in risultati:
    print(f"{simbolo}: {valore}")

max_val = float(max(risultati, key=lambda x: x[1])[1])
valuta_max_val=max(risultati, key=lambda x: x[1])[0]

print(max_val)
print(valuta_max_val)
print(str(valuta_max_val)+str(max_val))
