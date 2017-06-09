from app import db
from datetime import datetime
from flask_admin.contrib import sqla
from sqlalchemy.schema import ForeignKey
import flask_admin as admin


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(35))
    email = db.Column(db.String(40), unique=True)
    status = db.Column(db.String(1))
    valid = db.Column(db.String(1))
    create_at = db.Column(db.DateTime)
    trades = db.relationship('Trade', backref='fk_user', lazy='dynamic')

    def __str__(self):
        return self.name, self.email, self.status


    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py
        seed()

        for i in range(count):
            u = User(name=forgery_py.name.full_name(),
                    email=forgery_py.internet.email_address(),
                    status='A',
                    valid='N',
                    create_at=forgery_py.date.date()
                    )
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class Trade(db.Model):
    __tablename__= 'trades'
    trade_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trade_long_id = db.Column(db.String(64))
    symbol = db.Column(db.String(32))
    action = db.Column(db.Integer)
    stop = db.Column(db.Float())
    active = db.Column(db.Integer)
    trade_info = db.Column(db.Text)
    privacy = db.Column(db.Integer)
    fk_portfolio_id = db.Column(db.Integer)
    blocked = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __str__(self):
        return self.trade_long_id, self.fk_user_id, self.symbol



    # Realizamos el Scraping del sitio web para
    # obtener el listado de los simbolos y changes
    # que son trending al dia solicitado.
    # Estos son guardados en la tabla SCRAPS, luego
    # de generar los numeros aleatorios de acerudo al CHANGE
    @staticmethod
    def getSymbols():
        import urllib2
        import requests
        from bs4 import BeautifulSoup
        from sqlalchemy.exc import IntegrityError
        import forgery_py

        quote_page = 'http://www.investcom.com/us/mpgnasdaq.htm'
        r = requests.get("http://www.investcom.com/us/mpgnasdaq.htm")

        if "blocked" in r.text:
            print "we've been blocked"


        if r.status_code == 200:
            # Obtener la lista de simbolos del sitio web (quote_page)
            page = urllib2.urlopen(quote_page)
            soup = BeautifulSoup(page, 'html.parser')
            data_name = soup.find('div', attrs={'class' : 'genTable'})

            for item in data_name.find_all('tr'):
                name_symbol = item.find("u")
                value_symbol = item.find("td", attrs={'nowrap' : "", 'align' : 'right'})
                change = item.find_all("font")
                                
                for i in range(len(change)):
                    if i == 1:
                        l = []
                        #record.update( {str(name_symbol.text) : str(change[i].text)} )
                        symbol  = str(name_symbol.text)
                        porc_ch = str(change[i].text)
                        porc_ch = porc_ch.replace("%", '')
                        porc_ch = porc_ch.replace("+", '')
                        porc_ch = porc_ch.replace("-", '')
                        porc_ch = float(porc_ch)

                        c = Trade()
                        l = c.random_number(porc_ch)

                        sc = Scrap(symbol=symbol,
                                   porc_change=porc_ch,
                                   create_date=forgery_py.date.date(),
                                   numbers=str(l)
                                  )
                        db.session.add(sc)
                        try:
                            db.session.commit()
                        except IntegrityError:
                            db.session.rollback()

        else:
            print "Failure of the connection to the web page"
            return False




    # Generador de los numeros aleatorios de acuardo
    # a numero (% change) suministrado, retorna una lista
    # valores negativos y positivos al metodo fake, por cada simbolo
    @staticmethod
    def random_number(porc_change):
        from random import uniform
        from sqlalchemy.exc import IntegrityError

        porc_change = float(porc_change)


        list_random_num = []
        for i in range(0, 10):
            num_pos = round(uniform(0, porc_change),6)
            porc_change = (-1 * porc_change)
            num_neg = round(uniform(porc_change, 0),6)
            list_random_num.append(num_pos)
            list_random_num.append(num_neg)

        return list_random_num



    # Generamos un trade falso para un usuario especifico
    # con el sumbolo y change obtenido en la funcion getSymbols
    @staticmethod
    def generate_fake(count=2):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py
        seed()

        user_count = User.query.count()
        # Generamos el scraper y recuperamos los simbolos 
        # obtenidos del sitio y los valores aleatorios del campo change
        vscrap = Trade
        vscrap.getSymbols()
        scrap_count = Scrap.query.count()

        if scrap_count > 0:

            for i in range(count):
                # Seleccionamos el usuario al que le asociaremos el registro fake
                u = User.query.offset(randint(0, user_count - 1)).first()
                # recurpamos el primer symbol y su valor change
                #s = Scrap.query.offset(randint(0, scrap_count - 1)).first()
                s = Scrap.query.get(int(i))

                vsymbol = s.symbol
                vchange = s.porc_change
                vrandom = s.numbers

                #print vsymbol

                
                # Armamos el diccionario con la info del trade
                ts_info = {}
                t = Trade(trade_long_id=forgery_py.name.full_name(),
                            symbol=s,
                            action=1,
                            stop=0,
                            active=1,
                            trade_info=vrandom,
                            privacy=1,
                            fk_portfolio_id=0,
                            blocked=0,
                            fk_user=u,
                            created_at=forgery_py.date.date()
                        )
                db.session.add(t)
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()

        else:
            print "Diccionario vacio, verifique"



class Scrap(db.Model):
    __tablename__ = 'scraps'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(35), unique=True)
    porc_change = db.Column(db.String(40), unique=True)
    create_date = db.Column(db.DateTime)
    numbers = db.Column(db.String(400) )

    def __str__(self):
        return self.symbol, self.porc_change




#Create model for class User
class UserAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['name', 'email']

#Create model for class Trade
class TradeAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['trade_long_id', 'symbol', 'action', 'trade_info']

#Create model for class Scrap
class ScrapAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['symbol', 'porc_change', 'numbers', 'create_date']


