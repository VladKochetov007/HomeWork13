import functools
from typing import Any, Callable, TypeVar

# Task 10.3.1: Check if an object is iterable

def isIterable(obj: object) -> bool:
    """
    Checks if an object supports the iteration protocol.
    An object is iterable if iter() can be called on it without raising a TypeError.
    """
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def demonstrate_task_10_3_1() -> None:
    """Demonstrates the isIterable function."""
    print("Demonstrating isIterable function:")
    objects_to_test = [
        [1, 2, 3],        # list (iterable)
        "hello",          # string (iterable)
        (4, 5, 6),        # tuple (iterable)
        range(5),         # range object (iterable)
        {"a": 1, "b": 2}, # dict (iterable, iterates over keys)
        {1, 2, 3},        # set (iterable)
        123,              # int (not iterable)
        None,             # NoneType (not iterable)
        lambda x: x*x     # function (not iterable)
    ]

    print("\\nTesting various objects:")
    for i, obj in enumerate(objects_to_test):
        obj_type_str = str(type(obj)).split("'")[1] # Get a prettier type name
        print(f"Object {i+1} ({obj_type_str}): {obj}")
        if isIterable(obj):
            print(f"  - Is iterable. Contents:")
            try:
                for item in obj: # type: ignore
                    print(f"    - {item}")
            except Exception as e:
                print(f"    Error iterating: {e}")
        else:
            print(f"  - Is NOT iterable.")
        print("-" * 20)

# Task 10.3.2: Create a class from a string using reflection

def create_class_from_string(class_code: str, class_name: str) -> type | None:
    """
    Creates a class from its string representation of code.
    
    Args:
        class_code: A string containing the Python code for the class.
        class_name: The name of the class to be created.
        
    Returns:
        The created class type, or None if creation fails.
    """
    local_namespace: dict[str, Any] = {}
    try:
        exec(class_code, globals(), local_namespace)
        created_class = local_namespace.get(class_name)
        if isinstance(created_class, type):
            return created_class
        else:
            print(f"Error: Class '{class_name}' not found or not a type after exec.")
            return None
    except Exception as e:
        print(f"Error creating class '{class_name}' from string: {e}")
        return None

def demonstrate_task_10_3_2() -> None:
    """Demonstrates creating a class from a string."""
    print("Demonstrating class creation from string:")

    # This is a placeholder for the code from the URL.
    # Replace this with the actual code from:
    # github.com/krenevych/oop/blob/master/labs/lab10/home/task2/main.py
    sample_class_code = """
class MyDynamicClass:
    message = "Hello from MyDynamicClass!"

    def __init__(self, value: int):
        self.value = value
        print(f"MyDynamicClass instance created with value: {self.value}")

    def display(self) -> None:
        print(f"MyDynamicClass instance: value = {self.value}, message = '{self.message}'")

    @staticmethod
    def static_method_example() -> str:
        return "This is a static method."

    @classmethod
    def class_method_example(cls) -> str:
        return f"This is a class method of {cls.__name__}"
"""
    class_name_to_create = "MyDynamicClass"
    print(f"Attempting to create class '{class_name_to_create}' from string:\\n```python\\n{sample_class_code}\\n```")
    
    DynamicClass = create_class_from_string(sample_class_code, class_name_to_create)

    if DynamicClass:
        print(f"\\nSuccessfully created class: {DynamicClass}")
        print(f"Class name: {DynamicClass.__name__}")
        
        # Test static and class methods if they exist
        if hasattr(DynamicClass, "static_method_example"):
            print(f"Calling static method: {DynamicClass.static_method_example()}") # type: ignore
        if hasattr(DynamicClass, "class_method_example"):
            print(f"Calling class method: {DynamicClass.class_method_example()}") # type: ignore

        print("\\nAttempting to instantiate the dynamic class...")
        try:
            instance = DynamicClass(100) # type: ignore
            if hasattr(instance, "display"):
                instance.display() # type: ignore
            else:
                print("Instance created, but 'display' method not found.")
        except Exception as e:
            print(f"Error instantiating or using DynamicClass: {e}")
    else:
        print(f"\\nFailed to create class '{class_name_to_create}'.")

# Task 10.3.3: Function call logger decorator
F = TypeVar('F', bound=Callable[..., Any])

