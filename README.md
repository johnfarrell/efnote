# efnote

**E**xtendable **F**ormat **Note**

### Table of Contents
* [What is EFNote](#what-is-efnote)
* [Features](#features)
* [Usage](#usage)
* [Installation](#installation)
* [Contributing](#contributing)
  * [To-Do](#to-do)
* [Issues](#issues)

## What is EFNote?
EFNote is designed to streamline journaling, notetaking, bug-reporting, or any
other formattable text writing you do.

EFNote is also in heavy development so changes will be frequent and functions
will be limited.

## Features

 
* **Custom format note taking**: Easily create journals, to-do lists, revision logs, etc.; all with your own format. Don't be restricted to a journal with only name, date, and content!
* **Easily search between all EFNote entries**: Whether it be a shopping list, bug report, or diary, easily find what you're looking for between all entries with a dead-simple search interface.
* **Auto prompting for note fields**: Don't waste time away from development formatting a plaintext file.
* **Secure storage**: All notes can be optionally stored in an encrypted local database to ensure your privacy. 
## Usage

EFNote is designed to be as easy to use as possible. Simply run `$ efnote` from your terminal of choice and it will do the rest before getting you back to your work.

For quicker usage, EFNote provides a set of commands to speed the process up.

* `$ efnote new [<format>]`

   Create a new note of a specific format. If no format is specified, a dialog will show displaying the current formats in the `~/.efnote/formats.efn` file and ask for one.
   Formats not already in the `formats.efn` config file are also supported, and if one is entered a dialog will display to create a new format.

* `$ efnote view [<format>]`
  
   View notes of a specified format sorted by most recently edited. Formats not specified in the `formats.efn` config file are similarly supported as in the `$ efnote new` command.

## Installation

Due to EFNote being in heavy development, the install process is a bit convoluted.

#### Clone EFNote
```
$ git clone https://github.com/johnfarrell/efnote.git
```

#### Run install script
**Disclaimer**: Install script is currently not implemented, you have create a symlink yourself.

This will install any dependencies and create a symlink to the directory allowing you to run efnote from anywhere

```
$ cd efnote
$ ./install 
```

#### Run EFNote
```
$ efnote
```

## Contributing

Feel free to contribute and suggest features by cloning this repository or
adding a feature request using the [enhancement](https://github.com/FARRELLJJOHN/efnote/labels/enhancement) issue label.

#### To-Do

 - [x] Create To-Do list.
 - [ ] Create installation script.
 - [x] Implement supported format note creation.
 - [x] Specific note type gross view
 - [ ] Created note searching
 - [ ] Interactive note format creation

## Issues
Please use the GitHub [issue tracker](https://github.com/FARRELLJJOHN/efnote/issues)
to report any bugs you encounter.

## License

Made using the [MIT License](https://opensource.org/licenses/MIT).