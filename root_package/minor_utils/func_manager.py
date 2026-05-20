# Errors
from .errors import InvalidArgumentError

class Manager:
    managers = {}
    counter = 0

#--------
    def __init__(self, name=None):

        self.__name = (
            name
            if name is not None
            else "Manager"
        )

        self.__funcs = []

        self.id = Manager.counter
        Manager.counter += 1
        Manager.managers[self.id] = self
#--------

#--------(Registration API)--------
    def add_func(self, func=None, name=None, *args, **kwargs):
        def decorator(f, *args, **kwargs):
            self.__validate_func(func, *args, **kwargs)

            if not self.validate_name(name):
                raise InvalidArgumentError(f"Invalid function name '{name}'. Function names must be valid identifiers.")

            func_name = (
                name
                if name is not None
                else f.__name__
            )

            if self.is_existing_func(func_name):
                raise InvalidArgumentError(f"Function '{func_name}' already exists in manager {self.__name}.")
            
            self.__funcs.append(func_name, f)

            return f
        
        if func is None:
            return decorator
        
        return decorator(func)
    
    def del_func(self, name):
        if not self.is_existing_func(name):
            raise InvalidArgumentError(f"Function '{name}' does not exist in manager {self.__name}.")
        
        try:
            func_id = int(name)
            del self.__funcs[func_id]
        except (ValueError, TypeError):
            for i, (func_name, _) in enumerate(self.__funcs):
                    if func_name == name:
                        del self.__funcs[i]
                        break
    
#--------

#--------(Lookup API)--------
    def get_func(self, name):
        if not self.is_existing_func(name):
            raise InvalidArgumentError(f"Function '{name}' does not exist in manager {self.__name}.")
        
        try:
            func_id = int(name)
            return self.__funcs[func_id][1]
        except (ValueError, TypeError):
            for func_name, func in self.__funcs:
                    if func_name == name:
                        return func
#--------

#--------
    def find_func(self, name):
        if not self.is_existing_func(name):
            return None
        
        try:
            func_id = int(name)
            return self.__funcs[func_id][1]
        except (ValueError, TypeError):
            for func_name, func in self.__funcs:
                    if func_name == name:
                        return func
#--------

#--------
    def get_funcs(self):
        return [func for _, func in self.__funcs]
#--------

#--------
    def get_info(self, name = None):
        if name is None:
                return self.__funcs.copy()
        else:
            func = self.get_func(name)
            return [func] if func is not None else []
#--------

#--------
    def find_info(self, name = None):
        if name is None:
                return self.__funcs.copy()
        else:
            func = self.find_func(name)
            return [func] if func is not None else []
#--------

#--------
    def get_func_id(self, name):
        if not self.is_existing_func(name):
            raise InvalidArgumentError(f"Function '{name}' does not exist in manager {self.__name}.")
        
        try:
            func_id = int(name)
            return func_id
        except (ValueError, TypeError):
            for i, (func_name, _) in enumerate(self.__funcs):
                    if func_name == name:
                        return i
#--------

#--------
    def get_func_name(self, name):
        if not self.is_existing_func(name):
            raise InvalidArgumentError(f"Function '{name}' does not exist in manager {self.__name}.")
        
        try:
            func_id = int(name)
            return self.__funcs[func_id][0]
        except (ValueError, TypeError):
            for func_name, _ in self.__funcs:
                    if func_name == name:
                        return func_name
#--------

#--------
    def get_ids(self):
        return list(range(len(self.__funcs)))
#--------

#--------
    def get_names(self):
        return [func_name for func_name, _ in self.__funcs]
#--------

#--------
    def info_to_string(self, name = None):
        funcs = self.get_info(name)
        output = ""
        for i, (func_name, func) in enumerate(funcs):
            output += (
                f"--------\n"
                f"ID = {i}\n"
                f"Name = {func_name}\n"
                f"Function = {func.__name__}\n"
            )
        output += "--------\n"
        return output
#--------

