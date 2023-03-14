####################################################################
#                                                                  # 
#                        IMPORTATION DES                           #
#                            MODULES                               #
#                                                                  #
####################################################################

import sqlalchemy.orm as _orm
import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative

####################################################################
#                                                                  # 
#                          SQLALCHEMY                              #
#                            SETUP                                 #
#                                                                  #
####################################################################

# Définition de l'URL de la base de données pour SQLAlchemy :
# elle se trouvera dans le dossier courant dans le fichier `database.db`
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# Création d'un moteur de base de données 
engine = _sql.create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True,
    connect_args={'check_same_thread': False}
)

# Définition d'un objet de session pour accéder à la base de données
SessionLocal = _orm.sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Déclaration de la classe de base pour les modèles de base de données
Base = _declarative.declarative_base()

# Création de toutes les tables dans la base de données
Base.metadata.create_all(bind=engine)
