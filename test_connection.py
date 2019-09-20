#!/usr/bin/env python
# see https://github.com/apache/tinkerpop/blob/master/gremlin-python/src/main/jython/tests/driver/test_client.py
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver.request import RequestMessage

# test a connection
def test_connection():
    # see https://github.com/apache/tinkerpop/blob/master/gremlin-python/src/main/jython/gremlin_python/driver/driver_remote_connection.py
    remoteConnection=DriverRemoteConnection('ws://localhost:8182/gremlin','g')
    g = traversal().withRemote(remoteConnection)
    t=g.V()
    # see https://github.com/apache/tinkerpop/blob/master/gremlin-python/src/main/jython/gremlin_python/driver/client.py
    client=remoteConnection._client

    connection=client._get_connection()
    message = RequestMessage('traversal', 'bytecode', {'gremlin': t.bytecode, 'aliases': {'g': client._traversal_source}})
    results_set = connection.write(message).result()
    future = results_set.all()
    results = future.result()
    assert len(results) == 6
    assert isinstance(results, list)
    assert results_set.done.done()
    assert 'host' in results_set.status_attributes
    #print (results_set.status_attributes)

test_connection()
