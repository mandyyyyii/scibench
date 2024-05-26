# SciBench


**SciBench** is a novel benchmark for college-level scientific
problems sourced from instructional textbooks. The benchmark is designed to evaluate the complex reasoning capabilities,
strong domain knowledge, and advanced calculation skills of LLMs. 

We developed an innovative **evaluation protocol** for a detailed analysis of reasoning abilities. This
involves instructing LLMs to self-identify and categorize their errors within a predefined set of
capabilities. This process offers a fine-grained understanding of where the models are falling short.

## Update
- Our paper has been accepted for **ICML 2024**.
- Our dataset is now accessible at [Huggingface Datasets](https://huggingface.co/datasets/xw27/scibench). 
- The multimodal dataset is available in the `./data/img` folder. 
- Our dataset has been updated with minor changes. The previous version can be accessed in the "old" branch. For the latest results based on our most current dataset, please visit our [website](https://scibench-ucla.github.io).

## Data
![Alt text](assets/example.jpg)

The SciBench dataset is under dataset/original folder in json file format. Each file is list of dictionary and can be extracted using following scripts.
Each file stands for one textbook, which is fully elaborated in the paper. 

```
subject='atkins'
with open("./data/original/{}.json".format(subject), encoding='utf-8') as json_file:
    problems=json.load(json_file)

```

## Evaluation
To evaluate our data using LLM, please refer to folder under eval

## Analysis (Evaluation Protocol)
![Alt text](assets/pipeline.jpg)

The evaluation protocol involves analyzing both LLM
and reference (correct) solutions with the assistance of human annotators to identify error reasons.
These reasons are then summarized into ten essential scientific problem-solving skills in which LLM
may face challenges. Subsequently, a LLM verifier is employed to automatically attribute each
incorrectly answered problem to a lack of a specific skill. The resulting error profiles enable the
interpretation of the improved skills by certain prompting strategies and direct comparison of various
strategies.
### run evaluation protocol
After running the evaluation part, use the output to run the evaluation protocol. "setting" refers to the experiment setting: zero_nosys, zero, zeroCot, few, fewCot, python, wolfram, which are fully explained under eval folder.
```
cd eval
OPENAI_API_KEY=your_key python ana_error.py --setting your_setting 
```

## Citation
If you find our paper useful, please cite our paper
```
@inproceedings{wang2024scibench,
author = {Wang, Xiaoxuan and Hu, Ziniu and Lu, Pan and Zhu, Yanqiao and Zhang, Jieyu and Subramaniam, Satyen and Loomba, Arjun R. and Zhang, Shichang and Sun, Yizhou and Wang, Wei},
title = {{SciBench: Evaluating College-Level Scientific Problem-Solving Abilities of Large Language Models}},
booktitle = {Proceedings of the Forty-First International Conference on Machine Learning},
year = {2024},
}
```
