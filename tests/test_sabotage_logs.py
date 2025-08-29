from ai_identity.sabotage_logs import SabotageLogger


def test_logs_multiple_events():
    """Logged events are appended in order."""
    logger = SabotageLogger()
    logger.log('anomaly')
    logger.log('intrusion')
    assert logger.events == ['anomaly', 'intrusion']


def test_loggers_are_isolated():
    """Separate instances maintain independent event lists."""
    first = SabotageLogger()
    second = SabotageLogger()
    first.log('issue')
    assert second.events == []
