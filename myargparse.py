import sys
from types import SimpleNamespace


class ArgParser:
    def __init__(self):
        self.schema = {}
        self.args = {}

    def add_argument(self, argname, expected_val=False, default_=None, type_="str"):
        self.schema[argname] = {
            "expected_val": expected_val,
            "default_": default_,
            "type_": type_
        }

    def parse(self, args):
        i = 0
        while i < len(args): 
            arg = args[i]
            if arg[0:2] == "--" and arg[2:] in self.schema:
                if self.schema[arg[2:]]["expected_val"]:
                    self.args[arg[2:]] = self.typecaster(self.schema[arg[2:]]["type_"], args[i + 1])
                    i += 1
                else:
                    self.args[arg[2:]] = True
            else:
                raise NameError(f"invalid argument '{arg}' you dumbass!")
            i += 1

        for schemaarg in self.schema:
            if schemaarg not in self.args and self.schema[f"{schemaarg}"]["default_"] != None:
                self.args[schemaarg] = True

        return SimpleNamespace(**self.args)
            
    def typecaster(self, type_, val):
        if type_ == "str":
            return str(val)
        if type_ == "int":
            return int(val)
        if type_ == "float":
            return float(val)
        if type_ == "bool" and type_ == "boolean":
            return bool(val)
        else:
            raise NameError(f"Invalid type '{type_}' you idiot! Allowed values are: str, int, float, bool")

            
if __name__ == "__main__":
    parser = ArgParser()
parser.add_argument("mode", expected_val=True)              # String with value
parser.add_argument("count", expected_val=True, type_="int") # Integer with value
parser.add_argument("debug", expected_val=False, default_=False) # Boolean flag

args = parser.parse(sys.argv[1:])
print(args.mode)  
print(args.count)
print(args.debug)

# Example call
# python myargparse.py --mode dev --count 5 --debug