#--------(Config API)--------
    def compile_config(self, config=None):
        ids = list(range(len(self.__funcs)))

        if config is None:
            return ids
        
        env = {"ids": ids}
        result = []

        for expr in config:
            if isinstance(expr, int):
                result.append(expr)
                continue

            value = eval(expr, {}, env)
            if isinstance(value, int):
                result.append(value)
            elif isinstance(value, (list, tuple)):
                result.extend(value)
            else:
                raise InvalidArgumentError(f"Invalid config expression '{expr}'. Config expressions must evaluate to an integer or a list/tuple of integers.")
        
        return result
#--------

#--------
    def sample_menu(self):
        menu = "--------Commands (ID: Name)--------\n" + "Note: commands are executed only by their IDs, not names.\n"
        for i, func_name in enumerate(self.get_names()):
            menu += f"{i}: {func_name}\n"
        menu += "-1: Exit\n" + "-"*16 + "\n"
        return menu
#--------

#--------
    def sample_not_found_func(self, name):
        if not self.is_id(name):
            return f"Functions must be called by their IDs, not names. '{name}' is not an ID."
        
        if not self.is_existing_func(name):
            return f"Function '{name}' not found in manager {self.__name}."
#--------

#--------(Execution API)--------
    def call_func(self, name, *args, safe = False, **kwargs):
        if safe:
            try:
                return self.get_func(name)(*args, **kwargs)
            except Exception as e:
                print(f"Error occurred while calling function '{name}': {e}")
                return None
        else:
            return self.get_func(name)(*args, **kwargs)
#--------

#--------
    def run(self, *, config = None, arguments = None, safe = False):
        order = self.compile_config(config)

        if arguments is None:
            arguments = [([], {}) for _ in self.__funcs]

        if len(arguments) != len(self.__funcs):
            raise InvalidArgumentError(f"Invalid arguments list. The number of argument sets must match the number of functions in the manager ({len(self.__funcs)}).")
        
        results = []

        for func_id in order:
            args, kwargs = arguments[func_id]

            result = self.call_func(func_id, safe = safe, *args, **kwargs)
            results.append(result)

        return results
#--------

#--------
    def run_manual(self, *, arguments = None, safe = False, menu = None):
        if menu is None:
            menu = self.sample_menu()
        else:
            menu = str(menu) + "\n"
        
        invalid_index_message = self.sample_not_found_func("{name}")
        
        if arguments is None:
            arguments = [([], {}) for _ in self.__funcs]

        if len(arguments) != len(self.__funcs):
            raise InvalidArgumentError(f"Invalid arguments list. The number of argument sets must match the number of functions in the manager ({len(self.__funcs)}).")
        
        results = {}

        while True:
            print(menu)
            choice = input("> ").strip()

            if choice == "-1":
                return results
            
            if not self.is_id(choice) or not self.is_existing_func(choice):
                print(invalid_index_message.format(name=choice))
                continue
            
            func_id = int(choice)
            args, kwargs = arguments[func_id]

            result = self.call_func(func_id, *args, safe = safe, **kwargs)
            results.setdefault(func_id, []).append(result)
#--------

# --------(Validation API)--------
    def is_existing_func(self, name):
        try:
            func_id = int(name)
            return 0 <= func_id < len(self.__funcs)
        except (ValueError, TypeError):
            if not self.validate_name(name):
                raise InvalidArgumentError(f"Invalid function identifier '{name}'. '{name}' must be a name or an integer index.")
            
            for func_name, _ in self.__funcs:
                if func_name == name:
                    return True
            return False
#--------

#--------
    def is_id(self, name):
        try:
            func_id = int(name)
            return True
        except (ValueError, TypeError):
            return False
#--------

#--------
    def is_name(self, name):
        if self.validate_name(name):
            return True
        return False
#--------
    
#--------
    @classmethod
    def __validate_func(cls, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise InvalidArgumentError(f"Function '{func.__name__}' raised an error:\n{str(e)}") from e
#--------

#--------
    @staticmethod
    def validate_name(name):
        name = str(name).strip()
        return name.isidentifier()
#--------