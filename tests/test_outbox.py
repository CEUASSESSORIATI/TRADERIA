from app.outbox import Outbox


def test_outbox_enqueue_ack(tmp_path):
    queue = Outbox(tmp_path / "queue.sqlite3")
    queue.enqueue("event", {"value": 123})
    pending = queue.pending()
    assert len(pending) == 1
    assert pending[0][1:] == ("event", {"value": 123})
    queue.acknowledge(pending[0][0])
    assert queue.count() == 0
