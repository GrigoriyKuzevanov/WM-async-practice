import sys
from parser.migration_utils.runner import alembic_runner

alembic_runner(*sys.argv[1:])
