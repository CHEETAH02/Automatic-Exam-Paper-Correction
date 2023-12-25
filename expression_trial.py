import re

expression = "Sin^2(x),+,Cos^2(x)"

expression = expression.split(",")
print(expression)


def prep_for_neg(expression):
    print(expression)
    modified_expression = []
    i = 0
    print(len(expression))
    while(i < len(expression)):
        #print(i)
        if(expression[i] == '-'):
            if(expression[i+1] == '('):
                i += 2
                bracket_count = 1
                modified_expression.append('+')             #       += "+,(,0,-,("
                modified_expression.append('(')
                modified_expression.append('0')
                modified_expression.append('-')
                modified_expression.append('(')
                while(bracket_count != 0):
                    modified_expression.append(expression[i])
                    if(expression[i] == '('):
                        bracket_count += 1
                    elif(expression[i] == ')'):
                        bracket_count -= 1
                    i += 1
                modified_expression.append(')')         #+= ",)"
            else:
                modified_expression.append('+')
                modified_expression.append('(')
                modified_expression.append('0')
                modified_expression.append('-')
                modified_expression.append(expression[i+1])
                modified_expression.append(')')
                i += 2
            
        else:
            modified_expression.append(expression[i])
            i+=1
    print("line 46")
    print(modified_expression)
    return modified_expression

expression = prep_for_neg(expression)

print("expression after handling neg:")
print(expression)
print(expression[0])
if(expression[0] == '+'):
    print("hello")
    expression = expression[1:]

print(expression)



newexp = []
for i in range(0,len(expression)):
    if(expression[i] == '+' and expression[i-1] == '('):
        pass
    else:
        newexp.append(expression[i])

expression = newexp

print("after handling + first conditin")
print(expression)


def is_operator(char):
    return char in {'+', '-', '*', '/'}

def is_operand(char):
    #return char.isalnum()
    return char not in {'+','-','*','/','(',')'}

def precedence(operator):
    if operator == '+' or operator == '-':
        return 1
    elif operator == '*' or operator == '/':
        return 2
    return 0

def infix_to_prefix(expression):
    stack = []
    output = []

    for char in reversed(expression):
        if is_operand(char):
            output.append(char)
        elif char == ')':
            stack.append(char)
        elif char == '(':
            while stack and stack[-1] != ')':
                output.append(stack.pop())
            stack.pop()  # Discard '('
        elif is_operator(char):
            while stack and precedence(stack[-1]) >= precedence(char):
                output.append(stack.pop())
            stack.append(char)

    while stack:
        output.append(stack.pop())

    output = output[::-1]
    print(output)
    return output


prefix_expression = infix_to_prefix(expression)
print("Infix expression:",expression)
print(type(expression))
print("Prefix expression:", prefix_expression)

formatted_prefix_expression = ""
for i in range(0,len(prefix_expression)) :
    formatted_prefix_expression += prefix_expression[i]
    formatted_prefix_expression += ' '

print(formatted_prefix_expression)
###########################################################


def extract_num_nonnum(variable):
    numbers = re.findall(r'\d+', variable)
    non_numbers = re.findall(r'\D+', variable)
    numbers = ''.join(numbers)
    non_numbers = ''.join(sorted(non_numbers))
    if(numbers == ""):
      numbers+='1'
    return numbers,non_numbers

#####################################################################


def get_contents(s):
  match = re.match(r'([0-9a-z]+)?([A-Z][a-z]*(\^\d+)?\((\w+)\))?(\w+)?', s)

  coefficient = ""
  trig_term = ""
  inside_trig = ""
  coefficient = match.group(1) if match.group(1) else ""
  coefficient+= match.group(5) if match.group(5) else ""
  trig_term = match.group(2) if match.group(2) else ""
  inside_trig = match.group(4) if match.group(4) else ""
  print('Coefficient:', coefficient)  # Outputs: 4a for s = "4aSin^2(x)"
  print('Trig term:', trig_term)  # Outputs: Sin^2(x) for s = "4aSin^2(x)"
  print('Inside trig term:', inside_trig)  # Outputs: x for s = "4aSin^2(x)"
  return coefficient, trig_term, inside_trig


###########################################################################

