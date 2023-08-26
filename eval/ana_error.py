import os
import openai
import numpy as np
import operator
import argparse
import json
import math
from prompt import prompt_scai
from post_process import parse_math_answer
openai.api_key = os.getenv("OPENAI_API_KEY")
def find_error(sys, problem, correct, sol, tool="", ans=[]):
    messages=[{"role": "system", "content": sys}]
    if tool not in ["python","wolfram"]:
        instruct= "The question is " + problem + "\n" + "The correct solution is "+correct+"\n"+"The model solution is "+sol
    else:
        idx1=sol.find('```')
        idx2=sol[idx1+3:].find('```')
        instruct= "The question is " + problem + "\n" + "The correct solution is "+correct+"\n"+"The model solution is "+sol[:idx2+idx1+6]+"\n"+"The translated program generates the answer as "+ans +", which is treated as model's output answer."
    messages+=[
            {"role": "user", "content": instruct}
          ]
    return messages

    
def call_engine(messages, engine,temperature=0,n=1, patience=10, sleep_time=0):
    while patience > 0:
        patience -= 1
        try:
            response = openai.ChatCompletion.create(model=engine,
                              messages=messages,
                              temperature=temperature)
            if n == 1:
                prediction = response['choices'][0]['message']['content'].strip()
                if prediction != "" and prediction != None:
                    return prediction
            else:
                prediction = [choice['message']['content'].strip() for choice in response['choices']]
                if prediction[0] != "" and prediction[0] != None:
                    return prediction

        except Exception as e:
            print(e)
            if sleep_time > 0:
                time.sleep(sleep_time)
    return ""

def equiv(model_output, answer, unit):
    model_output=model_output.replace(',', '')
    try:
        first=math.isclose(float(model_output.strip()), float(answer.strip()), abs_tol=0.1)
    except:
        first=False
    try: 
        model=model_output.strip().split()[0]
        second=math.isclose(float(model), float(answer.strip()), abs_tol=0.1)
    except:
        second=False
    if first or second:
        return True
    return False

def run(file, engine, start_n,setting):
    outputs = []
    answers = []
    types = []
    list_equiv = []
    model_outputs=[]
    ls_dict=[]

    fnames_list = []

    correct = 0
    total = 0
    count=0
    sys_name=""
    sys_prompt=prompt_scai.sys_ana
    
    sys_name=""
    with open("./output_{}/{}_dict_{}_{}_{}.json".format(setting, engine, setting, start_n,file), encoding='utf-8') as json_file, open("../dataset/original/{}_sol.json".format(file), encoding='utf-8') as ori_file:
        problems=json.load(json_file)
        ori_problems=json.load(ori_file)
        for i, problem_data in enumerate(problems): 
                if problem_data["correct"]:
                    continue
                fnames_list.append(problem_data["fname"])
                problem_text=ori_problems[i]["problem_text"]+" The unit of the answer is "+ori_problems[i]["unit"]+"."
                message=find_error(sys_prompt, problem_text, ori_problems[i]["solution"], problem_data["gpt solution"], setting, problem_data["gpt answer"])
                model_output_ori=call_engine(message, engine=engine)
                
                print(message, model_output_ori)
                model_output = parse_math_answer(model_output_ori)
                

                outputs.append(model_output)
                model_outputs.append(model_output_ori)

                print("Model output:")
                print(model_output)
                print("--------------------------------------------")
                
                total += 1

                
                
                ls_dict.append({'gpt solution': problem_data["gpt solution"], "correct solution": ori_problems[i]["solution"], "problem_text": ori_problems[i]["problem_text"], "correct answer": problem_data["correct answer"],
                               "gpt error reason": model_output, "gpt error explain":model_output_ori,"fname": problem_data["fname"], "correct":problem_data["correct"]})
                if total % 1==0:
                    with open("./output_{}/error_{}_dict_{}_{}_{}.json".format(setting, engine, sys_name, start_n,file), 'w') as fout:
                        json.dump(ls_dict, fout)
                    with open("./output_{}/error_{}_{}_{}_{}.txt".format(setting, engine,sys_name, start_n,file), "w+") as f:
                        for k, (output, fnames, model_output) in enumerate(zip(outputs, fnames_list, model_outputs)):
                            f.write("\n{} OUTPUT: {} | fname:{} | gpt: {}\n".format(k, output, fnames, model_output))

                        

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', type=str, default='gpt-3.5-turbo')
    parser.add_argument('--setting', type=str, default='zero')
    parser.add_argument('--start_num', type=int, default=0)   
    parser.add_argument('--list_source', nargs='+', default=["atkins", "calculus","chemmc","class","diff","fund","matter","quan","stat","thermo"])
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    for source in args.list_source:
        run(source,args.engine, args.start_num, args.setting)