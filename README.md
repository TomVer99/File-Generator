# File Generator

![Release](https://img.shields.io/github/v/release/TomVer99/File-Generator?label=Release&style=flat-square)
![Stars](https://img.shields.io/github/stars/TomVer99/File-Generator?label=Stars&style=flat-square)

![Maintained](https://img.shields.io/maintenance/yes/2022?label=Maintained&style=flat-square)
![Issues](https://img.shields.io/github/issues-raw/TomVer99/File-Generator?label=Issues&style=flat-square)

![license](https://img.shields.io/github/license/TomVer99/File-Generator?color=blue&label=License&style=flat-square)

## Description

This is a simple file generator that uses .xml files to generate files in multiple languages.

`gen.source.xml`, `gen.source.simulator.xml` and `gen.source.intrusion.xml` are example files and should not be used for anything else.

## Usage

The file generator uses .xml files to generate files. The structure of the .xml file is explained below in the wiki. (not yet implemented)

When the .xml files are set up, the generator can be run. It does not take any arguments so you can execute it however you want. The generator will then look for .xml files in the same directory as the generator and generate the files in the specified output directory.

## Supported languages

| Language        | Generation | Planned  | Parsing | Planned |
| --------------- | ---------- | -------- | ------- | ------- |
| C++ (class)     | ✔️         | 🔶      | ✔️      | 🔶     |
| C++ (functions) | ❌         | ✔️      | ❌      | ✔️     |
| C               | ❌         | ✔️      | ❌      | ✔️     |

## Requirements

- Python 3.X (tested with 3.10.0)
  - xmlschema
