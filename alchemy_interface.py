import sqlalchemy.types
from sqlalchemy import func
from sqlalchemy.types import TypeDecorator
from decimal import Decimal as D
import sqlalchemy.types as types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import distinct, create_engine, Numeric, Integer, Column, DateTime, Time
from sqlalchemy.ext.declarative import declarative_base

class SqliteNumeric(types.TypeDecorator):
    impl = types.String
    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.VARCHAR(100))
    def process_bind_param(self, value, dialect):
        return str(value)
    def process_result_value(self, value, dialect):
        return D(value)
Numeric = SqliteNumeric

engine = create_engine('sqlite:///measures.db', echo=False)

# create a Session
Session = sessionmaker(bind=engine)


Base = declarative_base()
class Measure(Base):
    """"""
    __tablename__ = "measures"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    gps_x = Column(Numeric(5,5))
    gps_y = Column(Numeric(5,5))
    sensor = Column(String)
    value = Column(Integer)

    #----------------------------------------------------------------------
    def __init__(self, date, time, gps_x, gps_y, sensor, value):
        """"""
        self.date = date
        self.time = time
        self.gps_x = gps_x
        self.gps_y = gps_y
        self.sensor = sensor
        self.value = value

    # za lepsi izpis
    def nice_string(self):
        return "%s %s %s %s %s %s" % (self.date, self.time, self.gps_x, self.gps_y, self.sensor, self.value,)
