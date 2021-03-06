import os, re

FREE_MEMBER = '~'

class Member(object):
    def __init__(self, vars={ FREE_MEMBER : 1 }):
#        self.__str__ = self.__repr__
        self.vars = vars
        
    def __str__(self):
        result = ''
        for var,power in sorted(self.vars.items()):
            if var == FREE_MEMBER:
                continue
            elif power == 1:
                result += var
            else:
                result +=var + '^' + str(power)
        return result
    
    def __eq__(self, other):
        return self.__str__() == other.__str__()
     
    def __cmp__(self, other):
        key1 = sorted([(-p, v) for v,p in sorted(self.vars.items())])
        key2 = sorted([(-p, v) for v,p in sorted(other.vars.items())])
        return cmp(key1, key2)
        
    def __hash__(self):
        return hash(self.__str__())
    
    def __mul__(self, other):
        result = self.vars.copy()
        for var, power in other.vars.items():
            if var == FREE_MEMBER:
                continue
            elif var in result:
                result[var] += power
            else:
                result[var] = power
        return Member(result)
        
    def is_free(self):
        return self.vars.keys() == [FREE_MEMBER]
        
class Polynom(object):
    
    def __init__(self, polynom={}):
#        self.__str__ = self.__repr__
        self.polynom = polynom
    
    def __getitem__(self, key):
        return self.polynom[key]
    
    def __setitem__(self, key, value):
        self.polynom[key] = value
    
    def __contains__(self, key):
        return key in self.polynom
        
    def copy(self):
        return Polynom(self.polynom.copy())
    
    def code(self):
        result = 0
        for v in self.polynom.values():
            result += v
        return result
            
    def __str__(self):
        result = ''
        for member,count in sorted(self.polynom.items()):
            # Free member
            if member.is_free() and count != 0:
                result += '%+d' % count 
            # Skip 1 and -1 multiplicatgor
            elif count == 1:
                result += '+' + str(member)
            elif count == -1:
                result += '-' + str(member)
            elif count > 0:
                result += '+' + str(count) + '' + str(member)
            elif count < 0:
                result += str(count) + '' + str(member)
        # Remove leading plus if exists
        if len(result) > 0 and result[0] == '+':
            result = result[1:]
        return result
        
    def __add__(self, other):
        result = self.copy()
        for member in other.polynom.keys():
            if member in result:
                result[member] += other.polynom[member]
            else:
                result[member] = other.polynom[member]
        return result
 
    def __sub__(self, other):
        result = self.copy()
        for member in other.polynom.keys():
            if member in result:
                result[member] -= other.polynom[member]
            else:
                result[member] = -other.polynom[member]
        return result
    
    def ___neg__ (self):
        result = self.copy()
        for member,count in result.items():
            result[member] = -count
        return result
        
    def __mul__(self, other):
        result = Polynom({})
        for member1, count1 in self.polynom.items():
            for member2, count2 in other.polynom.items():
                count = count1 * count2
                member = member1 * member2
                if member in result:
                    result[member] += count
                else:
                    result[member] = count 
        return result

    def __pow__(self, other):
        result = self.copy()
        for i in range(1, other.polynom[Member()]):
            result *= self
        return result

class DIGIT(Polynom):
    def __init__(self, value):
        super(DIGIT, self).__init__({ Member() : value })
    
class VAR(Polynom):
    def __init__(self, name):
        super(VAR, self).__init__({ Member( { name : 1 } ) : 1 })

def polynom(expression):
    e = expression
    if e.startswith('-'):
        e = '0' + e
    e = re.sub(r'([a-z])([a-z])', r'\1*\2', e)
    e = re.sub(r'(\d)([a-z])', r'\1*\2', e)
    e = re.sub(r'(\d)(\()', r'\1*\2', e)
    e = re.sub(r'([a-z])(\()', r'\1*\2', e)
    e = re.sub(r'(\))([a-z])', r'\1*\2', e)
    e = re.sub(r'(\))(\()', r'\1*\2', e)
    e = re.sub(r'\^', r'**', e)
    e = re.sub(r'([a-z]+)', r'VAR("\1")', e)
    e = re.sub(r'(\d+)', r'DIGIT(\1)', e)
    return eval(e)

def process_file(file):
    tasks = open(file).readlines()
#    tasks = ['(p+q)pq']
    filename, ext = os.path.splitext(file)
    with open(filename + '.html', 'w') as f:
        f.write('%s' % filename)
        f.write('<table border=1><tr><th>Num</th><th>Task</th><th>Answer</th><th>Code</th>')
        total_code = 0
        i = 0
        for task in tasks:
            if not task.strip(): continue
            i += 1
            p = polynom(task)        
            task = re.sub(r'\^(\S)', r'<sup>\1</sup>', task)
            answer = re.sub(r'\^(\S)', r'<sup>\1</sup>', str(p))
            code = p.code()
            total_code += code
            f.write('<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (i, task, answer, code))
        f.write('<tr><td/><td/><td/><td>%s</td></tr>' % total_code)
        f.write('</table>')
        
for file in os.listdir('.'):
    if not file.endswith('.txt'): continue
    process_file(file)
    
