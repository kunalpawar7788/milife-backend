{% extends "mail_templated/base.tpl" %}
{% load i18n %}
{% load resolve_frontend_url from urls_extra %}

{# ======== Subject of email #}
{% block subject %}You've been invited to Mi Life{% endblock %}

{% block body %}
{# ======== plain text version of email body #}
{% blocktrans %}You have been invited to mi-life.co.uk.{% endblocktrans %}

{% trans "Please go to the following page and choose your password:" %}

{% resolve_frontend_url "password-confirm" token=token %}

{% trans "Thanks for using our site!" %}
{% endblock body %}


{% block html %}
{# ======== html version of email body #}
<p>{% blocktrans %}You've been invited to mi-life.co.uk{% endblocktrans %}</p>

<p>{% trans "Please go to the following page and choose your password:" %}
<a href="{% resolve_frontend_url "password-confirm" token=token %}">{% trans "Reset Password" %}</a>
</p>

<p>{% trans "Thanks!" %}</p>
{% endblock html %}
