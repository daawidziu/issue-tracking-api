import pytest

from application.models import Account, Project


def test_account(app):
    email = 'a@b.c'
    password = '123456.a'
    account = Account(email=email, password=password, role='user')
    account.save()
    assert account.validate_password(password)
    assert not account.validate_password('wrong password')
    with pytest.raises(AttributeError):
        account.password
    account.delete()


def test_base(app):
    name = 'Name'
    desc = 'Description'
    project = Project(name=name, description=desc)
    project.save()
    assert Project.get(name=name).name == project.name
    assert Project.filter_by()
    assert Project.paginate(page=1).items == [project]
    project.update({'description': 'NewName'})
    assert project.description == 'NewName'
    project.delete()
