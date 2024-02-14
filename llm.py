from openai import OpenAI



def html_hint(html):
    client = OpenAI()
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a tool that suggests correct HTML syntax to programmers."},
            {"role": "user", "content": f"Complete the tags in the following snippet of HTML code: {html}"},
        ]
    )
    
    return completion.choices[0].message.content


def thread_from_file(path):
    client = OpenAI()
    file = client.files.create(file=open(path, 'rb'), purpose='assistants')
    assistant = client.beta.assistants.create(
        instructions="You are a chatbot that analyzes the content of HTML documents.",
        model='gpt-3.5-turbo-1106',
        tools=[{'type': 'retrieval'}],
        file_ids=[file.id]
    )
    thread = client.beta.threads.create()
    
    return thread


def wait_on_run(client, run):
    r = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    stat = r.status
    return stat


def ask_llm(thread, query):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Tell me what the HTML file says."
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Tell the user what he would see if he opened the HTML document in a web browser."
    )



    while True:
        stat = wait_on_run(client, run)
        print(stat)
        if stat == 'cancelled' or stat == 'failed' or \
           stat == 'expired' or stat == 'completed':
            break

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        for m in messages:
            print(m.content[0].text.value)
