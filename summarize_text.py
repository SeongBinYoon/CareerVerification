import openai
import extract2 as ext2

def summarize_text(text_dict, api_key):
    # for key, value in text_dict.items():
    #     if isinstance(value, list) and value:
    #         summ_text_list.append(value)
    # 모델 - GPT 3.5 Turbo 선택
    openai.api_key=api_key
    model = "gpt-3.5-turbo"

    prompt = f"""
    당신의 임무는 경력직 이력서에 있는 내용을 토대로 면접관에게 면접자에 대한 
    요약된 정보를 제공하는 것입니다.

    경력직 이력서에 있는 내용은 순서대로 업무 내용, 업무 성과, 이직 사유, 자기pr 순서 입니다.
    네 개의 역따옴표로 묶인 아래 내용들을 토대로 면접관에게 요약된 정보를 자연스러운 문장으로 제공해주세요.
    단, 없는 정보를 추측하여 만들어 내지 않도록 주의하세요.

    업무 내용: ```{text_dict['detailtask']}```
    업무 성과: ```{text_dict['perf']}```
    이직 사유: ```{text_dict['switjob']}```
    자기 pr: ```{text_dict['pr_career']}```
    """
    # 메시지 설정하기
    messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
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
