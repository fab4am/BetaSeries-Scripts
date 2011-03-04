# -*- coding: utf-8 -*-

import os

from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

dburi = 'sqlite:///bs.db'
Base = declarative_base()
engine = create_engine(dburi, echo=False)
Session = sessionmaker(bind=engine)
Session = Session()

class Serie(Base):
    __tablename__ = 'series'
    
    id = Column(Integer, primary_key=True)
    """ primary id """
    bs_id = Column(String)
    """ betaseries id """
    name = Column(String)
    """ name or title of the serie """
    path = Column(String)
    """ the path of the serie """
    enabled = Column(Boolean, default = True)
    """ Is the serie enabled """
    seasons = relationship("Season", backref="serie")
    """ relationship between Serie and Season """
    
    
    def __repr__(self):
       return "<Serie('%s', '%s')>" % (self.bs_id, self.name)

class Season(Base):
    __tablename__ = 'seasons'

    id = Column(Integer, primary_key=True)
    """ primary id """
    num = Column(String)
    """ num like S01 """
    path = Column(String)
    """ path in the filesystem """
    enabled = Column(Boolean, default = True)
    """ Is the season enabled """
    id_serie = Column( Integer, ForeignKey( Serie.id , ondelete="SET NULL"), index=True )
    """ reference to the serie """
    episodes = relationship("Episode", backref="season")
    """ relationship between Season and Episode """
    

    def __repr__(self):
        return "<Season('%s')>" % (self.num)

class Episode(Base):
    __tablename__ = 'episodes'

    id = Column(Integer, primary_key=True)
    """ primary id """
    num = Column(String)
    """ num like S01E01 """
    name = Column(String)
    """ the name of the episode """
    path = Column(String)
    """ filepath of this episode """
    enabled = Column(Boolean, default = True)
    """ Is the episode enabled """
    id_season = Column( Integer, ForeignKey( Season.id , ondelete="SET NULL"), index=True )
    """ reference to the season """

    def __repr__(self):
        return "<Episode('%s', '%s')>" % (self.num, self.name)

class Option(Base):
    __tablename__ = 'options'

    id = Column(Integer, primary_key=True)
    """ primary id """
    key = Column(String)
    """ num like S01 """
    value = Column(String)
    """ path in the filesystem """

    def __repr__(self):
        return "<Option('%s', '%s')>" % (self.key, self.value)


if not os.path.isfile(dburi[dburi.rfind('/') + 1:]):
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    pass