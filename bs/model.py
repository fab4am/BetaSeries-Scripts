# -*- coding: utf-8 -*-

import os

from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship

dburi = 'sqlite:///bs.db'
Base = declarative_base()
engine = create_engine(dburi, echo=False)
Session = scoped_session(sessionmaker(bind=engine))()

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
    serie = relationship("Serie", backref="seasons")
    """ relationship between Serie and Season """
    

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
    season = relationship("Season", backref="episodes")
    """ relationship between Season and Episode """

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

class Download(Base):
    __tablename__ = 'downloads'

    id = Column(Integer, primary_key=True)
    """ primary id """
    link = Column(String)
    """ Link of the torrent file used for this download """
    finished = Column(Boolean, default = False)
    """ Is the download finished """

    id_episode = Column( Integer, ForeignKey( Episode.id , ondelete="SET NULL"), index=True )
    """ link to the episode downloaded """
    episode = relationship("Episode", backref="downloads")
    """ relationship between Download and Episode """

    def __repr__(self):
        return "<Download('%s', '%s')>" % (self.link, self.episode)


if not os.path.isfile(dburi[dburi.rfind('/') + 1:]):
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    pass