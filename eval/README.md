## zero shot no sys

```bash
cd eval
mkdir output_zero_nosys
OPENAI_API_KEY=your_key python eval_zero.py 
```

## zero shot with sys

```sh
cd eval
mkdir output_zero
OPENAI_API_KEY=your_key python eval_zero.py --sys 
```

## zero shot Cot

```sh
cd eval
mkdir output_zeroCot
OPENAI_API_KEY=your_key python eval_zeroCot.py 
```

## few shot 

```sh
cd eval
mkdir output_few
OPENAI_API_KEY=your_key python eval_few.py 
```

## few shot Cot

```sh
cd eval
mkdir output_fewCot
OPENAI_API_KEY=your_key python eval_few.py --Cot 
```

## python few shot 

```sh
cd eval
mkdir output_python
OPENAI_API_KEY=your_key python eval_tool.py --tool python
```
## wolfram few shot 
First, you need to create a wolfram account and download wolfram software on desktop. Please refer: https://reference.wolfram.com/language/WolframClientForPython/docpages/basic_usages.html

```sh
pip install wolframclient
cd eval
mkdir output_wolfram
OPENAI_API_KEY=your_key python eval_tool.py --tool wolfram
```

Description:\
--start_num _index number of the frist sample to test._ \
--engine _LLM model engine (eg. gpt-4)_ \
--list_source _list of textbook sources to test._ 

