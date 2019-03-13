import pytest
from django.core.urlresolvers import reverse

from adhocracy4.test.helpers import redirect_target
from liqd_product.apps.budgeting import phases
from tests.helpers import assert_template_response
from tests.helpers import freeze_phase
from tests.helpers import setup_phase


@pytest.mark.django_db
def test_list_view(client, phase_factory, proposal_factory, partner):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'liqd_product_budgeting/proposal_list.html')


@pytest.mark.django_db
def test_detail_view(client, phase_factory, proposal_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    url = item.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'liqd_product_budgeting/proposal_detail.html')


@pytest.mark.django_db
def test_create_view(client, phase_factory, proposal_factory, user,
                     category_factory, area_settings_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    area_settings_factory(module=module)
    category = category_factory(module=module)
    url = reverse(
        'liqd_product_budgeting:proposal-create',
        kwargs={
            'partner_slug': project.organisation.partner.slug,
            'module_slug': module.slug
        }
    )
    with freeze_phase(phase):
        client.login(username=user.email, password='password')

        response = client.get(url)
        assert_template_response(
            response,
            'liqd_product_budgeting/proposal_create_form.html')

        data = {
            'name': 'Idea',
            'description': 'description',
            'category': category.pk,
            'budget': 123,
            'point': (0, 0),
            'point_label': 'somewhere'
        }
        response = client.post(url, data)
        assert redirect_target(response) == 'proposal-detail'


@pytest.mark.django_db
def test_moderate_view(client, phase_factory, proposal_factory, user,
                       area_settings_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    area_settings_factory(module=module)
    url = reverse(
        'liqd_product_budgeting:proposal-moderate',
        kwargs={
            'partner_slug': project.organisation.partner.slug,
            'pk': item.pk,
            'year': item.created.year
        }
    )
    project.moderators.set([user])
    with freeze_phase(phase):
        client.login(username=user.email, password='password')

        response = client.get(url)
        assert_template_response(
            response,
            'liqd_product_budgeting/proposal_moderate_form.html')

        data = {
            'moderator_feedback': 'test',
            'is_archived': False,
            'statement': 'its a statement'
        }
        response = client.post(url, data)
        assert redirect_target(response) == 'proposal-detail'
