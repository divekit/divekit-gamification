from lark import Lark, Transformer,Tree, Token, v_args
from lark.visitors import Interpreter
from enum import Enum
from typing import List
import json , ast
from collections import namedtuple
from badges.models import Badge, UserBadge
from authentication.models import User
from django.db.models import QuerySet
import datetime
import logging


from django.utils import timezone

logger = logging.getLogger(__name__)

class RunTimeError(Exception):
    pass

class DbTypes(Enum):
   Badge = Badge
   UserBadge = UserBadge
   User = User

class Symbol():
   def __init__(self,name,value):
      self.name = name
      self.value = value
   
   def __repr__(self):
      return "({},{})".format(str(self.name),str(self.value))
      
class SymbolTable():
   def __init__(self):
      self.symbols:List[Symbol] = []
      
   def clear_cache(self):
      self.symbols:List[Symbol] = []

   def addSymbol(self,name,value=None):
      symbol =Symbol(name,value)
      self.symbols.append(symbol)
      return symbol
   
   def findSymbolIdxByName(self,name):
      for i in range(len(self.symbols)):
         if(self.symbols[i].name == name):
            return i
      return None
   
   def findSymbolByName(self,name):
      for symbol in self.symbols:
         if(symbol.name == name):
            return symbol
      return None

   def __repr__(self):
      return str(self.symbols)



class CompNode():
   def __init__(self,left,right):
      self.left = left
      self.right = right

class EqualNode(CompNode):
   def run(self):
      if(self.left.run() == self.right.run()): return True
      return False
   
   def __repr__(self):
      return "Equal({},{})".format(str(self.left),str(self.right))

class NotEqualNode(CompNode):
   def run(self):
      if(self.left.run() != self.right.run()): return True
      return False
   
   def __repr__(self):
      return "NotEqual({},{})".format(str(self.left),str(self.right))

class GteNode(CompNode):
   def run(self):
      if(self.left.run() >= self.right.run()): return True
      return False
   def __repr__(self):
      return "GTE({},{})".format(str(self.left),str(self.right))

class GtNode(CompNode):
   def run(self):
      if(self.left.run() > self.right.run()): return True
      return False
   def __repr__(self):
      return "GT({},{})".format(str(self.left),str(self.right))

class LteNode(CompNode):
   def run(self):
      if(self.left.run() <= self.right.run()): return True
      return False
   def __repr__(self):
      return "LTE({},{})".format(str(self.left),str(self.right))

class LtNode(CompNode):

   def run(self):
      if(self.left.run() < self.right.run()): return True
      return False
   
   def __repr__(self):
      return "LT ({},{})".format(str(self.left),str(self.right))

class OrNode(CompNode):
   def run(self):
      if(self.left.run() or self.right.run()): return True
      return False

   def __repr__(self):
      return "Or({},{})".format(str(self.left),str(self.right))

class AndNode(CompNode):

   def run(self):
      if(self.left.run() and self.right.run()): return True
      return False
   
   def __repr__(self):
      return "And({},{})".format(str(self.left),str(self.right))

class TrueNode():
   def __init__(self):
      pass

   def run(self):
      return True
   
   def __repr__(self):
      return "TrueNode"

class FalseNode():
   def __init__(self):
      pass

   def run(self):
      return False
   
   def __repr__(self):
      return "FalseNode"

class NilNode():
   def __init__(self):
      pass

   def run(self):
      return None
   
   def __repr__(self):
      return "NilNode"

class NegNode():
   def __init__(self,arg):
      self.arg = arg

   def run(self):
      return not self.arg
   
   def __repr__(self):
      return "NegNode({})".format(not self.arg)

class BlockNode():

   def __init__(self,statements):
      self.statements = statements
   
   def run(self):
      for statement in self.statements:
         statement.run()
   
   def __repr__(self):
      repr_str = "Block("

      for statement in self.statements:
         repr_str += str(statement) + ", "

      repr_str = repr_str[:-2] + ")"
      return repr_str

class DecNode():

   def __init__(self,name,value=None):
      self.name = name
      self.value = value
   
   def run(self):
      if self.value:
         symbolTable.addSymbol(self.name,self.value.run())
      else:
         symbolTable.addSymbol(self.name)
   
   def __repr__(self):
      return "DecNode({},{})".format(self.name,str(self.value))
   
class AtomNode():

   def __init__(self,type,value):
      self.type = type
      self.value = value
   
   def run(self):
      if(self.type == "STRING"):
         return self.value[1:-1]
      elif(self.type == "NUMBER"):
         eval = ast.literal_eval(self.value)
         if(isinstance(eval,float)):
            return eval
         elif(isinstance(eval,int)):
            return eval
      elif(self.type == "CNAME"):
         return self.value
      
   def __repr__(self):
      return "Atom({})".format(self.value)

class AddNode():
   def __init__(self,left,right):
      self.left = left
      self.right = right
   
   def run(self):
      return self.left.run() + self.right.run()
   
   def __repr__(self):
      return "AddOp({}+{})".format(self.left,self.right)

