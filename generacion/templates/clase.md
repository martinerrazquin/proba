---
title: {{fecha|datefmt}}
type: docs
{% if prev is defined -%}
prev: clases/{{ prev }}
{% endif -%}
{% if next is defined -%}
next: clases/{{ next }}
{% endif -%}
weight: {{ week*10 + day }}
---

{% if feriado is defined %}
{{ feriado|feriadofmt }}
{% elif repaso is defined %}
Clase de repaso. Aprovechen a hacer consultas y traigan enunciados para resolver!
{% else %}
## Temas a tratar

{% for tema in temas -%}
* {{ tema }}
{% endfor %}
## Videos
{% if videos.teoricos is defined %}
### Teóricos
{% for video in videos.teoricos %}
{{ video|embedyt(true)}}
{% endfor -%}
{% endif %}
{% if videos.practicos is defined %}
### Prácticos
{% for video in videos.practicos %}
{{ video|embedyt(false) }}
{% endfor%}
{% endif %}

{% if ejercicios is defined %}
## Ejercicios de la Guía
{{ ejercicios|compileejs }}
{% endif %}
{% endif %}
