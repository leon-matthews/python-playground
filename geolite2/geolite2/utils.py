

def calculate_range(network):
    """
    Calculate start and finish address values.

    Args:
        network: IPv4Network or IPv6Network object.

    Returns:
        2-tuple of inclusive integers for start and finish address
    """
    return (int(min(network)), int(max(network)))
