import os
import time
import openai
import numpy as np
import operator
import json
import argparse
import math
from prompt import prompt_scai
from post_process import parse_math_answer
openai.api_key = os.getenv("OPENAI_API_KEY")

def few(sys, problem, problem_eg, exp_eg, answer_eg, unit_eg, Cot):
    if sys !="":
        
        messages=[{"role": "system", "content": sys}]
    else:
        messages=[]
    for idx in range(len(problem_eg)):
        question_input = "Problem {}.   ".format(idx + 1) + problem_eg[idx] + "\n"
        if Cot:
            question_output = "Explanation for Problem {}:   ".format(idx + 1) + exp_eg[idx] + "\n" + "The answer is \\boxed{"+ answer_eg[idx]+"} "+unit_eg[idx]
        else: 
            question_output = "The answer is \\boxed{"+ answer_eg[idx]+"} "+unit_eg[idx]
        
        messages += [
                {"role": "user", "content": question_input},
                {"role": "assistant", "content": question_output},
            ]
    test_question= "Problem {}.   ".format(len(problem_eg) + 1) + problem + "\n" 
    messages+=[
            {"role": "user", "content": test_question}
          ]
    return messages
    
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

sys_prompt=prompt_scai.sys_cal_box2

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
def run(file, engine, start_n, Cot):
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
    if Cot:
        cot_name="fewCot"
    else:
        cot_name="few"
    with open("../dataset/original/{}.json".format(file), encoding='utf-8') as json_file:
        problems=json.load(json_file)
        for problem_data in problems:
                count+=1
                if count<=start_n:
                    continue
                prob_book = problem_data["source"]
                fnames_list.append(problem_data["fname"])
                problem_text=problem_data["problem_text"]+" The unit of the answer is "+problem_data["unit"]+"."
                message=few(sys_prompt, problem_text, problem_eg, exp_eg, answer_eg,unit_eg, Cot)
                model_output_ori=call_engine(message, engine=engine)
                
                # print(message, model_output_ori)    
                model_output = parse_math_answer(model_output_ori)
                answer = problem_data["answer_number"]

                types.append(prob_book)
                outputs.append(model_output)
                answers.append(answer+"@@"+problem_data["unit"])
                model_outputs.append(model_output_ori)

                print("Model output:")
                print(model_output)
                print("Correct answer:")
                print(answer )
                print(problem_data["unit"])
                print("--------------------------------------------")
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
                               "gpt answer": model_output, "fname": problem_data["fname"], "source book": prob_book})
                if total % 1==0:
                    with open("./output_{}/{}_dict_{}_{}_{}.json".format(cot_name, engine, cot_name, start_n,file), 'w') as fout:
                        json.dump(ls_dict, fout)
                    with open("./output_{}/{}_{}_{}_{}.txt".format(cot_name, engine,cot_name, start_n,file), "w+") as f:
                        for k, (output, answer, correctness, fnames, model_output) in enumerate(zip(outputs, answers, list_equiv, fnames_list, model_outputs)):
                            f.write("\n{} Correct: {} | OUTPUT: {} | ANSWER: {} | fname:{} | gpt: {}\n".format(k, correctness, output, answer, fnames, model_output))

                        f.write("#####################\n")
                        print("#####################")
                        f.write("#####################\n")
                        print("Overall Accuracy = {}/{} = {:.3f}".format(correct, total, correct/total))
                        f.write("Overall Accuracy = {}/{} = {:.3f}\n".format(correct, total, correct/total))
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', type=str, default='gpt-4')
    parser.add_argument('--Cot', action='store_true')
    parser.add_argument('--start_num', type=int, default=0)     
    parser.add_argument('--list_source', nargs='+', default=["atkins", "calculus","chemmc","class","diff","fund","matter","quan","stat","thermo"])
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    
    for source in args.list_source:
        run(source,args.engine, args.start_num, args.Cot)