def simplify_list_int_sum(l) :
    sum = 0
    st = 0
    ans_list = []
    for i in range(1,len(l),2):
        if(l[i].isnumeric()) :
            st=1
            if(l[i-1] == '-'):
                sum -= int(l[i])
            else :
                sum += int(l[i])
        else:
            ans_list.append(l[i-1])
            ans_list.append(l[i])
            print("in line 138")
            print(ans_list)

    if(sum < 0) :
        ans_list.append('-')
        ans_list.append(str(abs(sum)))
    
    elif(len(ans_list) == 0):
        return str(sum)
    
    elif(sum == 0 ):#and st == 1):
        return ans_list
    
    else :
        ans_list.append('+')
        ans_list.append(str(sum))

    return ans_list


###########################################################

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

############################################################

def simplify_add(left_simplified, right_simplified) :
    print("in line 205")
    print(left_simplified)
    print(right_simplified)
    return_data_structure = []
    if(not(isinstance(left_simplified,list))):
        left_simplified = [left_simplified]
    if(len(left_simplified)%2 != 0):
        left_simplified.insert(0,'+')
    if(not(isinstance(right_simplified,list))):
        right_simplified = [right_simplified]
    if(len(right_simplified)%2 != 0):
        right_simplified.insert(0,'+')
    to_return = []
    tempterm = []
    to_return = right_simplified
    for i in range(1,len(left_simplified),2):
        tempterm.clear()
        tempterm.append(left_simplified[i-1])
        tempterm.append(left_simplified[i])
        lcoef, ltrig, ltrigin = get_contents(left_simplified[i])
        lnumcoef, lvarcoef = extract_num_nonnum(lcoef)
        right_simplified = to_return
        to_return = []
        for j in range(1,len(right_simplified),2):
            print("in line 697")
            rcoef, rtrig, rtrigin = get_contents(right_simplified[j])
            rnumcoef, rvarcoef = extract_num_nonnum(rcoef)
            if((ltrig == rtrig) and (lvarcoef == rvarcoef)):
                if(tempterm[0] == right_simplified[j-1]):#same symbols
                    if(tempterm[0] == '+'):
                        num = int(lnumcoef)+int(rnumcoef)
                        # if(num == 0):
                        #     tempterm[1] = 0
                        #     break
                        # elif(num < 0):
                        #     tempterm[0] = '-'
                        # else:
                            # tempterm[0] = '+'
                        tempterm[0] = '+'
                        tempterm[1] = str(abs(num))+lvarcoef+ltrig
                    else:
                        num = int(lnumcoef)+int(rnumcoef)
                        # if(num == 0):
                        #     tempterm[1] = 0
                        #     break
                        # elif(num > 0):
                        #     tempterm[0] = '+'
                        # else:
                        #     tempterm[0] = '-'
                        tempterm[0] = '-'
                        tempterm[1] = str(abs(num))+lvarcoef+ltrig
                else:#different sumbols
                    if(tempterm[0] == '+'):# +, + ,-
                        num = int(lnumcoef)-int(rnumcoef)
                        if(num == 0):
                            tempterm[1] = '0'
                            break      
                        elif(num > 0):
                            tempterm[0] = '+'
                        else:
                            tempterm[0] = '-'                
                        tempterm[1] = str(abs(num))+lvarcoef+ltrig
                    else:#- + +
                        num = int(rnumcoef)-int(lnumcoef)
                        if(num == 0):
                            tempterm[1] = '0'
                            break      
                        elif(num > 0):
                            tempterm[0] = '+'
                        else:
                            tempterm[0] = '-'                     
                        tempterm[1] = str(abs(num))+lvarcoef+ltrig
            elif((ltrigin == rtrigin) and (((ltrig[0:5] == "Sin^2" and rtrig[0:5] == "Cos^2") or (rtrig[0:5] == "Sin^2" and ltrig[0:5] == "Cos^2")) and lvarcoef == rvarcoef) and(tempterm[0] == '+' and right_simplified[0] == '+')):
                if(int(lnumcoef)>int(rnumcoef)):
                    npart = int(lnumcoef)-int(rnumcoef)
                    if(npart == 1):
                        tempterm[1] = lvarcoef+ltrig
                    else :
                        tempterm[1] = str(npart)+lvarcoef+ltrig

                    if(rnumcoef == '1'):
                        #tempterm[0] = '+'
                        to_return.append('+')
                        if(lvarcoef != ''):
                            #tempterm[1] = lvarcoef
                            to_return.append(lvarcoef)    
                        else:
                            #tempterm[1] = lnumcoef+lvarcoef
                            to_return.append(rnumcoef+lvarcoef)
                    else:
                        # tempterm[0] = '+'
                        # tempterm[1] = rnumcoef+lvarcoef
                        to_return.append('+')
                        to_return.append(rnumcoef+lvarcoef)
                        
                elif(int(rnumcoef)>int(lnumcoef)):
                    npart = int(rnumcoef)-int(lnumcoef)
                    if(npart == 1):
                        tempterm[1] = rvarcoef+rtrig
                    else :
                        tempterm[1] = str(npart)+rvarcoef+rtrig


                    if(lnumcoef == '1'):
                        #tempterm[0] = '+'
                        to_return.append('+')
                        if(lvarcoef != ''):
                            #tempterm[1] = lvarcoef
                            to_return.append(lvarcoef)     
                        else:
                            #tempterm[1] = lnumcoef+lvarcoef
                            to_return.append(lnumcoef+lvarcoef) 
                    else:
                        # tempterm[0] = '+'
                        # tempterm[1] = rnumcoef+lvarcoef
                        to_return.append('+')
                        to_return.append(lnumcoef+lvarcoef)

                else :
                    tempterm[0] = '+'
                    tempterm[1] = '0'
                    to_return.append('+')
                    if(lnumcoef == '1'):
                        
                        if(lvarcoef != ''):
                            #tempterm[1] = lvarcoef
                            to_return.append(lvarcoef)  
                            print("in line 331")
                            print(to_return)
                        else:
                            #tempterm[1] = lnumcoef+lvarcoef
                            to_return.append(lnumcoef+lvarcoef)
                            
                    else :
                        # tempterm[0] = '+'
                        # tempterm[1] = lnumcoef+lvarcoef
                        to_return.append(lnumcoef+lvarcoef)
            
            elif((ltrigin == rtrigin) and ((((ltrig[0:5] == "Sec^2" and rtrig[0:5] == "Tan^2") or (ltrig[0:7] == "Cosec^2" and rtrig[0:5] == "Cot^2")) and (tempterm[0] == '+' and right_simplified[j-1] == '-')) and lvarcoef == rvarcoef)):# or ((rtrig[0:5] == "Sec^2" and ltrig[0:5] == "Tan^2") and (tempterm[0] == '-' and right_simplified[j-1] == '+')))
                if(int(lnumcoef)>int(rnumcoef)):
                    npart = int(lnumcoef)-int(rnumcoef)
                    tempterm[0] = '+'
                    if(npart == 1):
                        tempterm[1] = lvarcoef+ltrig
                    else :
                        tempterm[1] = str(npart)+lvarcoef+ltrig

                    if(rnumcoef == '1'):
                        #tempterm[0] = '+'
                        to_return.append('+')
                        if(lvarcoef != ''):
                            #tempterm[1] = lvarcoef
                            to_return.append(lvarcoef)    
                        else:
                            #tempterm[1] = lnumcoef+lvarcoef
                            to_return.append(rnumcoef+lvarcoef)
                    else:
                        # tempterm[0] = '+'
                        # tempterm[1] = rnumcoef+lvarcoef
                        to_return.append('+')
                        to_return.append(rnumcoef+lvarcoef)
                        
                elif(int(rnumcoef)>int(lnumcoef)):
                    npart = int(rnumcoef)-int(lnumcoef)
                    tempterm[0] = '-'
                    if(npart == 1):
                        tempterm[1] = rvarcoef+rtrig
                    else :
                        tempterm[1] = str(npart)+rvarcoef+rtrig


                    if(lnumcoef == '1'):
                        #tempterm[0] = '+'
                        to_return.append('+')
                        if(lvarcoef != ''):
                            #tempterm[1] = lvarcoef
                            to_return.append(lvarcoef)     
                        else:
                            #tempterm[1] = lnumcoef+lvarcoef
                            to_return.append(lnumcoef+lvarcoef) 
                    else:
                        # tempterm[0] = '+'
                        # tempterm[1] = rnumcoef+lvarcoef
                        to_return.append('+')
                        to_return.append(lnumcoef+lvarcoef)

                else :
                    tempterm[0] = '+'
                    tempterm[1] = '0'
                    to_return.append('+')
                    if(lnumcoef == '1'):
                        
                        if(lvarcoef != ''):
                            #tempterm[1] = lvarcoef
                            to_return.append(lvarcoef)  
                            print("in line 331")
                            print(to_return)
                        else:
                            #tempterm[1] = lnumcoef+lvarcoef
                            to_return.append(lnumcoef+lvarcoef)
                            
                    else :
                        # tempterm[0] = '+'
                        # tempterm[1] = lnumcoef+lvarcoef
                        to_return.append(lnumcoef+lvarcoef)

            elif((ltrigin == rtrigin) and ((((ltrig[0:5] == "Tan^2" and rtrig[0:5] == "Sec^2") or (ltrig[0:5] == "Cot^2" and rtrig[0:7] == "Cosec^2")) and (tempterm[0] == '-' and right_simplified[j-1] == '+')) and lvarcoef == rvarcoef)):# or ((rtrig[0:5] == "Sec^2" and ltrig[0:5] == "Tan^2") and (tempterm[0] == '-' and right_simplified[j-1] == '+')))
                if(int(lnumcoef)>int(rnumcoef)):
                    npart = int(lnumcoef)-int(rnumcoef)
                    tempterm[0] = '-'
                    if(npart == 1):
                        tempterm[1] = lvarcoef+ltrig
                    else :
                        tempterm[1] = str(npart)+lvarcoef+ltrig

                    if(rnumcoef == '1'):
                        #tempterm[0] = '+'
                        to_return.append('+')
                        if(lvarcoef != ''):
                            #tempterm[1] = lvarcoef
                            to_return.append(lvarcoef)    
                        else:
                            #tempterm[1] = lnumcoef+lvarcoef
                            to_return.append(rnumcoef+lvarcoef)
                    else:
                        # tempterm[0] = '+'
                        # tempterm[1] = rnumcoef+lvarcoef
                        to_return.append('+')
                        to_return.append(rnumcoef+lvarcoef)
                        
                elif(int(rnumcoef)>int(lnumcoef)):
                    npart = int(rnumcoef)-int(lnumcoef)
                    tempterm[0] = '+'
                    if(npart == 1):
                        tempterm[1] = rvarcoef+rtrig
                    else :
                        tempterm[1] = str(npart)+rvarcoef+rtrig


                    if(lnumcoef == '1'):
                        #tempterm[0] = '+'
                        to_return.append('+')
                        if(lvarcoef != ''):
                            #tempterm[1] = lvarcoef
                            to_return.append(lvarcoef)     
                        else:
                            #tempterm[1] = lnumcoef+lvarcoef
                            to_return.append(lnumcoef+lvarcoef) 
                    else:
                        # tempterm[0] = '+'
                        # tempterm[1] = rnumcoef+lvarcoef
                        to_return.append('+')
                        to_return.append(lnumcoef+lvarcoef)

                else :
                    tempterm[0] = '+'
                    tempterm[1] = '0'
                    to_return.append('+')
                    if(lnumcoef == '1'):
                        
                        if(lvarcoef != ''):
                            #tempterm[1] = lvarcoef
                            to_return.append(lvarcoef)  
                            print("in line 331")
                            print(to_return)
                        else:
                            #tempterm[1] = lnumcoef+lvarcoef
                            to_return.append(lnumcoef+lvarcoef)
                            
                    else :
                        # tempterm[0] = '+'
                        # tempterm[1] = lnumcoef+lvarcoef
                        to_return.append(lnumcoef+lvarcoef)

            else:
                to_return.append(right_simplified[j-1])
                to_return.append(right_simplified[j])

        if(tempterm[1] != '0'):
            to_return.extend(tempterm)

    to_return = simplify_list_int_sum(to_return)

    if(to_return[0] == '+'):
        del to_return[0]
        
    if(len(to_return) == 1):
        return ''.join(to_return)
        
    return to_return



    

