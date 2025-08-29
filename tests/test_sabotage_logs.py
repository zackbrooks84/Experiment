from ai_identity.sabotage_logs import SabotageLogger

def test_logs_events():
    logger = SabotageLogger()
    logger.log('anomaly')
    assert logger.events == ['anomaly']
