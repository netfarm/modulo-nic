Modulo Registrazione Domini .it
===============================

Informazioni
------------

Utilizzo questo software per generare il modulo pdf per la registrazione dei domini .it.
I Registrant devono conservarlo con la firma del registrante.

Può essere utilizzato in un `virtualenv`, per installare le dipendenze
`pip install -r requirements.txt`

È stato testato con `apache2` e `nginx` (con uwsgi) ma dovrebbe funzionare con qualunque server supporti i cgi-bin.
È necessario impostare il charset del server `utf-8`, altrimenti le lettere accentate non saranno
gestite correttamente.

Istruzioni
----------

Copia i files in una cartella a piacimento, fai un link simbolico da `modulo-nic.py`
ad un file nella directory `/usr/bin/cgi-bin/`, per esempio io utilizzo `modulo-nic.pdf`, apache2
non ha problemi ad eseguire l'interprete python anche se l'estensione del file è .pdf, tuttavia
il file .py deve essere eseguibile.
Assicuratevi che apache2 o il server web che utilizzate sia configurato per servire i link simbolici,
altrimenti è possibile mettere i files direttamente nella directory dei cgi-bin ed eventualmente rinominare
modulo-nic.py in modulo-nic.pdf.

Un primo controllo puoi farlo eseguendo modulo-nic.py direttamente, dovrebbe visualizzare l'html della pagina
principale. Da linea di comando non è possibile generare il pdf.

Prova il modulo utilizzando il browser all'url http://server/cgi-bin/modulo-nic.pdf o come avete configurato.

Ho fatto questo semplice programma per utilizzo nella mia azienda, ho pensato che poteva essere utile anche
ad altri, ma non ho previsto un sistema per la personalizzazione.
In ogni caso la cosa è abbastanza semplice, nel file modulo-nic.rml puoi cambiare _NETFARM-REG_ con la tua sigla
e cambiare il watermark nella sezione `<pageGraphics>`.

Lo script attiva `cgitb` (in cima) per visualizzare eventuali errori di esecuzione, puoi disabilitarlo o redirigere
su file gli errori, consulta il modulo `cgi` nella documentazione di python.

Se invece il server web restituisce un Internal Error (500), consulta i log di errore,
su apache `/var/log/apache2/error.log`.
