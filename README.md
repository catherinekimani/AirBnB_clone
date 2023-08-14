# Python AirBnB clone - The console

![catherine](/AirBnB_logo/bnb.png)

## Description

<p>Welcome to our Python Airbnb Clone Project! This repository represents Part 1 of our larger project, where we've developed a powerful Command Interpreter.</p>

## Features
- Create a new object (ex: a new User or a new Place)
- Retrieve an object from a file, a database etc…
- Do operations on objects (count, compute stats, etc…)
- Update attributes of an object
- Destroy an object

## Usage
### Interactive Mode

<p> To use the Command Interpreter in interactive mode, follow these steps: </p>

1. Clone the repository.
2. Navigate to the project directory in your terminal.
3. Run the Command Interpreter by executing ./console.py.
4. You will see the (hbnb) prompt, indicating the interpreter is ready for commands.

### sample interactive session

```
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb) 
(hbnb) 
(hbnb) quit
$
```

### Non-Interactive Mode
<p> You can also use the Command Interpreter in non-interactive mode </p>

### sample non-interactive session

```
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
```

## Authors

- Emmanuel Mwembe: [mwembeemmanuel@gmail.com](mailto:mwembeemmanuel@gmail.com)
- Catherine Kimani: [catherinekimani882@gmail.com](mailto:catherinekimani882@gmail.com)
