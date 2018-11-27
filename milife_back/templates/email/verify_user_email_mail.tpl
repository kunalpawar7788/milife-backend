{% extends "mail_templated/base.tpl" %}
{% load i18n %}
{% load resolve_frontend_url from urls_extra %}

{# ======== Subject of email #}
{% block subject %}Confirm Your Email!{% endblock %}

{% block body %}
{# ======== plain text version of email body #}
{% blocktrans %}Thanks for registering, kindly confirm email{% endblocktrans %}

{% resolve_frontend_url "verify-user-email" token=token %}

{% trans "Thanks for using our site!" %}
{% endblock body %}


{% block html %}
{# ======== html version of email body #}
<p>{% blocktrans %}You're receiving this email because you requested a password reset
for your user account.{% endblocktrans %}</p>

<p>{% trans "Please go to the following page and choose a new password:" %}
<a href="{% resolve_frontend_url "verify-user-email" token=token %}">{% trans "Confirm Email" %}</a>
</p>

<p>{% trans "Thanks for using our site!" %}</p>
{% endblock html %}
