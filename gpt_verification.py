# The copyright of this code belongs to Jeong U, Han
import openai

def verify_html_usingGPT(text, verification_list, search_query, api_key):
    # 모델 - GPT 3.5 Turbo 선택
    openai.api_key=api_key
    model = "gpt-3.5-turbo"
    keyword = search_query
    name = verification_list[0]
    score = verification_list[1]

    # 질문 작성하기
    query = f'아래의 웹에서 크롤링한 내용을 토대로 {name} 이(가) {keyword}에서 {score} 수상 성적을 거뒀는지 확인해줘. \'{text}\''
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