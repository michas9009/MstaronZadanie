<h2>Postup instalacie a spustenia</h2>

Instalacia potrebnych balickov:
	
	pip install -r req.txt

Instalacia prostredia:
	
	pip install virtualenv
	virtualenv venv
	venv\Scripts\activate

Vytvoreni suboru pre program (v pripade ze nie je)

	type nul >> main.py



Pred supstenim programu vo webovom rozhrani je potrebne vytvorit aspon jedneho pouzivatela.(aby fungovalo pridavanie prispevkov, jeho ID bude 1)

Jednou z moznosti je pomocou napr. Postman-u. Alebo v terminali vo vyvojovom prostredi pomocou:

	python
	>>> from main import db
	>>> db.create_all()
	>>> from main import Users
	>>> user = Users(name="AAA", surname="BBB")
	>>> db.session.add(user)
	>>> db.session.commit()
	>>> exit()
	


Spustenie:

	set FLASK_APP=main.py
	set FLASK_ENV=development
	flask run

Nasledne je mozne otvorit program cez webovy prehliadac na lokalnej adrese.
