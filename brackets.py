import re

def get_eval(count):
    for i in range(count):
        yield i
        
print list(get_eval(10))

tasks = '''
5(x+4)
5x-2(x-3)
a(2b-c+3d)
(x+3)(x+1)
5x+3(2y-4(3x+y))
'''
#tasks='(x+3)(x+1)'
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
        key1 = sorted([(v, -p) for v,p in sorted(self.vars.items())])
        key2 = sorted([(v, -p) for v,p in sorted(other.vars.items())])
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
            result += abs(v)
        return result
            
    def __str__(self):
        result = ''
        for member,count in sorted(self.polynom.items()):
            # Free member
            if member.is_free():
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
    e = re.sub(r'(\d)([a-z])', r'\1*\2', e)
    e = re.sub(r'(\d)(\()', r'\1*\2', e)
    e = re.sub(r'([a-z])(\()', r'\1*\2', e)
    e = re.sub(r'(\))(\()', r'\1*\2', e)
    e = re.sub(r'\^', r'**', e)
    e = re.sub(r'([a-z]+)', r'VAR("\1")', e)
    e = re.sub(r'(\d+)', r'DIGIT(\1)', e)
    return eval(e)

with open('test.html', 'w') as f:
    f.write('<table border=1><tr><th>Task</th><th>Answer</th><th>Code</th>')
    total_code = 0
    for task in tasks.split('\n'):
        if not task.strip(): continue
        p = polynom(task)        
        task = re.sub(r'\^(\S)', r'<sup>\1</sup>', task)
        answer = re.sub(r'\^(\S)', r'<sup>\1</sup>', str(p))
        code = p.code()
        total_code += code
        f.write('<tr><td>' + task + '</td><td>' + answer + '</td><td>' + str(code) + '</td></tr>')
#        print '%s => %s [%d]' % (task, p, p.code())
    f.write('<tr><td/><td/><td>%s</td></tr>' % total_code)
    f.write('</table>')
        