class MinNode():
   def __init__(self,left,right):
      self.left = left
      self.right = right
   
   def run(self):
      return self.left.run() - self.right.run()
   
   def __repr__(self):
      return "MinOp({}-{})".format(self.left,self.right)

class MinusNode():
   def __init__(self,atom):
      self.atom:AtomNode = atom
   
   def run(self):
      val = self.atom.run()
      if(self.atom.type == "NUMBER"):
         return - val
      elif(self.atom.type == "CNAME"):
         val = symbolTable.findSymbolByName(val).value
         if isinstance(val, (float,int)):
            return - val
      raise RuntimeError("{} not a number".format(val))
   
   def __repr__(self):
      return "Minus(-{})".format(self.atom)

class MulNode():
   def __init__(self,left,right):
      self.left = left
      self.right = right
   
   def run(self):
      return self.left.run() * self.right.run()
   
   def __repr__(self):
      return "MulOp({}*{})".format(self.left,self.right)

class DivNode():
   def __init__(self,left,right):
      self.left = left
      self.right = right
   
   def run(self):
      return self.left.run() / self.right.run()
   
   def __repr__(self):
      return "DivOp({}/{})".format(self.left,self.right)

class AssignNode():
   def __init__(self,name,args):
      self.args = args
      self.name = name
   
   def run(self):
      
      symbol = symbolTable.findSymbolByName(self.name)
      val = self.args.run()
      if not symbol:
         raise RunTimeError("{} not declared".format(self.name))
      symbol.value = val
      

   def __repr__(self):
      return "AssignNode({},{})".format(self.name,self.args)

class ArrNode():
   def __init__(self,args):
      self.args = args
   
   def run(self):
      arr = []
      for arg in self.args:
         arr.append(arg.run())
      
      return arr

   def __repr__(self):
      repr_str = "ArrNode["

      for arg in self.args:
         repr_str += str(arg) + ", "

      repr_str = repr_str[:-2] + "]"
      return repr_str

class ParamNode():
   def __init__(self,param,value):
      self.param = param
      self.value = value
   
   def run(self):
      paramObj = (self.param.value,self.value.run())
      return paramObj
      
   def __repr__(self):
      return "Param({}={})".format(self.param,self.value)

class CallNode():
   def __init__(self,name,args):
      self.args = args
      self.name = name
   
   def run(self):
      if(self.name in DbTypes.__members__):
         params = {}
         func = None
         for arg in self.args:
            if(isinstance(arg,ParamNode)):
               param = arg.run()
               params[param[0]] = param[1]
            elif(isinstance(arg,CallFunNode) and arg.funName in ["first","all","count"]):
               func = arg.run()
         
         if(func):
            val = getattr(DbTypes[self.name].value.objects.filter(**params),func)()
         else:
            val = DbTypes[self.name].value.objects.filter(**params).first()

         if(isinstance(val,QuerySet)):
            return list(val)
      else:
         symbol = symbolTable.findSymbolByName(self.name)
         if(not hasattr(symbol,"value")):
            raise RuntimeError("SYMBOL NOT FOUND {}".format(self.name))
         val = symbol.value   
         for arg in self.args:
            try:
               if(isinstance(arg,CallAtNode)):
                  val = getattr(val,arg.name)
               elif(isinstance(arg,CallArNode)):
                  val = val[arg.run()]
            except Exception as e:
               if(self.name == "request"):
                  return None
               else:
                  raise e
      return val
      
   def __repr__(self):
      return "Call({})".format(self.name)

class CallFunNode():
   def __init__(self,funName,params):
      self.funName = funName
      self.params = params

   def run(self):
      return self.funName

   def __repr__(self):
      return "CallFun({})".format(self.funName)

class CallAtNode():
   def __init__(self,name,):
      self.name = name
   
   def run(self):
      return self.name

   def __repr__(self):
      return "CallAt({})".format(self.name)

class CallArNode():
   def __init__(self,arg):
      self.arg = arg
   
   def run(self):
      return int(self.arg.run())

   def __repr__(self):
      return "CallAr({})".format(self.arg)

