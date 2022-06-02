# `todo-cli`

**Usage**:

```console
$ todo-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `login`: Login to the TODO app with your email and...
* `logout`: Logout from the TODO app.
* `register`: Register to the TODO app with your email and...

## `todo-cli login`

Login to the TODO app with your email and password.
Your credentials are stored until your run the logout command.

**Usage**:

```console
$ todo-cli login [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `todo-cli logout`

Logout from the TODO app.

**Usage**:

```console
$ todo-cli logout [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `todo-cli register`

Register to the TODO app with your email and password.

**Usage**:

```console
$ todo-cli register [OPTIONS] EMAIL
```

**Arguments**:

* `EMAIL`: The email of the user  [required]

**Options**:

* `--help`: Show this message and exit.
