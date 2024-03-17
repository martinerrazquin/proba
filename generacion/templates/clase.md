---
title: {{fecha|datefmt}}
type: docs
{% if previous is defined %}
    prev: clases/{{ previous }}
{% endif %}
{% if next is defined %}
    next: clases/{{ next }}
{% endif %}
weight: {{current|classweight}}
---

{% if feriado is defined %}
    Feriado por {% *Puente* de **{{ puente }}** if puente is defined %} **{{ motivo }}**.
{% elif repaso is defined %}
    Clase de repaso. Aprovechen a hacer consultas y traigan enunciados para resolver!
{% else %}
    ## Temas a tratar
    {% for tema in temas %}
        * {{ tema }}
    {% endfor %}

    ## Videos

    {% if videos.teoricos is defined %}
    ### Teóricos
    {% for video in videos.teoricos %}
        {{ video|embedyt(true)}}
    {% endfor%}
    {% endif %}

    {% if videos.practicos is defined %}
    ### Teóricos
    {% for video in videos.practicos %}
        {{ video|embedyt(false) }}
    {% endfor%}
    {% endif %}

    {% if ejercicios is defined %}
    ## Ejercicios de la Guía
    {{ ejercicios|compileejs }}
    {% endif %}
{% endif %}
