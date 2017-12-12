from functools import lru_cache
from functools import partial
import requests


@lru_cache(maxsize=10)
def chips(x, y, acquired, ubids, host, resource='/chips'):
    """Returns chips from a Chipmunk instance given x, y, date range and ubid sequence

    Args:
        x: longitude
        y: latitude
        acquired: ISO8601 daterange '2012-01-01/2014-01-03'
        ubids: sequence of ubid strings
        host: protocol://host:port
        resource: /path/to/chips/resource (default: /chips)

    Returns:
        tuple: chips

    Example:
        >>> chipmunk.chips(host='http://host:port',
                           x=123456,
                           y=789456,
                           acquired='2012-01-01/2014-01-03',
                           ubids=['LANDSAT_7/ETM/sr_band1', 'LANDSAT_5/TM/sr_band1'])
    """
    params = [{'x': x, 'y': y, 'acquired': acquired, 'ubid': u } for u in ubids]
    responses = [requests.get(url=url, params=p).json() for p in params]
    return tuple(reduce(add, responses))


def spec(query, host, resource='/chip-specs'):
    url = '{}{}{}'.format(host, resource, query)
    print("URL:{}".format(url))
    return tuple(requests.get(url=url).json())


def specs(queries, host, resource='/chip-specs'):
    p = partial(spec, host=host, resource=resource)
    return {k: p(q=v) for k,v in queries.items()}


@lru_cache(maxsize=None)
def snap(x, y, host, resource='/grid/snap'):
    url = '{}{}'.format(host, resource)
    print("URL:{}".format(url))
    return requests.get(url=url, params={'x': x, 'y': y}).json()


@lru_cache(maxsize=None)
def near(x, y, host, resource='/grid/near'):
    url = '{}{}'.format(host, resource)
    return requests.get(url=url, params={'x': x, 'y': y}).json()
