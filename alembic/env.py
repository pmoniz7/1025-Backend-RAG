import os
from dotenv import load_dotenv
load_dotenv()

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

#### A T U A L   E N V.PY #####
print("%%%%%%%%%%% usuário %%%%%%%%%%%", {os.environ['DATABASE_USER']})
print("%%%%%%%%%%% host    %%%%%%%%%%%", {os.environ['DATABASE_HOST']})
print("%%%%%%%%%%% porta   %%%%%%%%%%%", {os.environ['DATABASE_PORT']})
print("%%%%%%%%%%% banco   %%%%%%%%%%%", {os.environ['DATABASE_NAME']})
print("%%%%%%%%%%% pw      %%%%%%%%%%%", {os.environ['DATABASE_PASSWORD']})

#config.set_main_option("sqlalchemy.url", f"postgresql://{os.environ['DATABASE_USER']}:@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}")
config.set_main_option("sqlalchemy.url", f"postgresql://{os.environ['DATABASE_USER']}:{os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}")
                                           
    
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    print("%%%%%% fileConfig %%%%% => ", config.config_file_name)
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

########### CHATGPT #############
##from models import Base
##target_metadata = Base.metadata
#################################     

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

#print("%%%%%% vai run_migrations offline %%%%% ")
url = config.get_main_option("sqlalchemy.url")
print("%%%%%% url %%%%% => ", url)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()



def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    print("%%%%%% vai run_migrations online - vai em connectable %%%%% ")
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    print("%%%%%% vai run_migrations online RESULTADO CONNECTABLE %%%%% ", connectable)
    with connectable.connect() as connection:
        print("%%%%%% vai run_migrations online EM CONNECTION %%%%% ", connection)
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        print("%%%%%% vai run_migrations online AS CONNECTION CRIADA  %%%%% => ", connection)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    print("%%% offline %%%")
    run_migrations_offline()
else:
    print("%%% online %%%")
    run_migrations_online()
