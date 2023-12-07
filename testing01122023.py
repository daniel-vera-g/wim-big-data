import os
import h5py


os.chdir(r"C:\__pc\ssroot\pycharm\Master\bigdata\Scripts\MillionSongSubset\A\A\A") #wechseln zu Ordner, in dem .h5-Dateien liegen
for file in os.listdir("."): #alle Dateien im Ordner
    print(file) #Dateinamen ausgeben
    with h5py.File(file) as f: #File-Methode öffnet Dateien
        print(f.keys()) #vgl. zu Dictionarys Keys - halten eigentliche Daten
        print(list(f['musicbrainz'])) #metadaten von musicbrainz // artist_mbtag = tags, die artist auf musicbrainz.org erhalten hat
        print()                              #artist_mbtags_count ist Anzahl der tags
        print(f.keys())
        print(f['musicbrainz/songs'][()]) #nimmt Key musicbrainz, geht in Songs und gibt dann alle Werte aus
        print(f['musicbrainz/artist_mbtags'][()]) #nimmt Key musicbrainz, geht in artist_mbtags und gibt dann alle Werte aus
        print(f['musicbrainz/artist_mbtags_count'][()]) #nimmt Key musicbrainz, geht in artist_mbtags_count und gibt dann alle Werte aus

