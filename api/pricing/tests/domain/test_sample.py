from api.pricing.pricing.domain import sample_entity

def test_id():
    entity = sample_entity.SampleEntity()
    assert entity.id() == 1