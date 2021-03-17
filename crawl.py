from bs4 import BeautifulSoup
import os
import sys
import re
import requests

HOME_DIR = '/home/jin/ps'
BOJ_URL = 'https://acmicpc.net/problem'

def make_problem_set(problem_num: str):
    if problem_num:
        url = '/'.join([BOJ_URL, problem_num])
        resp = requests.get(url)
        if resp.status_code == 200:
            html = resp.text
            soup = BeautifulSoup(html, 'html.parser')
            problem_body = str(soup.select_one('#problem_description'))
            problem_body = re.sub('<.+?>','',problem_body,0)

            problem_input = str(soup.select_one('#problem_input'))
            problem_input = re.sub('<.+?>','',problem_input,0)

            problem_output = str(soup.select_one('#problem_output'))
            problem_output = re.sub('<.+?>','',problem_output,0)

            sample_inputs = []
            sample_outputs = []

            for i in range(1, 5):
                sample_input = str(soup.select_one('#sample-input-' + str(i)))
                sample_input = re.sub('<.+?>','',sample_input,0)
                sample_output = str(soup.select_one('#sample-output-' + str(i)))
                sample_output = re.sub('<.+?>','',sample_output,0)

                if sample_input=='None' and sample_output=='None':
                    break
                else:
                    sample_inputs.append(sample_input)
                    sample_outputs.append(sample_output)

            os.makedirs(os.path.join(problem_num), exist_ok=True)
            with open(os.path.join(problem_num, 'problem'), 'w') as f:
                f.write('<PROBLEM>\n')
                f.write(problem_body)
                f.write('\n<PROBLEM_INPUT>\n')
                f.write(problem_input)
                f.write('\n<PROBLEM_OUTPUT>\n')
                f.write(problem_output)
                idx = 0
                for sample in zip(sample_inputs, sample_outputs):
                    f.write('\n<PROBLEM_INPUT_SAMPLE' + str(idx) + '>\n')
                    f.write(sample[0])
                    f.write('\n<PROBLEM_OUTPUT_SAMPLE' + str(idx) + '>\n')
                    f.write(sample[1])
                    idx += 1
            for i,sample in enumerate(sample_inputs):
                with open(os.path.join(problem_num, 'input' + str(i)), 'w') as f:
                    f.write(sample)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("python crawl.py {problem_number}")
        sys.exit(1)

    problem_num = sys.argv[1]

    make_problem_set(problem_num)



