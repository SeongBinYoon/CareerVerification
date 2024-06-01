# 검증 결과

## 개인 정보

- 성명: {{ files_pinfo['name'] }}
- 생년월일: {{ files_pinfo['birth'] }}
- 주소: {{ files_pinfo['address'] }}
- 연락처: {{ files_pinfo['phone'] }}

## 특허 검증 결과

{% for pat, vpat in zip(files_vcat['patent'], files_vres['patent']) %}
- **{{ pat }}**
  - 결과: {{ vpat }}
{% endfor %}

## 프로젝트 검증 결과

{% for proj, vproj in zip(files_vcat['project'], files_vres['project']) %}
- **{{ proj }}**
  - 결과: {{ vproj }}
  {% if gpt_res['proj'] %}
  - gpt 검증 의견: {{ gpt_res['proj'] }}
  {% endif %}
{% endfor %}

## Contributor (프로젝트 기여도) 검증 결과

{% for con, vcon in zip(files_vcat['contributor'], files_vres['contributor']) %}
- **{{ con }}**
  - 결과: {{ vcon }}
{% endfor %}

## 수상 내역 검증 결과

{% for awd, vawd in zip(files_vcat['award'], files_vres['award']) %}
- **{{ awd }}**
  - 결과: {{ vawd }}
  {% if gpt_res['award'] %}
  - gpt 검증 의견: {{ gpt_res['award'] }}
  {% endif %}
{% endfor %}
