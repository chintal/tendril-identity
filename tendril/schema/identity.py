

from tendril.schema.base import SchemaControlledYamlFile
from tendril.utils import log
logger = log.get_logger(__name__, log.DEBUG)


class IdentitySchema(SchemaControlledYamlFile):
    schema_name = 'IdentitySchema'
    schema_version_max = '1.0'
    schema_version_min = '1.0'


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_schema('IdentitySchema', IdentitySchema,
                        doc="Schema for Identity Definition Files")
