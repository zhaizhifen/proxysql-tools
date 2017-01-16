from schematics.models import Model
from schematics.types import StringType, IntType


class ProxySQLMySQLBackend(Model):
    """Contains information about MySQL backend"""
    hostgroup_id = IntType(default=0)

    # The name of the host running MySQL. When using unix domain socket, set this to the socket path
    hostname = StringType(required=True)

    # The port MySQL is listening on. When using unix domain socket, set this to 0
    port = IntType(default=3306, required=True)

    status = StringType(choices=['ONLINE', 'SHUNNED', 'OFFLINE_SOFT', 'OFFLINE_HARD'], default='ONLINE')

    weight = IntType(default=1)
    compression = IntType(default=0)
    max_connections = IntType(default=10000)
    max_replication_lag = IntType(default=0)
    use_ssl = IntType(choices=[0, 1], default=0)
    max_latency_ms = IntType(default=0)
    comment = StringType(default='')

    def __hash__(self):
        return hash(str(self.hostgroup_id) + self.hostname + str(self.port))


class ProxySQLMySQLUser(Model):
    """Contains information about MySQL backend user"""

    # Credentials for connecting to MySQL or ProxySQL instance
    username = StringType(required=True)
    password = StringType(required=True)

    active = IntType(choices=[0, 1], default=1)
    use_ssl = IntType(choices=[0, 1], default=0)

    # If there is no matching rule for the queries sent by this user then the traffic is sent to the specified
    # hostgroup
    default_hostgroup = IntType(default=0)

    # The schema to which the connection should change by default
    default_schema = StringType(default='information_schema')
    schema_locked = IntType(choices=[0, 1], default=0)

    # If this is set for the user with which the MySQL client is connecting to ProxySQL (thus a "frontend" user - see
    # below), transaction started within a hostgroup will remain within that hostgroup regardless of any other rules
    transaction_persistent = IntType(choices=[0, 1], default=0)

    # If set, it bypasses the query processing layer (rewriting, caching) and passes through the query directly as is
    # to the backend server
    fast_forward = IntType(choices=[0, 1], default=0)

    # Note, currently all users need both "frontend" and "backend" set to 1. If set to 1, this (username, password)
    # pair is used for authenticating to the MySQL servers against any hostgroup
    backend = IntType(choices=[0, 1], default=1)

    # If set to 1, this (username, password) pair is used for authenticating to the ProxySQL instance
    frontend = IntType(choices=[0, 1], default=1)

    max_connections = IntType(default=10000)

    def __hash__(self):
        return hash(str(self.username) + str(self.backend))
