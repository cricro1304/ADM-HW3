import regex as re

def trova_simboli_e_valori(testo):
    pattern = re.compile(r'(\p{Sc})?(\d+(?:,\d{3})*(?:\.\d{1,2})?)(?(1)|\s*(\p{Sc}))', re.UNICODE)
    risultati = pattern.findall(testo)
    
    # Crea una lista di tuple contenenti sia il simbolo di valuta che il valore numerico
    risultati_list = []
    for match in risultati:
        # Se il primo gruppo di cattura è vuoto, usa il terzo gruppo
        simbolo = match[0] if match[0] else match[2]
        
        # Converti il valore in float
        valore = float(match[1].replace(',', ''))
        
        risultati_list.append([simbolo, valore])
    
    return risultati_list

# Esempio di utilizzo
testo_di_esempio = "UK Students Full time: £9750 for the 2022/202300 academic year Part time: £1580 per 15 credits for the Individual Research Project for the 2022/2023 academic year EU Students Full time: £14750 for the 2022/2023 academic year Part time: £1230 per 15 credits for the 2022/2023 academic year"
risultati = trova_simboli_e_valori(testo_di_esempio)

print("Simboli di valute e valori numerici trovati:")
for simbolo, valore in risultati:
    print(f"{simbolo}: {valore}")

max_val = max(risultati, key=lambda x: x[1])[1]

print(f"Il massimo degli elementi in posizione 1 è: {max_val}")
