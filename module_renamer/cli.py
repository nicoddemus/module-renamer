# -*- coding: utf-8 -*-
"""Console script for module_renamer."""
from __future__ import absolute_import

import sys

import click

from module_renamer.commands.rename_imports import rename_modules
from .commands.analyze_modifications import analyze_modifications

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """
    Console script for module_renamer.
    """
    pass


@main.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--compare-with', default='master',
              help='Branch to be compared with [Default: master]')
@click.option('--branch', default=False,
              help='Branch that has the modifications [Default: current active branch]')
@click.option('--output-file', default='list_output.py',
              help='Change the name of the output file [Default: list_output.py]')
def analyze(project_path, compare_with, branch, output_file):
    """
    Generate the difference between the imports on two different branches.

    Command to analyze all modifications made between two different branches. The output will be a
    list written directly to a file (which will later be used by the script to rename the imports)

    Ex.:
    The following command generate a "list_output.py" with the difference between the
    current branch (that contains the modification) against the master.

    > renamer analyze project_path

    It's possible to use the flag --branch to point to branch different than the current one.
    It's possible to set --output-file to change the default output file name.

    > renamer analyze project_path --branch=my-branch --output-file=my_file.py

    And finally, it's possible to change the branch with which the modifications will be compared.

    > renamer analyze project_path --branch=my-branch --compare-with=my-other-branch

    """
    analyze_modifications(project_path, compare_with, branch, output_file)


@main.command()
@click.argument('project_path', nargs=-1, type=click.Path(exists=True))
@click.argument('import-file', type=click.Path(exists=True, resolve_path=True))
def rename(project_path, import_file):
    """
    Renames the imports statements of a project from a given file with a list of changed imports.

    Command to rename all imports statements of a project from a given list of imports.
    This file can be generated by the command analyze, or created manually.

    This file must have a list named 'imports_to_move' and each item of this list must be a tuple
    where the first element is the old path and the second element is the new path.

    Example.: The class Door was located at home.room and now is located on home.basic_material

    File Name: list_output.py
    Content:   imports_to_move = [('home.room.door'),(home.basic_material.door)]


    :param str project_path:
        A Path (or Paths) of the project that is going to be processed by the script.
    :param str import_file:
        Path of the file with the list of changed imports.

    """
    rename_modules(project_path, import_file)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
