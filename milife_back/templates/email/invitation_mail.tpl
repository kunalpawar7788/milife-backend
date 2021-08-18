{% extends "mail_templated/base.tpl" %}
{% load i18n %}
{% load resolve_frontend_url from urls_extra %}

{# ======== Subject of email #}
{% block subject %}You've been invited to Mi Life{% endblock %}

{% block body %}
{# ======== plain text version of email body #}
{% blocktrans %}Hi {{ user.first_name }}!{% endblocktrans %}
{% blocktrans %}
Your mi-life account has been created using the email address: {{ user.email }}
{% endblocktrans %}

{% trans "As a first step, please click on the "reset password" link to choose your own password:" %}

{% resolve_frontend_url "password-confirm" token=token %}

{% blocktrans %}
Once you have done this you will be able to log in with your new password.

Enjoy the app!
admin@mi-life
{% endblocktrans %}
{% endblock body %}


{% block html %}
{# ======== html version of email body #}
<p>{% blocktrans %}Hi {{ user.first_name }}!{% endblocktrans %}</p>
<p>{% blocktrans %}Your mi-life account has been created using the email address: {{ user.email }}{% endblocktrans %}</p>

<p>{% trans "As a first step, please click on the "reset password" link to choose your own password:" %}
<a href="{% resolve_frontend_url "password-confirm" token=token %}">{% trans "Reset Password" %}</a>
</p>

<p>{% blocktrans %}
Once you have done this you will be able to log in with your new password.

Enjoy the app!
admin@mi-life
{% endblocktrans %}</p>
{% endblock html %}

