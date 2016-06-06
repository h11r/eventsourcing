from uuid import uuid1

from eventsourcing.domain.model.events import DomainEvent, publish
from eventsourcing.domain.model.example import Example
from eventsourcing.infrastructure.stored_events.transcoders import topic_from_domain_class, make_stored_entity_id, \
    id_prefix_from_entity


class Snapshot(DomainEvent):

    def __init__(self, entity_id, last_event_id, topic, attrs):
        super(Snapshot, self).__init__(entity_id=entity_id, entity_version=0, last_event_id=last_event_id,
                                       topic=topic, attrs=attrs)

    @property
    def topic(self):
        """Path to the class.
        """
        return self.__dict__['topic']

    @property
    def attrs(self):
        """Attributes of the instance.
        """
        return self.__dict__['attrs']


def take_snapshot(entity, last_event_id):
    # Make the 'stored entity ID' for the entity.
    id_prefix = id_prefix_from_entity(entity)
    stored_snapshotted_entity_id = make_stored_entity_id(id_prefix, entity.id)

    # Create the snapshot event.
    snapshot = Snapshot(
        entity_id=stored_snapshotted_entity_id,
        last_event_id=last_event_id,
        topic=topic_from_domain_class(Example),
        attrs=entity.__dict__.copy(),
    )
    publish(snapshot)

    # Return the event.
    return snapshot
