import os
import time
import openai
import numpy as np
import sys
from io import StringIO
import operator
import json
import argparse
import math
from prompt import prompt_scai
from post_process import parse_math_answer
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
openai.api_key = os.getenv("OPENAI_API_KEY")

def tool_ms(sys, problem, problem_eg, exp_eg, answer_eg, unit_eg, tool, lan, num_shot):
    print(num_shot)
    if sys !="":
        
        messages=[{"role": "system", "content": sys}]
    else:
        messages=[]
    for idx in range(num_shot):
        question_input = "Problem {}.   ".format(idx + 1) + problem_eg[idx] + "\n"
        question_output = "Explanation for Problem {}:   ".format(idx + 1) + exp_eg[idx] + "\n" + "{} language for Problem {}: ```".format(lan, idx+1)+tool[idx]+"``` \n The answer is \\boxed{"+ answer_eg[idx]+"} "+unit_eg[idx]
        
        messages += [
                {"role": "user", "content": question_input},
                {"role": "assistant", "content": question_output},
            ]
    test_question= "Problem {}.   ".format(len(problem_eg) + 1) + problem + "\n" 
    messages+=[
            {"role": "user", "content": test_question}
          ]
    return messages
def get_langueg(subj, lan):
    output_lan=[]
    for i in range(4):
        with open("../dataset/original/{}/{}_{}.txt".format(lan,subj,i)) as f:
            output_lan.append(f.read())

    return output_lan
def call_engine(messages, engine,temperature=0,n=1, patience=1000000000, sleep_time=0):
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
            # print(e)
            if sleep_time > 0:
                time.sleep(sleep_time)
    return ""
def extract_lan(output, lan, session):
    idx=output.find('```')
    output=output[idx+3:]
    idx=output.find('```')
    output=output[:idx]
    if lan=='python':
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        try:
            exec(output)
            sys.stdout = old_stdout
            ans=redirected_output.getvalue().strip()
        except:
            print('fail')
            return "None"
    else:
        try:
            output="N[{}]".format(output)
            ans=session.evaluate(wlexpr(output))
        except:
            return "None"
    return ans
def equiv(model_output, answer, unit):
    
    try:
        # model_output=model_output.replace(',', '')
        model_output=str(model_output)
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



def get_eg(file):
    count=0
    problem=[]
    exp=[]
    answer=[]
    unit=[]
    with open("../dataset/original/{}_sol.json".format(file), encoding='utf-8') as json_file:
        problems=json.load(json_file)
        for problem_data in problems:
                count+=1
                if count>5:
                    break
                problem_text=problem_data["problem_text"]+" The unit of the answer is "+problem_data["unit"]+"."
                problem.append(problem_text)
                exp.append(problem_data["solution"])
                answer.append(problem_data["answer_number"])
                unit.append(problem_data["unit"])
    return problem, exp, answer,unit
def run(file, engine, start_n, Cot, tool):
    outputs = []
    answers = []
    types = []
    model_outputs=[]
    ls_dict=[]
    list_equiv=[]

    fnames_list = []

    correct = 0
    total = 0
    count=0
    problem_eg, exp_eg, answer_eg,unit_eg = get_eg(file)
    cot_name=""
    session=''

    sys_prompt=prompt_scai.sys_tool_python
    if tool=="python":
        sys_prompt=prompt_scai.sys_tool_python
    else:
        session = WolframLanguageSession('/Applications/Mathematica.app/Contents/MacOS/WolframKernel')
        print(session)
        sys_prompt=prompt_scai.sys_tool_wolfram

    list_lan=get_langueg(file, tool)
    if file=="thermo":
        num_shot=3
    else:
        num_shot=4
    with open("../dataset/original/{}.json".format(file), encoding='utf-8') as json_file:
        problems=json.load(json_file)
        for problem_data in problems:
                count+=1
                if count<=start_n:
                    continue
                prob_book = problem_data["source"]
                fnames_list.append(problem_data["fname"])
                problem_text=problem_data["problem_text"]+" The unit of the answer is "+problem_data["unit"]+"."
                message=tool_ms(sys_prompt, problem_text, problem_eg, exp_eg, answer_eg,unit_eg, list_lan,tool, num_shot)
                model_output_ori=call_engine(message, engine=engine)
                
                print(message, model_output_ori)    
                model_output = extract_lan(model_output_ori, tool, session)
                answer = problem_data["answer_number"]

                types.append(prob_book)
                outputs.append(str(model_output))
                answers.append(answer+"@@"+problem_data["unit"])
                model_outputs.append(model_output_ori)

                print("Model output:")
                print(model_output)
                print("Correct answer:")
                print(answer )
                print(problem_data["unit"])
                print("--------------------------------------------")
                res_equiv = equiv(model_output, answer, problem_data["unit"])
                try:
                    res_equiv = equiv(model_output, answer, problem_data["unit"])
                except:
                    res_equiv = False
                if res_equiv:
                    correct += 1
                total += 1

                print(str(correct) + "/" + str(total))
                list_equiv.append(res_equiv)
                ls_dict.append({'correct': res_equiv, 'gpt solution': model_output_ori, "correct answer": answer+"@@"+problem_data["unit"],
                               "gpt answer": str(model_output), "fname": problem_data["fname"], "source book": prob_book})
                if total % 1==0:
                    with open("./output_{}/{}_dict_{}_{}_{}.json".format(tool, engine, tool, start_n,file), 'w') as fout:
                        json.dump(ls_dict, fout)
                    with open("./output_{}/{}_{}_{}_{}.txt".format(tool, engine,tool, start_n,file), "w+") as f:
                        for k, (output, answer, correctness, fnames, model_output) in enumerate(zip(outputs, answers, list_equiv, fnames_list, model_outputs)):
                            f.write("\n{} Correct: {} | OUTPUT: {} | ANSWER: {} | fname:{} | gpt: {}\n".format(k, correctness, output, answer, fnames, model_output))

                        f.write("#####################\n")
                        print("#####################")
                        f.write("#####################\n")
                        print("Overall Accuracy = {}/{} = {:.3f}".format(correct, total, correct/total))
                        f.write("Overall Accuracy = {}/{} = {:.3f}\n".format(correct, total, correct/total))
    if tool=="wolfram":
        session.terminate()
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', type=str, default='gpt-4')
    parser.add_argument('--tool', type=str, default='wolfram')
    parser.add_argument('--Cot', action='store_true')
    parser.add_argument('--start_num', type=int, default=0)     
    parser.add_argument('--list_source', nargs='+', default=["atkins", "calculus","chemmc","class","diff","fund","matter","quan","stat","thermo"])
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    
    for source in args.list_source:
        run(source,args.engine, args.start_num, args.Cot, args.tool)
    