def log_function_call(func: F) -> F:
    """
    Decorator that logs a message to the console indicating the name of the
    function (or method) being called.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling function/method: '{func.__name__}' with arguments: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"Function/method '{func.__name__}' finished execution.")
        return result
    return wrapper # type: ignore 

@log_function_call
def example_function(a: int, b: int, c: str = "default") -> str:
    """An example function to be decorated."""
    print(f"  Inside example_function: a={a}, b={b}, c='{c}'")
    return f"Result: {a + b}, c was '{c}'"

class ExampleClassWithMethod:
    def __init__(self, name: str):
        self.name = name

    @log_function_call
    def greet(self, message: str) -> str:
        """An example method to be decorated."""
        print(f"  Inside {self.name}'s greet method: message='{message}'")
        return f"{self.name} says: {message}"

def demonstrate_task_10_3_3() -> None:
    """Demonstrates the function call logger decorator."""
    print("Demonstrating function call logger decorator:")
    
    print("\\nCalling decorated standalone function 'example_function':")
    result_func = example_function(10, 20, c="test")
    print(f"  Return value from example_function: '{result_func}'")

    print("\\nCreating an instance of ExampleClassWithMethod and calling decorated method 'greet':")
    obj = ExampleClassWithMethod("MyObject")
    result_method = obj.greet("Hello from the decorated method!")
    print(f"  Return value from greet: '{result_method}'")

# Task 10.3.4: Class instantiation logger decorator
T = TypeVar('T', bound=type)

def log_class_instantiation(cls: T) -> T:
    """
    Class decorator that modifies a class so that when a new instance
    is created, a message is printed to the console indicating
    which class instance is being created.
    """
    original_new = cls.__new__

    @functools.wraps(original_new)
    def new_wrapper(subclass: type, *args: Any, **kwargs: Any) -> Any:
        print(f"Creating an instance of class: '{subclass.__name__}' using __new__")
        # Ensure we call __new__ correctly, especially if it's from object
        if original_new is object.__new__:
            instance = original_new(subclass)
        else:
            instance = original_new(subclass, *args, **kwargs) # type: ignore
        return instance

    cls.__new__ = new_wrapper # type: ignore

    # If __init__ is not being called because __new__ is not passing args,
    # we might also need to wrap __init__ if __new__ does not call it.
    # However, the common pattern is for __new__ to return an instance,
    # and then __init__ is called on that instance.
    # If the original class has __init__ and __new__ wrapper does not account for it,
    # it can be problematic. For simplicity, let's assume __new__ is the primary focus
    # for "creating an instance" log.
    # A more robust version might also wrap __init__ if needed.

    # Let's refine to wrap __init__ as well, as it's more common for instance setup logging.
    # The problem statement says "під час створення нового екземпляру", which involves __new__ then __init__.
    # We can log at the start of __init__.
    
    original_init = cls.__init__

    @functools.wraps(original_init)
    def init_wrapper(self: Any, *args: Any, **kwargs: Any) -> None:
        # This message is more aligned with "instance is created and initialized"
        # print(f"Initializing an instance of class: '{self.__class__.__name__}'") # Alternative message
        original_init(self, *args, **kwargs)
        # print(f"Instance of '{self.__class__.__name__}' initialized.") # Alternative after init

    # Let's stick to the __new__ wrapper for "creating an instance" message as per task.
    # The message "creating an instance" is more aligned with __new__.
    # If there are issues with __init__ not being called properly,
    # this means original_new logic was more complex.

    return cls


@log_class_instantiation
class MyDecoratedClass:
    def __init__(self, x: int, y: str):
        print(f"  MyDecoratedClass.__init__ called with x={x}, y='{y}'")
        self.x = x
        self.y = y

    def get_info(self) -> str:
        return f"MyDecoratedClass instance with x={self.x}, y='{self.y}'"

@log_class_instantiation
class AnotherDecoratedClass:
    def __init__(self, name: str):
        print(f"  AnotherDecoratedClass.__init__ called with name='{name}'")
        self.name = name
        # No __new__ defined here, so it will use object.__new__

def demonstrate_task_10_3_4() -> None:
    """Demonstrates the class instantiation logger decorator."""
    print("Demonstrating class instantiation logger decorator:")

    print("\\nCreating instance of MyDecoratedClass:")
    instance1 = MyDecoratedClass(42, "hello decorated class")
    print(f"  Instance info: {instance1.get_info()}")

    print("\\nCreating instance of AnotherDecoratedClass:")
    instance2 = AnotherDecoratedClass("Test Instance")
    print(f"  Instance name: {instance2.name}")
    
    print("\\nCreating another instance of MyDecoratedClass:")
    instance3 = MyDecoratedClass(0, "another")
    print(f"  Instance info: {instance3.get_info()}")


if __name__ == "__main__":
    print("="*40)
    print("### Starting Homework 13 Solution ###")
    print("="*40)

    print("\\n" + "-"*10 + " Task 10.3.1: isIterable " + "-"*10)
    demonstrate_task_10_3_1()

    print("\\n" + "="*40)
    print("\\n" + "-"*10 + " Task 10.3.2: Create class from string " + "-"*10)
    demonstrate_task_10_3_2()

    print("\\n" + "="*40)
    print("\\n" + "-"*10 + " Task 10.3.3: Function call logger decorator " + "-"*10)
    demonstrate_task_10_3_3()

    print("\\n" + "="*40)
    print("\\n" + "-"*10 + " Task 10.3.4: Class instantiation logger decorator " + "-"*10)
    demonstrate_task_10_3_4()

    print("\\n" + "="*40)
    print("### Homework 13 Solution Finished ###")
    print("="*40) 