class BuiltinFuncCallNode():

   def __init__(self,funcName,args):
      self.funcName = funcName
      self.args = args
   
   def run(self):
      if self.funcName == "log":
         if not (self.args[0]):
            raise RuntimeError("Message for log() is missing!")
         msg = self.args[0].run()
         if(len(self.args) == 2):
            level = self.args[1].run()
         else: level ="DEBUG"

         if level == "DEBUG":
            logger.debug(msg)
         elif level == "INFO":
            logger.info(msg)
         
         return msg
      elif self.funcName == "str":
         obj_str = str(self.args[0].run())
         return obj_str
      elif self.funcName == "int":
         obj_int = int(self.args[0].run())
         return obj_int
      elif self.funcName == "float":
         obj_int = float(self.args[0].run())
         return obj_int
      elif self.funcName == "minutes":     
         return timezone.timedelta(minutes=self.args[0].run())
      elif self.funcName == "hours":         
         return timezone.timedelta(hours=self.args[0].run())
      elif self.funcName == "days":         
         return timezone.timedelta(days=self.args[0].run())
      elif self.funcName == "now":
         return timezone.make_aware(timezone.datetime.now())
      elif self.funcName == "to_date_time":
         if(len(self.args)==2):
            return timezone.make_aware(timezone.datetime.strptime(str(self.args[0].run()),str(self.args[1].run())))
         else:
            return timezone.make_aware(timezone.datetime.strptime(str(self.args[0].run()),"%d/%m/%Y %H:%M"))
      elif self.funcName == "update_badge":
         user_badge:UserBadge = self.args[0].run()
         completed_tasks = self.args[1].run()
         user_badge.progress = completed_tasks
         user_badge.save()
         
      elif self.funcName == "give_badge":
         user_badge = UserBadge()
         badge:Badge = self.args[0].run()
         user_badge.badge = badge
         user_badge.owner = self.args[1].run()

         if(len(self.args) == 3):
            user_badge.progress = self.args[2].run()
         else: user_badge.progress = badge.milestones
         user_badge.save()

         return user_badge      
      else:
         raise RunTimeError("Function {} not defined!".format(self.funcName))
      
   def __repr__(self):
      repr_str = "BuiltinFunc({},".format(self.funcName)

      for arg in self.args:
         repr_str += str(arg) + ", "

      repr_str = repr_str[:-2] + ")"
      return repr_str

class IfNode():

   def __init__(self,args):
      self.args = args
   
   def run(self):
      for if_stat in self.args:
         if(if_stat.run()):
            break
      

   def __repr__(self):
      return "IfStat()"
   
class ConditionNode():

   def __init__(self,condition,block):
      self.condition = condition
      self.block = block
   
   def run(self):
      if(self.condition.run()):
         self.block.run()
         return True
      return False

      
   def __repr__(self):
      return "CondNode()"

class DkbTransformer(Transformer):

   def start(self,args):
      return args[0]

   def block(self,args):
      return BlockNode(args)

   def statement(self,args):
      return args[0]
   
   def dec(self,args):
      if len(args)==1:
         return DecNode(args[0])
      else:
         return DecNode(args[0],args[1])
   
   def min(self,args):
      return MinusNode(args[0])

   def addop(self,args):
      return AddNode(args[0],args[1])
   
   def minop(self,args):
      return MinNode(args[0],args[1])
   
   def mulop(self,args):
      return MulNode(args[0],args[1])
   
   def divop(self,args):
      return DivNode(args[0],args[1])
   
   def atom_ex(self,args):
      return args[0]

   def atom(self,args):
      return AtomNode(args[0].type,args[0].value)

   def call_ex(self,args):
      return args[0]
   
   def call(self,args):
      return CallNode(args[0],args[1:])

   def call_at(self,args):
      return CallAtNode(args[0])

   def call_ar(self,args):
      return CallArNode(args[0])

   def call_fun(self,args):
      return CallFunNode(args[0],args[1:])
   
   def param(self,args):
      return ParamNode(args[0],args[1])

   def ass(self,args):
      return AssignNode(args[0],args[1])

   def array(self,args):
      return ArrNode(args)
      
   def arr_ex(self,args):
      return args[0]

   def builtin_func_call(self,args):
      return BuiltinFuncCallNode(args[0],args[1:])

   def if_statement(self,args):
      return IfNode(args)
   
   def condition_block(self,args):
      return ConditionNode(args[0],args[1])
   
   def stat_block(self,args):
      return args[0]

   def lt(self,args):
      return LtNode(args[0],args[1])
   
   def lte(self,args):
      return LteNode(args[0],args[1])
   
   def gt(self,args):
      return GtNode(args[0],args[1])
   
   def gte(self,args):
      return GteNode(args[0],args[1])
   
   def and_ex(self,args):
      return AndNode(args[0],args[1])
   
   def or_ex(self,args):
      return OrNode(args[0],args[1])
   
   def equals(self,args):
      return EqualNode(args[0],args[1])
   
   def not_equals(self,args):
      return NotEqualNode(args[0],args[1])
   
   def true_ex(self,args):
      return TrueNode()
   
   def false_ex(self,args):
      return FalseNode()
   
   def nil_ex(self,args):
      return NilNode()
   
   def func_ex(self,args):
      return args[0]
   
   def neg(self,args):
      return NegNode(args[0])
   
   def par(self,args):
      return args[0]


parser = Lark.open("grammar.lark", rel_to=__file__)
symbolTable = SymbolTable()

def customRequestObjDecoder(requestObjDict):
    return namedtuple('request', requestObjDict.keys())(*requestObjDict.values())


def run(text,req=None):
   from time import perf_counter
   tstart = perf_counter()
   symbolTable.clear_cache()
   if(req):
      symbolTable.addSymbol("request",json.loads(json.dumps(req),object_hook=customRequestObjDecoder))
   else:
      symbolTable.addSymbol("request",None)

   parse_tree = parser.parse(text)
   # print(parse_tree.pretty())

   ast_nodes = DkbTransformer().transform(parse_tree)
   # print(ast_nodes)

   ast_nodes.run()
   tend = perf_counter()

   print("Time it took to process DSL:",tend-tstart)