############################################################

def simplify_subtract(left_simplified, right_simplified) :
    return_data_structure = []
    if(not(isinstance(left_simplified,list))):
        left_simplified = [left_simplified]
    if(len(left_simplified)%2 != 0):
        left_simplified.insert(0,'+')
    if(not(isinstance(right_simplified,list))):
        right_simplified = [right_simplified]
    if(len(right_simplified)%2 != 0):
        right_simplified.insert(0,'+')
    to_return = []
    tempterm = []
    to_return = right_simplified
    for i in range(1,len(left_simplified),2):
        tempterm.clear()
        tempterm.append(left_simplified[i-1])
        tempterm.append(left_simplified[i])
        lcoef, ltrig, ltrigin = get_contents(left_simplified[i])
        lnumcoef, lvarcoef = extract_num_nonnum(lcoef)
        right_simplified = to_return
        to_return = []
        for j in range(1,len(right_simplified),2):
            rcoef, rtrig, rtrigin = get_contents(right_simplified[j])
            rnumcoef, rvarcoef = extract_num_nonnum(rcoef)
            if((ltrig == rtrig) and (lvarcoef == rvarcoef)):
                if(tempterm[0] == right_simplified[j-1]):#same symbols
                    if(tempterm[0] == '+'):
                        num = int(lnumcoef)-int(rnumcoef)
                        if(num == 0):
                            tempterm[1] = 0
                            break
                        elif(num < 0):
                            tempterm[0] = '-'
                        else:
                            tempterm[0] = '+'
                        tempterm[1] = str(abs(num))+lvarcoef+ltrig
                    else:
                        num = int(rnumcoef)-int(lnumcoef)
                        if(num == 0):
                            tempterm[1] = 0
                            break
                        elif(num > 0):
                            tempterm[0] = '+'
                        else:
                            tempterm[0] = '-'
                        tempterm[1] = str(abs(num))+lvarcoef+ltrig
                else:
                    if(tempterm[0] == '+'):# +, - -(+)
                        num = int(lnumcoef)+int(rnumcoef)
                        if(num == 0):
                            tempterm[1] = 0
                            break                      
                        tempterm[0] = '+'
                        tempterm[1] = str(abs(num))+lvarcoef+ltrig
                    else:# -, - +(-)
                        num = int(rnumcoef)+int(lnumcoef)
                        if(num == 0):
                            tempterm[1] = 0
                            break                      
                        tempterm[0] = '-'
                        tempterm[1] = str(abs(num))+lvarcoef+ltrig

            else:
                to_return.append(right_simplified[j-1])
                to_return.append(right_simplified[j])
                print("in line 744")
                print(to_return)

        if(tempterm[1] != '0'):
            if(tempterm[0] == '+'):
                tempterm[0] = '-'
            else:
                tempterm[0] = '+'
            to_return.extend(tempterm)
    

    
    

    for i in range(0,len(to_return),2):
        if(to_return[i] == '+'):
            to_return[i] = '-'
        else:
            to_return[i] = '+'
    
    to_return = simplify_list_int_sum(to_return)

    if(to_return[0] == '+'):
        del to_return[0]
        
    if(len(to_return) == 1):
        return ''.join(to_return)
        
    return to_return


