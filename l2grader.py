
import os
import sys
import subprocess,glob
import ntpath
import re
import types
import ast
import builtins
#from unittest.mock import patch, call

instructor = False

def test_part1(alphabetical_order):
    
    grade1 = 0
    
    
    try:
        f='b';s='c'; t='a'
        f,s,t = alphabetical_order('b','c','a')
        #print(ord_lst)
        if f=='a' and s=='b' and t=='c':
            grade1 += 5
            print(f'test1 with input {"b","c","a"}.... pass')
        else:
            print(f'test1 with input {"b","c","a"}.... fail')
    except Exception as ex:
        pass
        
    
    
    try:
        f='c';s='b'; t='a'
        f,s,t = alphabetical_order(f,s,t)
        #print(ord_lst)
        if f=='a' and s=='b' and t=='c':
            grade1 += 2.5
            print(f'test2 with input {"c","b","a"}.... pass')
        else:
            print(f'test2 with input {"c","b","a"}.... fail')
    except Exception as ex:
        pass
    
    try:
        f='c';s='a'; t='b'
        f,s,t = alphabetical_order(f,s,t)
        #print(ord_lst)
        if f=='a' and s=='b' and t=='c':
            grade1 += 2.5
            print(f'test3 with input {"c","a","b"}.... pass')
        else:
            print(f'test3 with input {"c","a","b"}.... fail')
    except Exception as ex:
        pass
    
    return grade1


def test_part2(count_odd):
    
    #from basename import count_odd
    
    grade2 = 0
    
    a=1;b=2;c=3;d=4
    try:
        output = count_odd(a,b,c,d)
        if output == 2:
            grade2 += 5
            print(f'test1 with input {a,b,c,d}....     pass')
        else:
            print(f'test1 with input {a,b,c,d}....     fail')
    except Exception as ex:
        pass
        
    a=19
    b=19
    c=19
    d=19
        
    try:
        output = count_odd(a,b,c,d)
        if output == 4:
            grade2 += 5
            print(f'test2 with input {a,b,c,d}.... pass')
        else:
            print(f'test2 with input {a,b,c,d}.... fail')
    except Exception as ex:
        pass
    
    return grade2

def test():
    
    files = glob.glob('lab2-*.ipynb')
    
    grades = []
    stud_nums = []
    error = []
    
    for fn in files:

        basename = os.path.splitext(os.path.basename(fn))[0]
        stud_num = basename.split('-')[1]
        lab_name = basename.split('-')[0]
        
        with open('notebook.py', 'w') as outputFile:
            subprocess.call(['jupyter', 'nbconvert', '--to', 'script',
                             fn, '--stdout'], stdout=outputFile)

        #tree = ast.parse(open(fn).read(), 'eval')
        with open('notebook.py') as fp:
            tree = ast.parse(fp.read(), 'eval')
        
        for node in tree.body[:]:
            if (not isinstance(node, ast.FunctionDef) and not isinstance(node, ast.Import)
                and not isinstance(node, ast.ImportFrom)):
                tree.body.remove(node)
        module = types.ModuleType(basename)
        #print(module.__dict__)
        # use compile to exec multi-line
        code = compile(tree,fn, 'exec')
        sys.modules['basename'] = module
        exec(code,module.__dict__)
        
        
        from basename import alphabetical_order, count_odd
        import math
        
        print('='*20)
        print(f'Part 1: Alphabetical Order')
        print('='*20)

        grade_p1 = test_part1(alphabetical_order)
        
        print()
        
        print('='*20)
        print(f'Part 2: Count odd numbers')
        print('='*20)

        grade_p2 = test_part2(count_odd)

        grades.append(grade_p1+grade_p2)
        stud_nums.append(stud_num)
    
    return stud_nums,grades,lab_name

if __name__ == "__main__":

    num, grade,lab_name = test()


    if instructor:
        import pandas as pd
        
        print('='*40)
        print(f'Student ID\t\t' + f'Grade')
        print('='*40)

        for i in range(len(num)):
            print(f'{num[i]}\t\t\t' + f'{grade[i]}')
        
        
        df = pd.DataFrame(list(zip(num,[float(x) for x in grade])),columns =['Student ID', 'Grade'])
        df.to_excel(f'{lab_name}.xlsx')
    
    else:
        print('='*40)
        print(f'Student ID\t\t' + f'Grade')
        print(f'{num[0]}\t\t\t' + f'{grade[0]}')
        print('='*40)
    


