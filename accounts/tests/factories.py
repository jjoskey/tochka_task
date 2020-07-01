import factory
import faker

from ..models import Account

fake = faker.Faker()


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    name = factory.Faker('name')
    balance = factory.Faker('pyint', min_value=3)
    hold = factory.LazyAttribute(
        lambda obj: fake.pyint(max_value=obj.balance - 1)
    )