############################################################################

def is_operand1(char):
    return char.isalnum()

def is_list(char):
    return isinstance(char,list)

def is_operand(char):
    return isinstance(char,list) or char not in('+','-','*','/')

def extract_number_and_variable(input_string):
    number_part = re.search(r'\d+', input_string).group()
    variable_part = re.sub(r'\d+', '', input_string)
    return number_part, variable_part

def build_expression_tree(prefix_expression):
    stack = []

    operators = set(['+', '-', '*', '/'])
    tokens = prefix_expression.split()
    #print(tokens)

    for token in reversed(tokens):
        if is_operand(token):
            node = TreeNode(token)
            stack.append(node)
        elif token in operators:
            node = TreeNode(token)
            node.left = stack.pop()
            node.right = stack.pop()
            stack.append(node)

    return stack.pop()

def display_tree(root, level=0, prefix="Root: "):
    if root is not None:
        print(" " * (level * 4) + prefix + str(root.value))
        if root.left is not None or root.right is not None:
            display_tree(root.left, level + 1, "L--- ")
            display_tree(root.right, level + 1, "R--- ")


def simplify_expression_tree(root):

    return_data_structure = []
    if root is None:
        return None

    if is_operand(root.value):
        return root.value

    left_simplified = simplify_expression_tree(root.left)
    right_simplified = simplify_expression_tree(root.right)
    #print(return_data_structure)

    if root.value == '+':
        if is_operand(left_simplified) and is_operand(right_simplified):       
            return simplify_add(left_simplified,right_simplified)

    elif root.value == '/':

        if(not(isinstance(left_simplified,list))):
            left_simplified = [left_simplified]
        if(len(left_simplified)%2 != 0):
            left_simplified.insert(0,'+')
        if(not(isinstance(right_simplified,list))):
            right_simplified = [right_simplified]
        if(len(right_simplified)%2 != 0):
            right_simplified.insert(0,'+')
        if(len(right_simplified) == 2):
            
            rcoef, rtrig, rtrigin = get_contents(right_simplified[1])
            rnumcoef, rvarcoef = extract_num_nonnum(rcoef)
            for i in range(1,len(left_simplified),2):
                numerator = ""
                denominator = ""
                if(left_simplified[i-1] == right_simplified[0]):
                    return_data_structure.append('+')
                else:
                    return_data_structure.append('-')
                lcoef, ltrig, ltrigin = get_contents(left_simplified[i])
                lnumcoef, lvarcoef = extract_num_nonnum(lcoef)
                if((int(lnumcoef) % int(rnumcoef)) == 0):
                    numerator += str(int(int(lnumcoef)/int(rnumcoef)))
                else:
                    numerator += lnumcoef
                    denominator += rnumcoef
                if(sorted(lvarcoef) != sorted(rvarcoef)):
                    numerator += lvarcoef
                    denominator += rvarcoef

                if((ltrigin == rtrigin) and (ltrig[0:3] == "Sin" and (rtrig[0:4] == "Cos(" or rtrig[0:4] == "Cos^"))):
                    if(ltrig[3] == '('):
                        lpow = 1
                    else:
                        lpow = int(ltrig[4])
                    if(rtrig[3] == '('):
                        rpow = 1
                    else:
                        rpow = int(rtrig[4])
                    
                    

                    if(lpow > rpow):
                        npart = lpow - rpow
                        if(npart == 1):
                            numerator += "Sin("+ltrigin+")"
                        else:
                            numerator += "Sin^"+str(npart)+"("+ltrigin+")"
                        if(rpow == 1):
                            numerator += "Tan("+ltrigin+")"
                        else:
                            numerator += "Tan^"+str(rpow)+"("+ltrigin+")"

                    elif(rpow > lpow):
                        npart = rpow - lpow
                        if(npart == 1):
                            denominator += "Cos("+ltrigin+")"
                        else:
                            denominator += "Cos^"+str(npart)+"("+ltrigin+")"
                        if(lpow == 1):
                            numerator += "Tan("+ltrigin+")"
                        else:
                            numerator += "Tan^"+str(lpow)+"("+ltrigin+")"
                    else:
                        if(rpow == 1):
                            numerator += "Tan("+ltrigin+")"
                        else:
                            numerator += "Tan^"+str(rpow)+"("+ltrigin+")"
                elif(ltrig == rtrig):
                    pass
                else:
                    numerator += ltrig
                    denominator += rtrig
                    
                if(denominator != ""):
                    return_data_structure.append(numerator+"/"+"("+denominator+")")
                else:
                    return_data_structure.append(numerator)

        else:
            return_data_structure.append(left_simplified+"/"+"("+right_simplified+")")


        if(return_data_structure[0] == '+'):
            del return_data_structure[0]
        if(len(return_data_structure) == 1):
            return_data_structure = ''.join(return_data_structure)

        return return_data_structure
                

    elif root.value == '-':
        
        if is_operand(left_simplified) and is_operand(right_simplified):
            return simplify_subtract(left_simplified,right_simplified)

    elif root.value == '*':
        if is_operand(left_simplified) and is_operand(right_simplified):
            if(not(isinstance(left_simplified,list))):
                left_simplified = [left_simplified]
            if(len(left_simplified)%2 != 0):
                left_simplified.insert(0,'+')
            if(not(isinstance(right_simplified,list))):
                right_simplified = [right_simplified]
            if(len(right_simplified)%2 != 0):
                right_simplified.insert(0,'+')
            for i in range(1,len(left_simplified),2):
                lcoef, ltrig, ltrigin = get_contents(left_simplified[i])
                lnumcoef, lvarcoef = extract_num_nonnum(lcoef)
                for j in range(1,len(right_simplified),2):
                    ret_term = ""
                    rcoef, rtrig, rtrigin = get_contents(right_simplified[j])
                    rnumcoef, rvarcoef = extract_num_nonnum(rcoef)
                    if(left_simplified[i-1] == right_simplified[j-1]):
                        return_data_structure.append('+')
                    else :
                        return_data_structure.append('-')
                    
                    ret_term += str(int(lnumcoef) * int(rnumcoef))
                    ret_term += (lvarcoef+rvarcoef)

                    if(ltrigin == rtrigin):
                        if(ltrig[0:3] == "Sin" and rtrig[0:5] == "Cosec") :
                            if(ltrig[3] == '('):
                                lpow = 1
                            else:
                                lpow = int(ltrig[4])
                            if(rtrig[5] == '('):
                                rpow = 1
                            else:
                                rpow = int(rtrig[6])
                            if(lpow > rpow):
                                npart = lpow - rpow
                                if(npart == 1):
                                    ret_term += "Sin("+ltrigin+")"
                                else:
                                    ret_term += "Sin^"+str(npart)+"("+ltrigin+")"
                                

                            elif(rpow > lpow):
                                npart = rpow - lpow
                                if(npart == 1):
                                    ret_term += "Cosec("+ltrigin+")"
                                else:
                                    ret_term += "Cosec^"+str(npart)+"("+ltrigin+")"
                                
                            else:
                                #both sin and cosec have same powers
                                pass
                        
                        elif(ltrig[0:5] == "Cosec" and rtrig[0:3] == "Sin") :
                            if(ltrig[5] == '('):
                                    lpow = 1
                            else:
                                lpow = int(ltrig[6])
                            if(rtrig[3] == '('):
                                rpow = 1
                            else:
                                rpow = int(rtrig[4])
                            if(lpow > rpow):
                                npart = lpow - rpow
                                if(npart == 1):
                                    ret_term += "Cosec("+ltrigin+")"
                                else:
                                    ret_term += "Cosec^"+str(npart)+"("+ltrigin+")"
                                

                            elif(rpow > lpow):
                                npart = rpow - lpow
                                if(npart == 1):
                                    ret_term += "Sin("+ltrigin+")"
                                else:
                                    ret_term += "Sin^"+str(npart)+"("+ltrigin+")"
                                
                            else:
                                #both sin and cosec have same powers
                                pass
                        
                        elif(((ltrig[0:3] == "Sec" and (rtrig[0:4] == "Cos(" or rtrig[0:4] == "Cos^")) or (rtrig[0:3] == "Sec" and (ltrig[0:4] == "Cos(" or ltrig[0:4] == "Cos^"))) or ((ltrig[0:3] == "Tan" and rtrig[0:3] == "Cot") or (rtrig[0:3] == "Tan" and ltrig[0:3] == "Cot"))):
                            if(ltrig[3] == '('):
                                lpow = 1
                            else:
                                lpow = int(ltrig[4])
                            if(rtrig[3] == '('):
                                rpow = 1
                            else:
                                rpow = int(rtrig[4])
                    
                    

                            if(lpow > rpow):
                                npart = lpow - rpow
                                if(npart == 1):
                                    ret_term += ltrig[0:3]+"("+ltrigin+")"
                                else:
                                    ret_term += ltrig[0:4]+str(npart)+"("+ltrigin+")"
                                

                            elif(rpow > lpow):
                                npart = rpow - lpow
                                if(npart == 1):
                                    ret_term += rtrig[0:3]+"("+rtrigin+")"
                                else:
                                    ret_term += rtrig[0:4]+str(npart)+"("+rtrigin+")"
                                
                            else:
                                #both sin and cosec have same powers
                                pass
                        
                        elif(ltrig[0:4] == "Cose" and rtrig[0:4] == "Cose"):
                            if(ltrig[5] == '('):
                                lpow = 1
                            else:
                                lpow = int(ltrig[6])
                            if(rtrig[5] == '('):
                                rpow = 1
                            else:
                                rpow = int(rtrig[6])
                            ret_term += (ltrig[0:5]+"^"+str(lpow+rpow)+"("+ltrigin+")")
                        elif(ltrig[0:3] == rtrig[0:3]):
                            if(ltrig[3] == '('):
                                lpow = 1
                            else:
                                lpow = int(ltrig[4])
                            if(rtrig[3] == '('):
                                rpow = 1
                            else:
                                rpow = int(rtrig[4])
                            ret_term += (ltrig[0:3]+"^"+str(lpow+rpow)+"("+ltrigin+")")
                        else:
                            ret_term += (ltrig+rtrig)

                    else:
                        ret_term += (ltrig+rtrig)

                    return_data_structure.append(ret_term)
                    
            if(return_data_structure[0] == '+'):
                del return_data_structure[0]
            if(len(return_data_structure) == 1):
                return_data_structure = ''.join(return_data_structure)
            return return_data_structure           
                                
                    # if(left_simplified[i].isnumeric() and right_simplified[j].isnumeric()):
                            
                    #     return_data_structure.append(str(int(left_simplified[i])*int(right_simplified[j])))
                    # else:
                    #     npart = int(lnumcoef)*int(rnumcoef)
                    #     return_data_structure.append(str(npart)+lvarcoef+rvarcoef+ltrig+rtrig)
            
            # if(not(is_list(left_simplified)) and not(is_list(right_simplified))):
            #     if(left_simplified == '0' or right_simplified == '0'):
            #         return '0'
            #     elif(left_simplified == '1'):
            #         return right_simplified
            #     elif(right_simplified == '1'):
            #         return left_simplified
            #     elif(left_simplified.isnumeric() and right_simplified.isnumeric()):
            #         return str(int(left_simplified)*int(right_simplified))
                
            #     else:
            #         lcoef, ltrig, ltrigin = get_contents(left_simplified)
            #         lnumcoef, lvarcoef = extract_num_nonnum(lcoef)
            #         rcoef, rtrig, rtrigin = get_contents(right_simplified)
            #         rnumcoef, rvarcoef = extract_num_nonnum(rcoef)
            #         npart = int(lnumcoef)*int(rnumcoef)
            #         return_data_structure.append(str(npart)+lvarcoef+rvarcoef+ltrig+rtrig)
            #         return return_data_structure

            # elif(not(isinstance(left_simplified,list))):
            #     if(left_simplified == '0'):
            #         return '0'
            #     elif(left_simplified == '1'):
            #         return right_simplified
            #     else:
            #         if(not(is_operator(right_simplified[0]))):
            #             right_simplified.insert(0,'+')
            #         lcoef, ltrig, ltrigin = get_contents(left_simplified)
            #         lnumcoef, lvarcoef = extract_num_nonnum(lcoef)
            #         for i in range(1,len(right_simplified),2):
            #             rcoef, rtrig, rtrigin = get_contents(right_simplified[1])
            #             rnumcoef, rvarcoef = extract_num_nonnum(rcoef)
            #             if(left_simplified.isnumeric() and right_simplified[i].isnumeric()):
            #                 return_data_structure.append(right_simplified[i-1])
            #                 return_data_structure.append(str(int(left_simplified)*int(right_simplified[i])))
            #             else:
            #                 return_data_structure.append(right_simplified[i-1])
            #                 npart = int(lnumcoef)*int(rnumcoef)
            #                 return_data_structure.append(str(npart)+lvarcoef+rvarcoef+ltrig+rtrig)#left_simplified+right_simplified[i])
            #         if(return_data_structure[0] == '+'):
            #             del return_data_structure[0]

            #         return return_data_structure
            

            # elif(not(isinstance(right_simplified,list))):
            #     if(right_simplified == '0'):
            #         return '0'
            #     elif(right_simplified == '1'):
            #         return left_simplified
            #     else:
            #         if(not(is_operator(left_simplified[0]))):
            #             left_simplified.insert(0,'+')
            #         rcoef, rtrig, rtrigin = get_contents(right_simplified)
            #         rnumcoef, rvarcoef = extract_num_nonnum(rcoef)
            #         for i in range(1,len(left_simplified),2):
            #             lcoef, ltrig, ltrigin = get_contents(left_simplified[i])
            #             lnumcoef, lvarcoef = extract_num_nonnum(lcoef)
            #             if(left_simplified[i].isnumeric() and right_simplified.isnumeric()):
            #                 return_data_structure.append(left_simplified[i-1])
            #                 return_data_structure.append(str(int(left_simplified[i])*int(right_simplified)))
            #             else:
            #                 return_data_structure.append(left_simplified[i-1])
            #                 npart = int(lnumcoef)*int(rnumcoef)
            #                 return_data_structure.append(str(npart)+lvarcoef+rvarcoef+ltrig+rtrig)
            #         if(return_data_structure[0] == '+'):
            #             del return_data_structure[0]

            #         return return_data_structure
                   

            # else:
            #     if(not(is_operator(left_simplified[0]))):
            #         left_simplified.insert(0,'+')
            #     if(not(is_operator(right_simplified[0]))):
            #         right_simplified.insert(0,'+')
            #     for i in range(1,len(left_simplified),2):
            #         lcoef, ltrig, ltrigin = get_contents(left_simplified[i])
            #         lnumcoef, lvarcoef = extract_num_nonnum(lcoef)
            #         for j in range(1,len(right_simplified),2):
            #             rcoef, rtrig, rtrigin = get_contents(right_simplified[j])
            #             rnumcoef, rvarcoef = extract_num_nonnum(rcoef)
            #             if(left_simplified[i-1] == right_simplified[j-1]):
            #                 return_data_structure.append('+')
            #             else :
            #                 return_data_structure.append('-')
            #             if(left_simplified[i].isnumeric() and right_simplified[j].isnumeric()):
                            
            #                 return_data_structure.append(str(int(left_simplified[i])*int(right_simplified[j])))
            #             else:
            #                 npart = int(lnumcoef)*int(rnumcoef)
            #                 return_data_structure.append(str(npart)+lvarcoef+rvarcoef+ltrig+rtrig)
            #     if(return_data_structure[0] == '+'):
            #         del return_data_structure[0]

            #     return return_data_structure
                            
expression_tree = build_expression_tree(formatted_prefix_expression)
print("Original Expression Tree:")
display_tree(expression_tree)

simplified_tree = simplify_expression_tree(expression_tree)
print("\nSimplified Expression Tree:")
print(simplified_tree)

print(''.join(simplified_tree))