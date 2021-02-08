{% extends "mail_templated/base.tpl" %}
{% load i18n %}
{% load resolve_frontend_url from urls_extra %}

{# ======== Subject of email #}
{% block subject %}You've been invited to Mi Life{% endblock %}

{% block body %}
{# ======== plain text version of email body #}
{% blocktrans %}Hi {{ user.first_name }}!{% endblocktrans %}
{% blocktrans %}
Your mi-life account has been created using the email address {{ user.email }}.
{% endblocktrans %}

{% trans "For the first step, please click on the "reset password" link to choose your own password:" %}

{% resolve_frontend_url "password-confirm" token=token %}

{% blocktrans %}
We have set the account up with a password of "password". 
Once you have reset your pasword you will be able to login with your new credentials.
{% endblocktrans %}
{% endblock body %}


{% block html %}
{# ======== html version of email body #}
<p>{% blocktrans %}Hi {{ user.first_name }}!{% endblocktrans %}</p>
<p>{% blocktrans %}Your mi-life account has been created using the email address {{ user.email }}.{% endblocktrans %}</p>

<p>{% trans "For the first step, please click on the "reset password" link to choose your own password:" %}
<a href="{% resolve_frontend_url "password-confirm" token=token %}">{% trans "Reset Password" %}</a>
</p>

<p>{% blocktrans %}
We have set the account up with a password of "password". 
Once you have reset your pasword you will be able to login with your new credentials.
{% endblocktrans %}</p>
{% endblock html %}

