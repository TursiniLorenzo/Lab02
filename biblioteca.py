import csv

from charset_normalizer.md import annotations
numero_sezioni_biblioteca = 0 # Creo una variabile per memorizzare il numero di sezioni della biblioteca

def carica_da_file(file_path):
    """Carica i libri dal file"""
    global numero_sezioni_biblioteca
    with open (file_path, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        righe = list (reader)
        prima_riga = righe.pop(0)
        numero_sezioni_biblioteca = int (prima_riga [0]) # Aggiorno la variabile inizializzata all'esterno della
                                                         # funzione con il numero effettivo di sezioni
    return righe

def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    """Aggiunge un libro nella biblioteca"""
    riga = [titolo, autore, str(anno), str(pagine), str(sezione)]
    # Siccome i valori nel file sono tutti di tipo stringa, faccio in modo che anche quelli inseriti dall'utente
    # lo siano, infatti quando vengono inseriti, essendo valori numerici, vengono memorizzati come int e non come
    # stringhe
    if riga in biblioteca :
        return False # Se il libro è già presente nella biblioteca, la funzione restituisce come valore False, in modo
                     # da comunicare che non è stato possibile aggiungere il libro
    with open (file_path, "a", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(riga)
    # Se invece il libro non è presente nella biblioteca, allora sarà possibile aggiungerlo in questo modo, restituendo
    # come valore finale True
    return True

def cerca_libro(biblioteca, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""
    for row in biblioteca :
        if not row:
            continue # In modo da saltare righe nulle/vuote
        if titolo in row [0] : # Verifico che il titolo sia presente nel "vettore colonna" contenente tutti i titoli
                               # presenti nella biblioteca
            return row [0], row [1], row [2], row [3], row [4]
    return None

def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    sezioni = [[] for _ in range (numero_sezioni_biblioteca)] # Lista di liste vuote, in cui inserire i vari libri divisi in sezioni

    for riga in biblioteca :
        num_sezione = int (riga [4])
        sezioni [num_sezione - 1].append (riga) # Popolo le liste per ogni sezione

    if 1 <= sezione <= numero_sezioni_biblioteca: # Controllo che l'input dell'utente sia corretto
        return sorted (sezioni [sezione - 1]) # Restituisco la sezione richiesta dall'utente, ricordando di sottrarre
                                              # 1 all'indice che va da 0 a 4 e non da 1 a 5
    return None

def main():
    biblioteca = []
    file_path = "biblioteca.csv"

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca = carica_da_file(file_path)
                for riga in biblioteca:
                    print (" | ".join (riga))
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro (biblioteca, titolo, autore, anno, pagine, sezione, file_path)
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()

