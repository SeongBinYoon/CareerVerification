import openai

# proj_ver로 정적 1차 검증 후 동적 2차 검증 함수
def verify_html_usingGPT(query, api_key):
    # 모델 - GPT 3.5 Turbo 선택
    openai.api_key=api_key
    model = "gpt-3.5-turbo"
    
    # 질문 작성하기
    print("="*100)
    print(query)
    print("="*100)
    # 메시지 설정하기
    messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['message']['content']
    print(answer)
    print("="*100)

    return answer