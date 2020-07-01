import faker

from .factories import AccountFactory
from ..models import Account
from ..tasks import write_off_holds_from_balances

fake = faker.Faker()


def test_write_off_holds_from_balances():
    accounts = AccountFactory.create_batch(size=fake.random_int(5, 10))
    initial_data = {
        str(account.uuid):
            {'balance': account.balance, 'hold': account.hold}
        for account in accounts
    }
    write_off_holds_from_balances()
    accounts = Account.objects.all()
    for account in accounts:
        assert account.balance == (initial_data[str(account.uuid)]['balance'] -
                                   initial_data[str(account.uuid)]['hold'])
        assert account.hold == 0
